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
source ${DIRECTORY}/../../../pipelines/scripts/helpers.sh

DEPT=$1
ENV=$(echo $2 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
CONF="${DIRECTORY}/../../../pipelines/config/${3}.conf"

config_exists ${CONF}

DEPT_UPPER=$(echo "${DEPT}" | awk '{print toupper($0)}')
ENV_LOWER=$(echo "${ENV}" | awk '{print tolower($0)}')
CLIENT="$(prop 'client')"
REGION="$(prop 'region.reports' eu-central-1)"

echo """
Setting up S3 Public Access Blocker:
      o Lambda function
      o custom cloudformation to trigger lambda
-------------------------------------
  config:          ${3}
  client:          ${CLIENT}
  env:             ${ENV}
  department:      ${DEPT}
  region:          ${REGION}

"""

cat > ${DIRECTORY}/cf-config.yml <<EOL
env: ${ENV}
env_lower: ${ENV_LOWER}
department: ${DEPT}
department_upper: ${DEPT_UPPER}
client: ${CLIENT}
region: ${REGION}
EOL

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

run cf sync --context ${DIRECTORY}/cf-config.yml -y ${DIRECTORY}/deployment.stacks

rm ${DIRECTORY}/cf-config.yml
rm s3-access-blocker.yml
echo "s3 block public access module COMPLETED"
