#!/usr/bin/env bash

REGION=$1
DEPT=$2
DEPT_UPPER=$(echo "${DEPT}" | awk '{print toupper($0)}')
CLIENT=$3
ENV=$(echo $4 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
ENV_LOWER=$(echo ${ENV} | awk '{print tolower($0)}')
DIRECTORY=$(dirname $0)

die2() { echo >&2 -e "\nERROR: $@\n"; exit 1; }
run() { "$@"; code=$?; [[ ${code} -ne 0 ]] && die2 "command [$*] failed with error code $code"; }


echo """
----------------------------------------------------
                Setting up S3 Public Access Blocker
                ---------------------

        Deploying:
            - Lambda Function
            - Custom CloudFormation To Call Lambda

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
                           --template-file ${DIRECTORY}/resources/s3-block-public-access.yml \
                           --s3-bucket ${LAMBDA_S3} \
                           --output-template-file s3-access-blocker.yml

aws cloudformation deploy --region ${REGION} --template-file s3-access-blocker.yml \
                          --stack-name stCapita-"${DEPT_UPPER}"-Connect-S3-Account-PublicAccess-Revoker  \
                          --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM

run cf sync --context ${DIRECTORY}/../../transforms/config-deployer.yml -y ${DIRECTORY}/deployment.stacks
rm s3-access-blocker.yml
echo """

               S3 block access: complete
----------------------------------------------------

"""
