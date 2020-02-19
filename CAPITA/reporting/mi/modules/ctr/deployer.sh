#!/usr/bin/env bash

REGION=$1
DEPT=$2
CLIENT=$3
ENV=$(echo $4 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
ENV_UPPER=$(echo ${ENV} | awk '{print toupper($0)}')
ENV_LOWER=$(echo ${ENV} | awk '{print tolower($0)}')

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
    region=$1
    stack=$2
    resource=$3
    output=$(aws cloudformation --region ${region} describe-stack-resources --stack-name ${stack} 2> /dev/null)

    if [[ ${output} == *"${resource}"* ]]; then
        exists="true"
    else
        exists="false"
    fi
}

echo """
----------------------------------------------------
                   ctr solution
                   ------------

"""

# check is pre-requisite resources exist
resource_exists ${REGION} stCapita-MI-${ENV}-CrossAccountRole CrossAccountFirehoseRole
if [[ ${exists} == "true" ]]; then
    resource_cross_account_role="Available"
else
    resource_cross_account_role="Not available"
    resources_missing=" (resources missing)"
fi

bucket_exists s3-capita-ccm-connect-${CLIENT}-${ENV_LOWER}-${REGION}-reporting
if [[ ${exists} == "true" ]]; then
    resource_reporting_bucket="Available"
else
    resource_reporting_bucket="Not available"
    resources_missing=" (resources missing)"
fi


echo """

Pre-requisites${resources_missing}:

    Cross Account Role        : ${resource_cross_account_role}
    Customer Reporting Bucket : ${resource_reporting_bucket}

"""

if [[ ! -z ${resources_missing} ]]; then
    echo "Aborting, pre-requisites missing"
    exit
fi


echo """

               Deploying CTR resources
               -----------------------

"""

cf sync -y --context ${DIRECTORY}/../../transforms/config-customer-deployer.yml \
   ${DIRECTORY}/ctr-resources.stacks


echo """

               Update the CTR Firehose
               -----------------------

"""

aws lambda --region ${REGION} invoke --function-name lmbMiFirehoseModder-${DEPT}-${ENV_UPPER} \
                  --payload "{
  \"debug\": true,
  \"ResourceProperties\": {
    \"FirehoseName\": \"kfh-${DEPT}-ctr-${ENV_LOWER}\",
    \"Prefix\": \"contact_record/clientname=${CLIENT}/rowdate=!{timestamp:yyyy-MM-dd}/\",
    \"ErrorPrefix\": \"errors/contact_record/!{firehose:error-output-type}/clientname=${CLIENT}/rowdate=!{timestamp:yyyy-MM-dd}/\",
    \"TransformationDb\": \"gl_${DEPT}_${ENV_LOWER}\",
    \"TransformationTable\": \"glt_ctr_${ENV_LOWER}\",
    \"TransformationRole\": \"rl_mi_ctr_${ENV_LOWER}\"
  }
}" result.txt


python ${DIRECTORY}/../../scripts/tag-firehose.py -r ${REGION} -f kfh-${DEPT}-ctr-${ENV_LOWER} \
                    -t sec:Compliance:PII bus:BusinessUnit:${DEPT} bus:ClientName:${CLIENT} \
                       tech:Environment:${ENV_LOWER} tech:ApplicationID:capita-${DEPT}-connect \
                       tech:ApplicationRole:reporting



rm result.txt

echo """

                  ctr solution: complete
----------------------------------------------------

"""
