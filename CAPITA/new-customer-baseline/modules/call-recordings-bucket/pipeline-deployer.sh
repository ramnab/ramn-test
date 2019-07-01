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
REPORTS_REGION="$(prop 'region.calls' eu-central-1)"
CALLS_REGION="$(prop 'region.calls' ${REPORTS_REGION})"
EXPIRATION_CALLS="$(prop 'expiration.calls' 90)"

echo """
Deploying call-recordings-bucket module
---------------------------------------
  config:          ${CONF}
  client:          ${CLIENT}
  env:             ${ENV}
  department:      ${DEPT}
  region (calls):  ${CALLS_REGION}
  calls expire after ${EXPIRATION_CALLS} days

"""

cat > ${DIRECTORY}/cf-config.yml <<EOL
env: ${ENV}
env_lower: ${ENV_LOWER}
department: ${DEPT}
department_upper: ${DEPT_UPPER}
client: ${CLIENT}
region: ${CALLS_REGION}
expiration_calls: ${EXPIRATION_CALLS}
EOL


run cf sync -y --context ${DIRECTORY}/cf-config.yml ${DIRECTORY}/deployment.stacks

rm ${DIRECTORY}/cf-config.yml
echo "call-recordings-bucket module COMPLETED"
