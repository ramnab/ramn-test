#!/usr/bin/env bash

# Ensure you are in the target account before running this script
# by using a tool such as 'awsume'

ENV=$(echo $1 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')

if [[ -z "${ENV}" ]]; then
    echo "
Usage:

    ./bin/deploy.sh  ENV
    
where ENV is the environment, e.g. 'Dev', 'Test', 'Prod'
(note the capitalisation)

** IMPORTANT: You need to switch to the target account
using a tool such as awsume before running this script **

"
    exit
fi

getStackOutput () {
    STACKNAME=$1
    KEY=$2
    # echo "getStackOutput security token=${AWS_SECURITY_TOKEN}"
    aws cloudformation describe-stacks --query "Stacks[?StackName == '${STACKNAME}'].Outputs[]| [?OutputKey=='${KEY}'].[OutputValue] | [0]" --output text
}

ENV_UPPER=$(echo $1 | awk '{print toupper($0)}')
ENV_LOWER=$(echo $1 | awk '{print tolower($0)}')
STACK="deploy-${ENV_LOWER}.stacks"

echo """
    Deploy RTA into Common ${ENV}
    -----------------------------

    Account:    ${AWSUME_PROFILE}
    Environ:    ${ENV}

"""

read -p "Continue? (y/n) " cont
if [[ ${cont} != "y" ]]; then
    echo "Aborting..."
    exit
fi
echo """
----------------------------------
      Deploying Baseline:

        - Account setup
        - Identity management
        - CDN

"""

cf sync -y ${STACK}


LAMBDA_S3=$(aws cloudformation describe-stacks --query "Stacks[?StackName == 'stCapita-RTA-${ENV}-AccountSetup'].Outputs[]| [?OutputKey=='oLambdaDeploymentBucketArn'].[OutputValue] | [0]" --output text | sed -e 's/arn.*:::\(.*\)/\1/')
COGNITO_ARN=$(getStackOutput stCapita-RTA-${ENV}-IdentityManagement oUserPoolArn)
USERPOOLCLIENTID=$(getStackOutput stCapita-RTA-${ENV}-IdentityManagement oUserPoolClientId)
USERPOOLID=$(getStackOutput stCapita-RTA-${ENV}-IdentityManagement oUserPoolId)


if [[ ${LAMBDA_S3} = "None" ]] || [[ ${COGNITO_ARN} = "None" ]] || [[ ${USERPOOLCLIENTID} = "None" ]] || [[ ${USERPOOLID} = "None" ]]; then
    echo """

* Aborting, missing parameters:

     - LAMBDA_S3:        ${LAMBDA_S3}
     - COGNITO_ARN:      ${COGNITO_ARN}
     - USERPOOLCLIENTID: ${USERPOOLCLIENTID}
     - USERPOOLID:       ${USERPOOLID}

"""
    exit
fi

echo """
----------------------------------
       Deploying Verify

"""

aws cloudformation package --region eu-central-1 --template-file templates/verify.yml \
                           --s3-bucket ${LAMBDA_S3} \
                           --output-template-file deploy-verify.yml

aws cloudformation deploy --region eu-central-1 --template-file deploy-verify.yml \
                          --stack-name stCapita-RTA-${ENV}-Verify  \
                          --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
                          --parameter-overrides \
                                pAlarmConfigFilePath=config/alarm_config.json \
                                pOutputFilePath=processed/agent_schedule.json \
                                pDepartment=ccm \
                                pEnvironment=${ENV_UPPER} \
                                pEnvironmentLowerCase=${ENV_LOWER}

rm deploy-verify.yml

# e.g. "s3-capita-ccm-common-test-rta-agentschedules"
AGENT_S3=$(getStackOutput stCapita-RTA-${ENV}-Verify oRtaScheduleBucketName)
TOPIC=$(getStackOutput stCapita-RTA-${ENV}-Verify  oSnsTopicArn)

echo """
----------------------------------
          Deploying RTA

"""

aws cloudformation package --region eu-central-1 --template-file templates/rta.yml \
                           --s3-bucket ${LAMBDA_S3} \
                           --output-template-file deploy-rta.yml

aws cloudformation deploy --region eu-central-1 --template-file deploy-rta.yml \
                          --stack-name stCapita-RTA-${ENV}-App  \
                          --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
                          --parameter-overrides \
                                pAgentSchedule=s3://${AGENT_S3}/processed/agent_schedule.json \
                                pEnvironment=${ENV_UPPER} \
                                pEnvironmentLowerCase=${ENV_LOWER} \
                                pSchedule="cron(0/1 5-21 * * ? *)"


echo """
----------------------------------
         Deploying API

"""

ALARM_DB=$(getStackOutput stCapita-RTA-${ENV}-App oRtaAlarmsDb)
ALARM_DB_ARN=$(getStackOutput stCapita-RTA-${ENV}-App oRtaAlarmsDbArn)

if [[ ${ALARM_DB} = "None" ]] || [[ ${ALARM_DB_ARN} = "None" ]]; then
    echo "Unable to find reference to the alarms db"
    exit
fi

aws cloudformation package --region eu-central-1 --template-file templates/api.yml \
                           --s3-bucket ${LAMBDA_S3} --output-template-file deploy-api.yml

aws cloudformation deploy --region eu-central-1 --template-file deploy-api.yml \
                          --stack-name stCapita-RTA-${ENV}-Api --capabilities CAPABILITY_IAM \
                          --parameter-overrides pUserPoolArn=${COGNITO_ARN} \
                                                pEnvironment=${ENV_UPPER} \
                                                pEnvironmentLowerCase=${ENV_LOWER} \
                                                pRtaAlarmsDb=${ALARM_DB} \
                                                pRtaAlarmsDbArn=${ALARM_DB_ARN}

API=$(getStackOutput stCapita-RTA-${ENV}-Api oRtaApi)

if [[ ${API} = "None" ]]; then
    echo "Unable to find API in stack stCapita-RTA-${ENV}-Api"
    exit
fi

echo """
----------------------------------
    Deploying HealthChecker

"""

aws cloudformation package --region eu-central-1 --template-file templates/health.yml \
                           --s3-bucket s3-capita-ccm-connect-common-${ENV_LOWER}-lambdas-eu-central-1 \
                           --output-template-file deploy-health.yml

aws cloudformation deploy --region eu-central-1 --template-file deploy-health.yml \
                          --stack-name stCapita-RTA-${ENV}-Health  \
                          --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
                          --parameter-overrides \
                                pDepartment=ccm \
                                pEnvironment=${ENV_UPPER} \
                                pEnvironmentLowerCase=${ENV_LOWER} \
                                pCronExpression="cron(0/15 6-21 * * ? *)" \
                                pTopic=${TOPIC}

rm deploy-health.yml


cat > html/js/config.js << EOF
window._config = {
    cognito: {
        userPoolId: "${USERPOOLID}",
        userPoolClientId: "${USERPOOLCLIENTID}",
        region: "eu-central-1"
    },
    api: {
        invokeUrl: "https://${API}.execute-api.eu-central-1.amazonaws.com/prod/rta"
    },
    env: "${ENV_LOWER}"
};
EOF



WEB_S3=$(aws cloudformation describe-stacks --query "Stacks[?StackName == 'stCapita-RTA-${ENV}-CDN'].Outputs[]| [?OutputKey=='oWebAppBucketArn'].[OutputValue] | [0]" --output text | sed -e 's/arn.*:::\(.*\)/s3:\/\/\1\//')

echo """
----------------------------------
       Uploading HTML

       S3: ${WEB_S3}
"""


aws s3 sync html/. ${WEB_S3}

echo """

Deployment Completed
"""
