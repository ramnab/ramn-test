#!/usr/bin/env bash

# Ensure you are in the target account before running this script
# by using a tool such as 'awsume'

ENV=$(echo $1 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
CLIENT=$2

if [ -z "$ENV" ]; then
    echo "
Usage:

    ./bin/deploy.sh  ENV CLIENT
    
where ENV is the environment, e.g. 'Dev', 'Test', 'Prod'
(note the capitalisation)

and CLIENT is the client identifier, such as 'tradeuk'

** IMPORTANT: You need to switch to the target account
using a tool such as awsume before running this script **

"
    exit
fi

getStackOutput () {
    STACKNAME=$1
    KEY=$2
    # echo "getStackOutput security token=${AWS_SECURITY_TOKEN}"
    aws cloudformation describe-stacks --query "Stacks[?StackName == '$STACKNAME'].Outputs[]| [?OutputKey=='$KEY'].[OutputValue] | [0]" --output text
}

# ENV_UPPER=$(echo $1 | awk '{print toupper($0)}')
# ENV_LOWER=`echo $1 | awk '{print tolower($0)}'`


echo "Running into account: $AWSUME_PROFILE"
echo "Client ID: $CLIENT"
echo "Environment: $ENV"

echo ""
read -p "Continue? (y/n) " cont
if [ $cont != "y" ]; then
    echo "Aborting..."
    exit
fi
echo ""
echo "------------------------------------------"
echo "Deploying reporting stack (SAM)"


LAMBDA_S3=s3-capita-ccm-tradeuk-nonprod-lambdas-eu-central-1
echo "Lambda bucket=$LAMBDA_S3"

aws cloudformation package --region eu-central-1 --template-file templates/reporting.yml \
                           --s3-bucket $LAMBDA_S3 \
                           --output-template-file deploy-reporting.yml

aws cloudformation deploy --region eu-central-1 --template-file deploy-reporting.yml \
                          --stack-name stCapita-MI-$ENV-Reporting  \
                          --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
                          --parameter-overrides \
                                pClient=$CLIENT \
                                pAgentReportDestinationArn=arn:aws:s3:::s3-capita-ccm-connect-common-$ENV_LOWER-reporting \
                                pQueueReportDestinationArn=arn:aws:s3:::s3-capita-ccm-connect-common-$ENV_LOWER-reporting \
                                pEnvironment=DEV \
                                pEnvironmentLowerCase=dev \
                                pDepartment=ccm \
                                pCustomUpdateToken=1

echo ""
echo "------------------------------------------"
echo "Deploying CTR stack (cfn sq)"

cf sync -y deploy-$ENV_LOWER.stacks


