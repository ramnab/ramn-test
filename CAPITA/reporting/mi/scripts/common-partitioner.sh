#!/bin/bash

ENV=$(echo $1 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
ENV_UPPER=$(echo $1 | awk '{print toupper($0)}')
ENV_LOWER=$(echo $1 | awk '{print tolower($0)}')


aws cloudformation package --region eu-central-1 --template-file modules/base-common/resources/partitioner.yml \
                           --s3-bucket s3-capita-ccm-connect-common-$ENV_LOWER-lambdas-eu-central-1 \
                           --output-template-file deploy-partitioner.yml

# deploy for CAPITA DEV
aws cloudformation deploy --region eu-central-1 --template-file deploy-partitioner.yml \
                          --stack-name stCapita-MI-$ENV-Partitioner  \
                          --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
                          --parameter-overrides \
                                pEnvironment=$ENV_UPPER \
                                pEnvironmentLowerCase=$ENV_LOWER \
                                pDepartment=ccm \
                                pClients=tradeuk \
                                pGlueDb=ccm_connect_reporting_$ENV_LOWER \
                                pTables=agent_interval,contact_record,queue_interval \
                                pCommonReportingBucket=s3-capita-ccm-connect-common-$ENV_LOWER-reporting
