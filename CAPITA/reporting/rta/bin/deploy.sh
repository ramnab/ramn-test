#!/usr/bin/env bash

PROFILE=$1
ENV=$2


if [ -z "$ENV" ]; then
    echo "
Usage:

    ./bin/deploy.sh  ENV
    
where ENV is the environment, e.g. 'Dev', 'Test', 'Prod'
(note the capitalisation)

You need to switch to the target role using a tool such as 
awsume before running this script

"
    exit
fi


awsume $PROFILE
aws s3 ls



getStackOutput () {
    STACKNAME=$1
    KEY=$2
    # echo "getStackOutput security token=${AWS_SECURITY_TOKEN}"
    aws cloudformation describe-stacks --query "Stacks[?StackName == '$STACKNAME'].Outputs[]| [?OutputKey=='$KEY'].[OutputValue] | [0]" --output text
}


ENV_UPPER=`echo $2 | awk '{print toupper($0)}'`
ENV_LOWER=`echo $2 | awk '{print tolower($0)}'`
STACK="deploy-$ENV_LOWER.stacks"

echo "Switched to account: $AWSUME_PROFILE"
echo "Working directory" `pwd`
echo "Deploying Infrastructure stack as defined in $STACK"

cf sync -y -n $STACK

echo "-----------------------"
echo "Deploying API"

LAMBDA_S3=`aws cloudformation describe-stacks --query "Stacks[?StackName == 'stCapita-RTA-$ENV-AccountSetup'].Outputs[]| [?OutputKey=='oLambdaDeploymentBucketArn'].[OutputValue] | [0]" --output text | sed -e 's/arn.*:::\(.*\)/\1/'`
COGNITO_ARN=`getStackOutput stCapita-RTA-$ENV-IdentityManagement oUserPoolArn`                       #`aws cloudformation describe-stacks --query "Stacks[?StackName == 'stCapita-RTA-$ENV-IdentityManagement'].Outputs[]| [?OutputKey=='oUserPoolArn'].[OutputValue] | [0]" --output text`
USERPOOLCLIENTID=`getStackOutput stCapita-RTA-$ENV-IdentityManagement oUserPoolClientId`             #`aws cloudformation describe-stacks --query "Stacks[?StackName == 'stCapita-RTA-$ENV-IdentityManagement'].Outputs[]| [?OutputKey=='oUserPoolClientId'].[OutputValue] | [0]" --output text`
USERPOOLID=`getStackOutput stCapita-RTA-$ENV-IdentityManagement oUserPoolId`                         #`aws cloudformation describe-stacks --query "Stacks[?StackName == 'stCapita-RTA-$ENV-IdentityManagement'].Outputs[]| [?OutputKey=='oUserPoolId'].[OutputValue] | [0]" --output text`

#getStackOutput stCapita-RTA-$ENV-IdentityManagement oUserPoolArn
echo $USERPOOLCLIENTID
exit
if [ $LAMBDA_S3 = "None" ] || [ $COGNITO_ARN = "None" ] || [ $USERPOOLCLIENTID = "None"] || [ $USERPOOLID = "None"]; then
    echo "Parameters are missing; aborting deployment"
    echo "LAMBDA_S3: $LAMBDA_S3"
    echo "COGNITO_ARN: $COGNITO_ARN"
    echo "USERPOOLCLIENTID: $USERPOOLCLIENTID"
    echo "USERPOOLID: $USERPOOLID"
    exit
fi

# aws cloudformation package --region eu-central-1 --template-file templates/api.yml \
#     --s3-bucket $LAMBDA_S3 --output-template-file deploy.yml

# aws cloudformation deploy --region eu-central-1 --template-file deploy.yml \
#     --stack-name stCapita-RTA-$ENV-Api --capabilities CAPABILITY_IAM \
#     --parameter-overrides pUserPoolArn=$COGNITO_ARN  \
#                           pEnvironment=$ENV_UPPER \
#                           pEnvironmentLowerCase=$ENV_LOWER

API=`getStackOutput stCapita-RTA-$ENV-Api oRtaApi` #`aws cloudformation describe-stacks --query "Stacks[?StackName == 'stCapita-RTA-$ENV-Api'].Outputs[]| [?OutputKey=='oRtaApi'].[OutputValue] | [0]" --output text`

if [ $API = "None" ]; then
    echo "Unable to find API in stack stCapita-RTA-$ENV-Api"
    exit
fi

cat > html/js/config.js << EOF
window._config = {
    cognito: {
        userPoolId: '$USERPOOLID',
        userPoolClientId: '$USERPOOLCLIENTID', 
        region: 'eu-central-1'
    },
    api: {
        invokeUrl: 'https://$API.execute-api.eu-central-1.amazonaws.com/prod/rta'
    }
};
EOF


WEB_S3=`aws cloudformation describe-stacks --query "Stacks[?StackName == 'stCapita-RTA-$ENV-CDN'].Outputs[]| [?OutputKey=='oWebAppBucketArn'].[OutputValue] | [0]" --output text | sed -e 's/arn.*:::\(.*\)/s3:\/\/\1\//'`
echo "Uploading to $WEB_S3"
# aws s3 sync html/. $WEB_S3

awsume

