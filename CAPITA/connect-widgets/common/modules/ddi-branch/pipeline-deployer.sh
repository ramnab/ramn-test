#!/usr/bin/env bash

# pipeline-deployer
# Designed to deploy this module using the deployment pipeline
# Can be run locally
#
# Usage:
#    pipeline-deployer.sh DEPT ENV CONFIG_FILE
#
# CONFIG_FILE is from /pipelines/config/*.conf
#


DIRECTORY=$(dirname $0)
source ${DIRECTORY}/../../../../pipelines/scripts/helpers.sh

DEPT=$1
ENV=$(echo $2 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
CONF="${DIRECTORY}/../../../../pipelines/config/${3}.conf"

config_exists ${CONF}

DEPT_UPPER=$(echo "${DEPT}" | awk '{print toupper($0)}')
ENV_LOWER=$(echo "${ENV}" | awk '{print tolower($0)}')
CLIENT="$(prop 'client')"
DEPLOY_REGION="$(prop 'region.widgets' 'eu-west-2')"

echo """
Deploying ddi-branch AWS Connect widget
---------------------------------------
  config:          ${CONF}
  client:          ${CLIENT}
  env:             ${ENV}
  department:      ${DEPT}
  deploy region:   ${DEPLOY_REGION}

"""

LAMBDA_S3=s3-capita-${DEPT}-connect-${CLIENT}-${ENV_LOWER}-${DEPLOY_REGION}-lambdas

aws cloudformation package --region ${DEPLOY_REGION} \
                           --template-file ${DIRECTORY}/resources/ddibranch-widget.yml \
                           --s3-bucket ${LAMBDA_S3} \
                           --output-template-file deploy-ddibranch-widget.yml

aws cloudformation deploy --region ${DEPLOY_REGION} \
                          --template-file deploy-ddibranch-widget.yml \
                          --stack-name stCapita-CCM-${CLIENT}-${ENV}-DdiBranch  \
                          --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
                          --parameter-overrides \
                                pClient=${CLIENT} \
                                pEnvironment=${ENV_UPPER} \
                                pEnvironmentLowerCase=${ENV_LOWER} \
                                pDepartment=${DEPT_UPPER} \

rm deploy-ddibranch-widget.yml
