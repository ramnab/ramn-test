#!/bin/bash

CLIENT=$1
ENV=$(echo $2 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
ENV_UPPER=$(echo $2 | awk '{print toupper($0)}')
ENV_LOWER=$(echo $2 | awk '{print tolower($0)}')

if [ $ENV_LOWER = "prod" ]; then
    LAMBDA_S3=s3-capita-ccm-$CLIENT-prod-lambdas-eu-central-1
else
    LAMBDA_S3=s3-capita-ccm-$CLIENT-nonprod-lambdas-eu-central-1
fi

echo "Deploying to client $CLIENT, env $ENV_UPPER"

aws cloudformation package --region eu-central-1 --template-file modules/base-customer/resources/customer-reporting-modder.yml \
                           --s3-bucket $LAMBDA_S3 \
                           --output-template-file deploy-customer-reporting-modder.yml

# deploy for CAPITA DEV
aws cloudformation deploy --region eu-central-1 --template-file deploy-customer-reporting-modder.yml \
                          --stack-name stCapita-MI-$ENV-ReportingBucketModder  \
                          --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
                          --parameter-overrides \
                                pClient=$CLIENT \
                                pEnvironment=$ENV_UPPER \
                                pEnvironmentLowerCase=$ENV_UPPER \
                                pDepartment=ccm \
                                pCustomerReportingBucketArn=arn:aws:s3:::s3-capita-ccm-connect-$CLIENT-$ENV_LOWER-reporting
