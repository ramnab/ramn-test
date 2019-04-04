#!/usr/bin/env bash

CLIENT=$1
ENV=$(echo $2 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
ENV_UPPER=$(echo $2 | awk '{print toupper($0)}')
ENV_LOWER=$(echo $2 | awk '{print tolower($0)}')

if [[ ${ENV_LOWER} = "prod" ]]; then
    LAMBDA_S3=s3-capita-ccm-${CLIENT}-prod-lambdas-eu-central-1
else
    LAMBDA_S3=s3-capita-ccm-${CLIENT}-nonprod-lambdas-eu-central-1
fi

DIRECTORY=`dirname $0`

echo """
----------------------------------------------------
                 Agent Intervals
                 ---------------

"""

echo """

         Deploying AI Lambda and Resources
         ---------------------------------

"""

# Get KMS ARN
KMS=$(python ${DIRECTORY}/../../scripts/get_kms_arn.py connect-master)

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
                                pDepartment=ccm \
                                pTransformationDb=gl_ccm_${ENV_LOWER} \
                                pCommonDestination=s3-capita-ccm-connect-common-${ENV_LOWER}-reporting \
                                pCustomerReportBucket=s3-capita-ccm-connect-${CLIENT}-${ENV_LOWER}-reporting \
                                pKMSArn=${KMS}


rm deploy-agent-intervals.yml

echo """

                 Updating AI Firehose
                 ---------------------

"""

aws lambda invoke --function-name lmbMiFirehoseModder-ccm-${ENV_UPPER} \
                  --payload "{
  \"debug\": true,
  \"ResourceProperties\": {
    \"FirehoseName\": \"kfh-ccm-ai-${ENV_LOWER}\",
    \"Prefix\": \"agent_interval/clientname=${CLIENT}/rowdate=!{timestamp:yyyy-MM-dd}/\",
    \"ErrorPrefix\": \"errors/agent_interval/!{firehose:error-output-type}/clientname=${CLIENT}/rowdate=!{timestamp:yyyy-MM-dd}/\",
    \"TransformationDb\": \"gl_ccm_${ENV_LOWER}\",
    \"TransformationTable\": \"glt_agent_intervals_${ENV_LOWER}\",
    \"TransformationRole\": \"rl_mi_agent_interval_${ENV_LOWER}\"
  }
}" result.txt



python ${DIRECTORY}/../../scripts/tag-firehose.py -f kfh-ccm-ai-${ENV_LOWER} \
                    -t sec:Compliance:Normal bus:BusinessUnit:ccm bus:ClientName:${CLIENT} \
                       tech:Environment:${ENV_LOWER} tech:ApplicationID:capita-ccm-connect \
                       tech:ApplicationRole:reporting



echo """

              Updating AI Daily Firehose
              --------------------------

"""

aws lambda invoke --function-name lmbMiFirehoseModder-ccm-${ENV_UPPER} \
                  --payload "{
  \"debug\": true,
  \"ResourceProperties\": {
    \"FirehoseName\": \"kfh-ccm-ai-daily-${ENV_LOWER}\",
    \"Prefix\": \"agent_daily/clientname=${CLIENT}/rowdate=!{timestamp:yyyy-MM-dd}/\",
    \"ErrorPrefix\": \"errors/agent_daily/!{firehose:error-output-type}/clientname=${CLIENT}/rowdate=!{timestamp:yyyy-MM-dd}/\",
    \"TransformationDb\": \"gl_ccm_${ENV_LOWER}\",
    \"TransformationTable\": \"glt_agent_intervals_${ENV_LOWER}\",
    \"TransformationRole\": \"rl_mi_agent_interval_${ENV_LOWER}\"
  }
}" result.txt

python scripts/tag-firehose.py -f kfh-ccm-ai-daily-${ENV_LOWER} \
                    -t sec:Compliance:Normal bus:BusinessUnit:ccm bus:ClientName:${CLIENT} \
                       tech:Environment:${ENV_LOWER} tech:ApplicationID:capita-ccm-connect \
                       tech:ApplicationRole:reporting


rm result.txt


echo """

         Updating Customer Bucket trigger for AI
         ---------------------------------------

"""

aws lambda invoke --function-name lmbMiReportingModder-ccm-${ENV_UPPER} \
                  --payload "{
                    \"bucket\": \"s3-capita-ccm-connect-${CLIENT}-${ENV_LOWER}-reporting\",
                    \"prefix\": \"connect/ccm-prd-${CLIENT}-connect/reports/agent_interval/\",
                    \"lambda\": \"lmbMIAgentInterval-ccm-${ENV_UPPER}\"}" r.txt


echo """

      Updating Customer Bucket trigger for AI Daily
      ---------------------------------------------

"""

aws lambda invoke --function-name lmbMiReportingModder-ccm-${ENV_UPPER} \
                  --payload "{
                    \"bucket\": \"s3-capita-ccm-connect-${CLIENT}-${ENV_LOWER}-reporting\",
                    \"prefix\": \"connect/ccm-prd-${CLIENT}-connect/reports/agent_daily/\",
                    \"lambda\": \"lmbMIAgentInterval-ccm-${ENV_UPPER}\"}" r.txt




echo """

                  agent interval: complete
----------------------------------------------------


"""