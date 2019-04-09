#!/usr/bin/env bash

ENV=$(echo $1 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
ENV_UPPER=$(echo $1 | awk '{print toupper($0)}')
ENV_LOWER=$(echo $1 | awk '{print tolower($0)}')
DIRECTORY=`dirname $0`



echo """
----------------------------------------------------
                   base-common
                   -----------

"""

echo """

    Creating/Updating Common Reporting Bucket
    ------------------------------------------

"""


cf sync -y --context ${DIRECTORY}/../../transforms/config-ccm-common-${ENV_LOWER}.yml \
                     ${DIRECTORY}/common-reporting-bucket.stacks



echo """

                Setting up Athena
                -----------------

"""


python ${DIRECTORY}/../../scripts/create-athena-workgroups.py ccm ${ENV}


if [[ ! $? -eq 0 ]]; then
    echo "Unable to create/update athena workgroups... aborting"
    exit
fi

LAMBDA_S3="s3-capita-ccm-connect-common-${ENV_LOWER}-lambdas-eu-central-1"

aws cloudformation package --region eu-central-1 \
                           --template-file ${DIRECTORY}/resources/athena.yml \
                           --s3-bucket ${LAMBDA_S3} \
                           --output-template-file deploy-athena.yml

aws cloudformation deploy --region eu-central-1 --template-file deploy-athena.yml \
                          --stack-name stCapita-MI-${ENV}-Athena  \
                          --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
                          --parameter-overrides \
                                pEnvironment=${ENV_UPPER} \
                                pEnvironmentLowerCase=${ENV_LOWER} \
                                pDepartment=ccm \
                                pReportBucket=s3-capita-ccm-connect-common-${ENV_LOWER}-reporting \
                                pCtrLocation=contact_record/ \
                                pQILocation=queue_interval/ \
                                pQDailyLocation=queue_daily/ \
                                pQILocation=queue_daily/ \
                                pADailyLocation=agent_daily/

echo "cloudformation deploy returned $?"

rm deploy-athena.yml




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
                                pDepartment=ccm \
                                pClients=tradeuk \
                                pGlueDb=ccm_connect_reporting_${ENV_LOWER} \
                                pTables=agent_interval,contact_record,queue_interval,agent_daily,queue_daily \
                                pCommonReportingBucket=s3-capita-ccm-connect-common-${ENV_LOWER}-reporting

rm deploy-partitioner.yml


