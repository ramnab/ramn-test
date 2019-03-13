#!/bin/bash

ENV=$(echo $2 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
ENV_UPPER=$(echo $2 | awk '{print toupper($0)}')
ENV_LOWER=$(echo $2 | awk '{print tolower($0)}')

aws cloudformation package --region eu-central-1 --template-file modules/base-common/resources/athena.yml \
                           --s3-bucket s3-capita-ccm-common-$ENV_LOWER-lambdas-eu-central-1 \
                           --output-template-file deploy-athena.yml

# deploy for CAPITA DEV
aws cloudformation deploy --region eu-central-1 --template-file deploy-athena.yml \
                          --stack-name stCapita-MI-$ENV-Athena  \
                          --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
                          --parameter-overrides \
                                pEnvironment=$ENV_UPPER \
                                pEnvironmentLowerCase=$ENV_LOWER \
                                pDepartment=ccm
