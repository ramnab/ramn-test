#!/usr/bin/env bash

REGION=$1
DEPT=$(echo $2 | awk '{print tolower($0)}')
DEPT_UPPER=$(echo "${DEPT}" | awk '{print toupper($0)}')
CLIENT=$3
ENV=$(echo $4 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
ENV_LOWER=$(echo ${ENV} | awk '{print tolower($0)}')
DIRECTORY=$(dirname $0)
SSM_PARAMETER="ConnectIPs"
EMAIL_ADDRESS="DL-CCM-AWSCONNECTTEAM@capita.co.uk"

die2() { echo >&2 -e "\nERROR: $@\n"; exit 1; }
run() { "$@"; code=$?; [[ ${code} -ne 0 ]] && die2 "command [$*] failed with error code $code"; }


echo """
----------------------------------------------------
                Setting up Lambda IP Range notifier
                ---------------------

        Deploying:
            - Lambda Function to notify of ip range changes
            - SNS topic
            - SNS subscription

"""

LAMBDA_S3=s3-capita-ccm-connect-${CLIENT}-${ENV_LOWER}-lambdas-${REGION}

#Install dependencies
echo "my directory is ${DIRECTORY}"

(cd "${DIRECTORY}"/resources/code && pip install -r requirements.txt -t .)
if [ $? -gt 0 ]; then
  echo "Deployment didn't succeed, exiting"
  exit 1
fi

aws cloudformation package --region ${REGION} \
                           --template-file ${DIRECTORY}/resources/aws-ip-changed.yml \
                           --s3-bucket ${LAMBDA_S3} \
                           --output-template-file aws-ip-changed-sam.yml

aws cloudformation deploy --region ${REGION} --template-file aws-ip-changed-sam.yml \
                          --stack-name stCapita-"${DEPT_UPPER}"-Connect-IP-Change-Notifier  \
                          --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
                          --parameter-overrides pEmailEndpoint=${EMAIL_ADDRESS} \
                          pSsmParameter=${SSM_PARAMETER} pDepartment=${DEPT}

rm aws-ip-changed-sam.yml
echo """

               Setting up Lambda IP Range notifier
----------------------------------------------------

"""
