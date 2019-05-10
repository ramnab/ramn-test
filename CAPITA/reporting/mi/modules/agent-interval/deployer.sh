#!/usr/bin/env bash

DEPT=$1
CLIENT=$2
ENV=$(echo $3 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
ENV_UPPER=$(echo ${ENV} | awk '{print toupper($0)}')
ENV_LOWER=$(echo ${ENV} | awk '{print tolower($0)}')

LAMBDA_S3=s3-capita-${DEPT}-connect-${CLIENT}-${ENV_LOWER}-lambdas-eu-central-1

DIRECTORY=$(dirname $0)

function bucket_exists() {
    bucket=$1
    output=$(aws s3api list-buckets --query "Buckets[].Name" --output text)
    if [[ ${output} == *"${bucket}"* ]]; then
        exists="true"
    else
        exists="false"
    fi
}

function resource_exists() {
    stack=$1
    resource=$2
    output=$(aws cloudformation describe-stack-resources --stack-name ${stack} 2> /dev/null)

    if [[ ${output} == *"${resource}"* ]]; then
        exists="true"
    else
        exists="false"
    fi
}

echo """
----------------------------------------------------
                 Agent Intervals
                 ---------------

"""

# check is pre-requisite resources exist
resource_exists stCapita-MI-${ENV}-CrossAccountRole CrossAccountFirehoseRole
if [[ ${exists} == "true" ]]; then
    resource_cross_account_role="Available"
else
    resource_cross_account_role="Not available"
    resources_missing=" (resources missing)"
fi

bucket_exists s3-capita-ccm-connect-${CLIENT}-${ENV_LOWER}-reporting
if [[ ${exists} == "true" ]]; then
    resource_reporting_bucket="Available"
else
    resource_reporting_bucket="Not available"
    resources_missing=" (resources missing)"
fi

resource_exists stCapita-MI-${ENV}-GlueDb GlueDb
if [[ ${exists} == "true" ]]; then
    resource_gluedb="Available"
else
    resource_gluedb="Not available"
    resources_missing=" (resources missing)"
fi

resource_exists stCapita-MI-${ENV}-FirehoseModder FirehoseModderLambda
if [[ ${exists} == "true" ]]; then
    resource_fh_modder="Available"
else
    resource_fh_modder="Not available"
    resources_missing=" (resources missing)"
fi


echo """

Pre-requisites${resources_missing}:

    Cross Account Role         : ${resource_cross_account_role}
    Customer Reporting Bucket  : ${resource_reporting_bucket}
    Glue DB                    : ${resource_gluedb}
    Firehose Modder Lambda     : ${resource_fh_modder}

"""

if [[ ! -z ${resources_missing} ]]; then
    echo "Aborting, pre-requisites missing"
    exit
fi


echo """

         Deploying AI Lambda and Resources
         ---------------------------------

"""

# Get KMS ARN
KEY_ALIAS=connect-master
if [[ ${ENV_LOWER} != 'prod' ]]; then
    KEY_ALIAS=connect-master-${ENV_LOWER}
fi
KMS=$(python ${DIRECTORY}/../../scripts/get_kms_arn.py ${KEY_ALIAS})

echo "KMS key = $KMS"

aws cloudformation package --region eu-central-1 \
                           --template-file ${DIRECTORY}/resources/agent-intervals.yml \
                           --s3-bucket ${LAMBDA_S3} \
                           --output-template-file deploy-agent-intervals.yml

aws cloudformation deploy --region eu-central-1 \
                          --template-file deploy-agent-intervals.yml \
                          --stack-name stCapita-MI-${ENV}-AgentIntervals  \
                          --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
                          --parameter-overrides \
                                pClient=${CLIENT} \
                                pEnvironment=${ENV_UPPER} \
                                pEnvironmentLowerCase=${ENV_LOWER} \
                                pEnvironmentUpperCase=${ENV_UPPER} \
                                pDepartment=${DEPT} \
                                pTransformationDb=gl_${DEPT}_${ENV_LOWER} \
                                pCommonDestination=s3-capita-${DEPT}-connect-common-${ENV_LOWER}-reporting \
                                pCustomerReportBucket=s3-capita-${DEPT}-connect-${CLIENT}-${ENV_LOWER}-reporting \
                                pKMSArn=${KMS}


rm deploy-agent-intervals.yml

echo """

                 Updating AI Firehose
                 ---------------------

"""

aws lambda invoke --function-name lmbMiFirehoseModder-${DEPT}-${ENV_UPPER} \
                  --payload "{
  \"debug\": true,
  \"ResourceProperties\": {
    \"FirehoseName\": \"kfh-${DEPT}-ai-${ENV_LOWER}\",
    \"Prefix\": \"agent_interval/clientname=${CLIENT}/rowdate=!{timestamp:yyyy-MM-dd}/\",
    \"ErrorPrefix\": \"errors/agent_interval/!{firehose:error-output-type}/clientname=${CLIENT}/rowdate=!{timestamp:yyyy-MM-dd}/\",
    \"TransformationDb\": \"gl_${DEPT}_${ENV_LOWER}\",
    \"TransformationTable\": \"glt_agent_intervals_${ENV_LOWER}\",
    \"TransformationRole\": \"rl_mi_agent_interval_${ENV_LOWER}\"
  }
}" result.txt



