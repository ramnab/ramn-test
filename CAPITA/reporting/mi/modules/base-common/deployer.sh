#!/usr/bin/env bash

DEPT=$1
ENV=$(echo $2 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
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

LAMBDA_S3="s3-capita-ccm-connect-common-${ENV_LOWER}-lambdas-eu-central-1"



echo """

         Deploying Athena Partitioner
         ----------------------------

"""

aws cloudformation package --region eu-central-1 \
                          --template-file ${DIRECTORY}/resources/partitioner.yml \
                           --s3-bucket ${LAMBDA_S3} \
                           --output-template-file deploy-partitioner.yml

aws cloudformation deploy --region eu-central-1 --template-file deploy-partitioner.yml \
                          --stack-name stCapita-MI-${ENV}-Partitioner  \
                          --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
                          --parameter-overrides \
                                pEnvironment=${ENV_UPPER} \
                                pEnvironmentLowerCase=${ENV_LOWER} \
                                pDepartment=${DEPT} \
                                pClients=tradeuk \
                                pGlueDb=ccm_connect_reporting_${ENV_LOWER} \
                                pTables=agent_interval,contact_record,queue_interval,agent_daily,queue_daily \
                                pCommonReportingBucket=s3-capita-${DEPT}-connect-common-${ENV_LOWER}-reporting

rm deploy-partitioner.yml


