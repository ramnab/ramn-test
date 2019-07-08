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
#DEPT_LOWER=$(echo "${DEPT}" | awk '{print tolower($0)}')
ENV_LOWER=$(echo "${ENV}" | awk '{print tolower($0)}')
CLIENT="$(prop 'client')"
REGION="$(prop 'region.reports' eu-central-1)"

# Defaults for KMS keys
MASTER_KEY="alias/connect-master-${ENV_LOWER}"
CALL_KEY="alias/connect-recordings-${ENV_LOWER}"
# KMS names for production
test "${ENV_LOWER}" == 'prod' && MASTER_KEY="alias/connect-master" && CALL_KEY="alias/connect-recordings"


echo """
Deploying customer Connect KMS keys, incorporating:
      o Connect Master and Call Recordings Key

-------------------------------------
  config:          ${3}
  client:          ${CLIENT}
  env:             ${ENV}
  department:      ${DEPT}
  region:          ${REGION}


"""

cat > ${DIRECTORY}/cf-config.yml <<EOL
region: ${REGION}
env: ${ENV}
department: ${DEPT}
department_upper: ${DEPT_UPPER}
master_key: ${MASTER_KEY}
EOL

run cf sync -y --context ${DIRECTORY}/cf-config.yml ${DIRECTORY}/deployment.stacks

echo "Protecting KMS keys..."
KMS_STACK="stCapita-${DEPT_UPPER}-Customer-Connect-${ENV}-Keys"

run aws cloudformation --region ${REGION} set-stack-policy \
                   --stack-name ${KMS_STACK} --stack-policy-body "{
  \"Statement\" : [
    {
      \"Effect\" : \"Deny\",
      \"Action\" : \"Update:*\",
      \"Principal\": \"*\",
      \"Resource\" : \"*\"
    }
  ]
}"
run aws cloudformation --region ${REGION}  update-termination-protection  \
                   --enable-termination-protection --stack-name ${KMS_STACK}


rm ${DIRECTORY}/cf-config.yml
echo "keys module COMPLETED"
