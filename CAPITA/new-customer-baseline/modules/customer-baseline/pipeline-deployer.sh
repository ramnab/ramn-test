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
REGION="$(prop 'region.reports' eu-west-2)"
EXPIRATION_REPORTS="$(prop 'expiration.reports' 30)"
EXPIRATION_CTR="$(prop 'expiration.ctr' 7)"
EXPIRATION_AGENT_EVENTS="$(prop 'expiration.agentevents' 30)"

echo """
Deploying customer baseline module, incorporating:
      o Lambda distribution bucket
      o Reporting bucket
      o Agent Events Kinesis stream
-------------------------------------
  config:          ${3}
  client:          ${CLIENT}
  env:             ${ENV}
  department:      ${DEPT}
  region:          ${REGION}

Expiration settings on reporting bucket prefix:
  /report:           ${EXPIRATION_REPORTS} days
  /raw-agentevents:  ${EXPIRATION_AGENT_EVENTS} days
  /raw-ctr:          ${EXPIRATION_CTR} days

"""

cat > ${DIRECTORY}/cf-config.yml <<EOL
env: ${ENV}
env_lower: ${ENV_LOWER}
department: ${DEPT}
department_upper: ${DEPT_UPPER}
client: ${CLIENT}
region: ${REGION}
expiration_reports: ${EXPIRATION_REPORTS}
expiration_ctr: ${EXPIRATION_CTR}
expiration_agentevents: ${EXPIRATION_AGENT_EVENTS}
EOL

run cf sync -y --context ${DIRECTORY}/cf-config.yml ${DIRECTORY}/deployment.stacks

rm ${DIRECTORY}/cf-config.yml
echo "customer baseline module COMPLETED"
