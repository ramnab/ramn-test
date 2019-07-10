#!/bin/bash


if [[ -z "$1" ]] || [[ -z "$2" ]] || [[ -z "$3" ]] || [[ -z "$4" ]];  then
    echo "Usage: deploy-bridge.sh REGION DEPARTMENT CLIENT ENV"
    exit
fi

REGION=$1
DEPARTMENT=$(echo $2 | awk '{print tolower($0)}')
CLIENT=$(echo $3 | awk '{print tolower($0)}')
ENV=$(echo $4 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
ENV_UPPER=$(echo ${ENV} | awk '{print toupper($0)}')
ENV_LOWER=$(echo ${ENV} | awk '{print tolower($0)}')
DIRECTORY=`dirname $0`
LAMBDA_S3=s3-capita-${DEPARTMENT}-connect-${CLIENT}-${ENV_LOWER}-lambdas-${REGION}
ACCOUNT_ALIAS=$(aws iam list-account-aliases --query "AccountAliases | [0]" --output text)

COMMON_ACCOUNT_ID=049293504011 # nonprod
if [[ ${ENV_LOWER} == "prod" ]]; then
    COMMON_ACCOUNT_ID=808647995970  # prod
fi

# HARD-CODED SETTINGS - need to be checked before deployment
CA_ROLE="arn:aws:iam::${COMMON_ACCOUNT_ID}:role/CA_RTA_${ENV_UPPER}"

echo """

------------------------------------------------------
  Deploying Agent Events Bridge to Customer Account
  --------------------------------------------------

            Account:     ${ACCOUNT_ALIAS}
            Region:      ${REGION}
            Department:  ${DEPARTMENT}
            Client:      ${CLIENT}
            Environment: ${ENV_LOWER}

  Using defaults:
    common account ${ENV_LOWER}: ${COMMON_ACCOUNT_ID}
    common account role: ${CA_ROLE}

"""

read -p "> Continue? (y/n) " cont
if [[ ${cont} != "y" ]]; then
    echo "Aborting..."
    exit
fi


aws cloudformation package --region ${REGION} --template-file ${DIRECTORY}/../templates/bridge.yml \
                           --s3-bucket ${LAMBDA_S3} \
                           --output-template-file deploy-bridge.yml

aws cloudformation deploy --region ${REGION} --template-file deploy-bridge.yml \
                          --stack-name stCapita-RTA-${ENV}-Bridge  \
                          --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
                          --parameter-overrides \
                                pClientName=${CLIENT} \
                                pEnvironment=${ENV} \
                                pEnvironmentLowerCase=${ENV_LOWER} \
                                pDepartment=${DEPARTMENT} \
                                pCommonAccountRoleArn=${CA_ROLE} \
                                pTargetStreamName=ks-${DEPARTMENT}-agent-events-${ENV_LOWER} \
                                pTargetStreamArn=arn:aws:kinesis:${REGION}:${COMMON_ACCOUNT_ID}:stream/ks-${DEPARTMENT}-agent-events-${ENV_LOWER} \
                                pInputStreamName=ks-ccm-agent-events-${ENV_LOWER}

echo "Deployment success code: $?"

rm deploy-bridge.yml
ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)

echo """

Agent Events Bridge Deployed!

connect instance
    -> ks-ccm-agent-events-${ENV_LOWER} 
    -> lmbRTA-Bridge-${DEPARTMENT}-${ENV} 
    -> [Common ${ENV}] ks-${DEPARTMENT}-agent-events-${ENV_LOWER}


Ensure role CA_RTA_${ENV_UPPER} in Common ${ENV} trusts account: ${ACCOUNT_ID}

"""
