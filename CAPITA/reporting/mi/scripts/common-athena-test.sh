#!/bin/bash

aws cloudformation package --region eu-central-1 --template-file modules/base-common/resources/athena.yml \
                           --s3-bucket s3-capita-ccm-common-test-lambdas-eu-central-1 \
                           --output-template-file deploy-athena.yml

# deploy for CAPITA DEV
aws cloudformation deploy --region eu-central-1 --template-file deploy-athena.yml \
                          --stack-name stCapita-MI-Test-Athena  \
                          --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
                          --parameter-overrides \
                                pEnvironment=TEST \
                                pEnvironmentLowerCase=test \
                                pDepartment=ccm
