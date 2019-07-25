#!/usr/bin/env bash

REGION=$1
DEPT=$2
ENV=$(echo $3 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
ENV_UPPER=$(echo ${ENV} | awk '{print toupper($0)}')
ENV_LOWER=$(echo ${ENV} | awk '{print tolower($0)}')
DIRECTORY=$(dirname $0)


echo """
----------------------------------------------------
                   base-common
                   -----------

"""

echo """

    Creating/Updating Common Reporting Bucket
    ------------------------------------------

"""

cf sync -y --context ${DIRECTORY}/../../transforms/config-common-deployer.yml \
                     ${DIRECTORY}/common-reporting-bucket.stacks



echo """

                Setting up Athena
                -----------------

"""

python ${DIRECTORY}/../../scripts/create-athena-workgroups.py ${DEPT} ${ENV}


if [[ ! $? -eq 0 ]]; then
    echo "Unable to create/update athena workgroups... aborting"
    exit
fi

cf sync -y --context ${DIRECTORY}/../../transforms/config-common-deployer.yml \
                     ${DIRECTORY}/athena.stacks


function create_bucket_if_not_exist {
    aws s3api head-bucket --bucket $2
    if [[ ! $? -eq 0 ]]; then
        echo "Creating new lambda distro bucket: $2 in region $1"
        aws s3 --region $1 mb s3://$2
    fi
}
LAMBDA_S3="s3-capita-${DEPT}-connect-common-${ENV_LOWER}-lambdas-${REGION}"
create_bucket_if_not_exist ${REGION} ${LAMBDA_S3}


echo """

         Deploying Athena Partitioner
         ----------------------------

"""

REPORTING_BUCKET="s3-capita-${DEPT}-connect-common-${ENV_LOWER}-reporting"
if [[ ${REGION} != "eu-central-1" ]]; then
    REPORTING_BUCKET="s3-capita-${DEPT}-connect-common-${ENV_LOWER}-reporting-${REGION}"
fi

aws cloudformation package --region ${REGION} \
                           --template-file ${DIRECTORY}/resources/partitioner.yml \
                           --s3-bucket ${LAMBDA_S3} \
                           --output-template-file deploy-partitioner.yml

aws cloudformation deploy --region ${REGION} --template-file deploy-partitioner.yml \
                          --stack-name stCapita-MI-${ENV}-Partitioner  \
                          --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
                          --parameter-overrides \
                                pEnvironment=${ENV_UPPER} \
                                pEnvironmentLowerCase=${ENV_LOWER} \
                                pDepartment=${DEPT} \
                                pClients=tradeuk,gassafe \
                                pGlueDb=ccm_connect_reporting_${ENV_LOWER} \
                                pTables=agent_interval,contact_record,queue_interval,agent_daily,queue_daily,agent_events \
                                pCommonReportingBucket=${REPORTING_BUCKET}

rm deploy-partitioner.yml


