#!/bin/bash

aws cloudformation package --region eu-central-1 --template-file modules/base-common/resources/athena.yml \
                           --s3-bucket s3-capita-ccm-common-dev-lambdas-eu-central-1 \
                           --output-template-file deploy-athena.yml

# deploy for CAPITA DEV
aws cloudformation deploy --region eu-central-1 --template-file deploy-athena.yml \
                          --stack-name stCapita-MI-Dev-Athena  \
                          --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
                          --parameter-overrides \
                                pEnvironment=DEV \
                                pEnvironmentLowerCase=dev \
                                pDepartment=ccm
