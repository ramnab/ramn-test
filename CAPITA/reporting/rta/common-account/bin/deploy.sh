#!/usr/bin/env bash

# Ensure you are in the target account before running this script
# by using a tool such as 'awsume'

DEPARTMENT=$(echo $1 | awk '{print tolower($0)}')
ENV=$(echo $2 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
REGION="eu-central-1"

if [[ -z "${ENV}" ]] || [[ -z "${DEPARTMENT}" ]]; then
    echo "
Usage:

    ./bin/deploy.sh DEPARTMENT  ENV
    
where ENV is the environment, e.g. 'dev', 'test', 'prod'

** IMPORTANT: You need to switch to the target account
using a tool such as awsume before running this script **

"
    exit
fi
DIRECTORY=`dirname $0`

getStackOutput () {
    STACKNAME=$1
    KEY=$2
    aws cloudformation describe-stacks --region ${REGION} --query "Stacks[?StackName == '${STACKNAME}'].Outputs[]| [?OutputKey=='${KEY}'].[OutputValue] | [0]" --output text
}

ENV_UPPER=$(echo ${ENV} | awk '{print toupper($0)}')
ENV_LOWER=$(echo ${ENV} | awk '{print tolower($0)}')
STACK="${DIRECTORY}/../deploy-${ENV_LOWER}.stacks"
ACCOUNT_ALIAS=$(aws iam list-account-aliases --query "AccountAliases | [0]" --output text)

echo """
        Deploy RTA into Common
    ----------------------------

    Account:    ${ACCOUNT_ALIAS}
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


LAMBDA_S3=$(getStackOutput stCapita-RTA-${ENV}-AccountSetup oLambdaDeploymentBucketArn | sed -e 's/arn.*:::\(.*\)/\1/')
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

aws cloudformation package --region ${REGION} \
                           --template-file ${DIRECTORY}/../templates/verify.yml \
                           --s3-bucket ${LAMBDA_S3} \
                           --output-template-file deploy-verify.yml

aws cloudformation deploy --region ${REGION} --template-file deploy-verify.yml \
                          --stack-name stCapita-RTA-${ENV}-Verify  \
                          --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
                          --parameter-overrides \
                                pAlarmConfigFilePath=config/alarm_config.json \
                                pOutputFilePath=processed/agent_schedule.json \
                                pDepartment=${DEPARTMENT} \
                                pEnvironment=${ENV_UPPER} \
                                pEnvironmentLowerCase=${ENV_LOWER}

rm deploy-verify.yml

# e.g. "s3-capita-ccm-common-test-rta-agentschedules"
AGENT_S3=$(getStackOutput stCapita-RTA-${ENV}-Verify oRtaScheduleBucketName)
TOPIC=$(getStackOutput stCapita-RTA-${ENV}-Verify  oSnsTopicArn)
KMS_KEY_ID=$(getStackOutput stCapita-RTA-${ENV}-Kms oMasterKeyArn)

echo "Uploading alarm_config.json to s3://${AGENT_S3}/config/"
aws s3 cp ${DIRECTORY}/../config/alarm_config.json s3://${AGENT_S3}/config/


echo """
----------------------------------
          Deploying RTA

"""

aws cloudformation package --region ${REGION} \
                           --template-file ${DIRECTORY}/../templates/rta.yml \
                           --s3-bucket ${LAMBDA_S3} \
                           --output-template-file deploy-rta.yml

aws cloudformation deploy --region ${REGION} --template-file deploy-rta.yml \
                          --stack-name stCapita-RTA-${ENV}-App  \
                          --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
                          --parameter-overrides \
                                pAgentSchedule=s3://${AGENT_S3}/processed/agent_schedule.json \
                                pEnvironment=${ENV_UPPER} \
                                pEnvironmentLowerCase=${ENV_LOWER} \
                                pSchedule="cron(0/1 5-21 * * ? *)" \
                                pKmsKeyId=${KMS_KEY_ID}

rm deploy-rta.yml

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

aws cloudformation package --region ${REGION} \
                           --template-file ${DIRECTORY}/../templates/api.yml \
                           --s3-bucket ${LAMBDA_S3} --output-template-file deploy-api.yml

aws cloudformation deploy --region ${REGION} --template-file deploy-api.yml \
                          --stack-name stCapita-RTA-${ENV}-Api --capabilities CAPABILITY_IAM \
                          --parameter-overrides pUserPoolArn=${COGNITO_ARN} \
                                                pEnvironment=${ENV_UPPER} \
                                                pEnvironmentLowerCase=${ENV_LOWER} \
                                                pRtaAlarmsDb=${ALARM_DB} \
                                                pRtaAlarmsDbArn=${ALARM_DB_ARN}

rm deploy-api.yml

API=$(getStackOutput stCapita-RTA-${ENV}-Api oRtaApi)

if [[ ${API} = "None" ]]; then
    echo "Unable to find API in stack stCapita-RTA-${ENV}-Api"
    exit
fi

echo """
----------------------------------
    Deploying HealthChecker

"""

aws cloudformation package --region ${REGION} \
                           --template-file templates/health.yml \
                           --s3-bucket s3-capita-${DEPARTMENT}-connect-common-${ENV_LOWER}-lambdas-${REGION} \
                           --output-template-file deploy-health.yml

aws cloudformation deploy --region ${REGION} --template-file deploy-health.yml \
                          --stack-name stCapita-RTA-${ENV}-Health  \
                          --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
                          --parameter-overrides \
                                pDepartment=${DEPARTMENT} \
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



WEB_S3=$(getStackOutput stCapita-RTA-${ENV}-CDN oWebAppBucketArn | sed -e 's/arn.*:::\(.*\)/s3:\/\/\1\//')

echo """
----------------------------------
       Uploading HTML to S3

       Bucket: ${WEB_S3}
"""


aws s3 sync html/. ${WEB_S3}

DOMAIN=$(getStackOutput stCapita-RTA-${ENV}-CDN oWebAppDomainName)


echo """

Deployment Completed:

    https://${DOMAIN}

"""
