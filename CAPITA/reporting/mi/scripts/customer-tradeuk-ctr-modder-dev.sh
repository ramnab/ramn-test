#!/bin/bash

aws cloudformation package --region eu-central-1 --template-file modules/base-customer/resources/fh-modder.yml \
                           --s3-bucket s3-capita-ccm-tradeuk-nonprod-lambdas-eu-central-1 \
                           --output-template-file deploy-fh-modder.yml

# deploy for CAPITA DEV
aws cloudformation deploy --region eu-central-1 --template-file deploy-fh-modder.yml \
                          --stack-name stCapita-MI-Dev-FirehoseModder  \
                          --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
                          --parameter-overrides \
                                pClient=tradeuk \
                                pEnvironment=DEV \
                                pEnvironmentLowerCase=dev \
                                pDepartment=ccm
