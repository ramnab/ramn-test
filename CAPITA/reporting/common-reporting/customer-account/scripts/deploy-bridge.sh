#!/bin/bash


if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: deploy-bridge.sh <CLIENT> <ENV>"
    exit
fi

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
echo "Currently the source and target streams are hardcoded... "

aws cloudformation package --region eu-central-1 --template-file templates/bridge.yml \
                           --s3-bucket $LAMBDA_S3 \
                           --output-template-file deploy-bridge.yml

aws cloudformation deploy --region eu-central-1 --template-file deploy-bridge.yml \
                          --stack-name stCapita-RTA-$ENV-Bridge  \
                          --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
                          --parameter-overrides \
                                pClient=$CLIENT \
                                pEnvironment=$ENV_UPPER \
                                pEnvironmentLowerCase=$ENV_LOWER \
                                pDepartment=ccm \
                                pCommonAccountRoleArn=arn:aws:iam::049293504011:role/CA_RTA_TEST \
                                pTargetStreamName=ks-ccm-agent-events-test \
                                pTargetStreamArn=arn:aws:kinesis:eu-central-1:049293504011:stream/ks-ccm-agent-events-test \
                                pInputKinesisArn=arn:aws:kinesis:eu-central-1:443350248290:stream/ks-ccm-agent-events-prod

