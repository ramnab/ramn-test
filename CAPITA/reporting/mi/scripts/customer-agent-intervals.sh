#!/bin/bash


if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: customer-agent-intervals.sh <CLIENT> <ENV>"
    exit
fi

CLIENT=$1
ENV=$(echo $2 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
ENV_UPPER=$(echo $2 | awk '{print toupper($0)}')
ENV_LOWER=$(echo $2 | awk '{print tolower($0)}')

echo "Deploying to client $CLIENT, env $ENV_UPPER"

aws cloudformation package --region eu-central-1 --template-file modules/base-customer/resources/agent-intervals.yml \
                           --s3-bucket s3-capita-ccm-tradeuk-nonprod-lambdas-eu-central-1 \
                           --output-template-file deploy-agent-intervals.yml

aws cloudformation deploy --region eu-central-1 --template-file deploy-agent-intervals.yml \
                          --stack-name stCapita-MI-$ENV-AgentIntervals  \
                          --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
                          --parameter-overrides \
                                pClient=$CLIENT \
                                pEnvironment=$ENV_UPPER \
                                pEnvironmentLowerCase=$ENV_LOWER \
                                pDepartment=ccm \
                                pTransformationDb=gl_ccm_$ENV_LOWER \
                                pCommonDestination=s3-capita-ccm-connect-common-$ENV_LOWER-reporting \
                                pCustomerReportBucket=s3-capita-ccm-connect-$CLIENT-$ENV_LOWER-reporting