python ${DIRECTORY}/../../scripts/tag-firehose.py -f kfh-${DEPT}-ai-${ENV_LOWER} \
                    -t sec:Compliance:Normal bus:BusinessUnit:${DEPT} bus:ClientName:${CLIENT} \
                       tech:Environment:${ENV_LOWER} tech:ApplicationID:capita-${DEPT}-connect \
                       tech:ApplicationRole:reporting



echo """

              Updating AI Daily Firehose
              --------------------------

"""

aws lambda invoke --function-name lmbMiFirehoseModder-${DEPT}-${ENV_UPPER} \
                  --payload "{
  \"debug\": true,
  \"ResourceProperties\": {
    \"FirehoseName\": \"kfh-${DEPT}-ai-daily-${ENV_LOWER}\",
    \"Prefix\": \"agent_daily/clientname=${CLIENT}/rowdate=!{timestamp:yyyy-MM-dd}/\",
    \"ErrorPrefix\": \"errors/agent_daily/!{firehose:error-output-type}/clientname=${CLIENT}/rowdate=!{timestamp:yyyy-MM-dd}/\",
    \"TransformationDb\": \"gl_${DEPT}_${ENV_LOWER}\",
    \"TransformationTable\": \"glt_agent_intervals_${ENV_LOWER}\",
    \"TransformationRole\": \"rl_mi_agent_interval_${ENV_LOWER}\"
  }
}" result.txt

python scripts/tag-firehose.py -f kfh-${DEPT}-ai-daily-${ENV_LOWER} \
                    -t sec:Compliance:Normal bus:BusinessUnit:${DEPT} bus:ClientName:${CLIENT} \
                       tech:Environment:${ENV_LOWER} tech:ApplicationID:capita-${DEPT}-connect \
                       tech:ApplicationRole:reporting


rm result.txt


echo """

         Updating Customer Bucket trigger for AI
         ---------------------------------------

"""

# Note that the s3 prefix may need to be changed to point to the correct connect instance
# This is because sometimes the dev Connect instance will be used for testing
aws lambda invoke --function-name lmbMiReportingModder-${DEPT}-${ENV_UPPER} \
                  --payload "{
                    \"bucket\": \"s3-capita-${DEPT}-connect-${CLIENT}-${ENV_LOWER}-reporting\",
                    \"prefix\": \"connect/${DEPT}-dev-${CLIENT}-connect/reports/agent_interval/\",
                    \"lambda\": \"lmbMIAgentInterval-${DEPT}-${ENV_UPPER}\"}" r.txt


echo """

      Updating Customer Bucket trigger for AI Daily
      ---------------------------------------------

"""
# Note that the s3 prefix may need to be changed to point to the correct connect instance
# This is because sometimes the dev Connect instance will be used for testing
aws lambda invoke --function-name lmbMiReportingModder-${DEPT}-${ENV_UPPER} \
                  --payload "{
                    \"bucket\": \"s3-capita-${DEPT}-connect-${CLIENT}-${ENV_LOWER}-reporting\",
                    \"prefix\": \"connect/${DEPT}-dev-${CLIENT}-connect/reports/agent_daily/\",
                    \"lambda\": \"lmbMIAgentInterval-${DEPT}-${ENV_UPPER}\"}" r.txt




echo """

                  agent interval: complete
----------------------------------------------------


"""
