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
CONF="${DIRECTORY}/../../../pipelines/config/${3}.conf"

config_exists ${CONF}



DEPT_UPPER=$(echo "${DEPT}" | awk '{print toupper($0)}')
CLIENT="$(prop 'client')"
REPORTS_REGION="$(prop 'region.reports' eu-central-1)"
UPLOAD_TIMEOUT="$(prop 'cloudtrail.upload_timeout' 30)"
LOG_RETENTION="$(prop 'cloudtrail.log_retention' 90)"
AUDIT_RETENTION="$(prop 'cloudtrail.audit_retention' 365)"


echo """
----------------------------------------------------
                Setting up CloudTrail
                ---------------------

        Deploying:
            - CloudTrail KMS Key
            - CloudTrail CloudWatch logs
            - CloudTrail bucket
            - Access bucket
 with
     Upload timeout of ${UPLOAD_TIMEOUT} days
     CloudWatch Log retention of ${LOG_RETENTION} days
     CloudTrail Log retention of ${AUDIT_RETENTION} days

"""

cat > ${DIRECTORY}/cf-config.yml <<EOL
department: ${DEPT}
department_upper: ${DEPT_UPPER}
client: ${CLIENT}
region: ${REPORTS_REGION}
upload_timeout_days: ${UPLOAD_TIMEOUT}
log_retention_days: ${LOG_RETENTION}
audit_retention_days: ${AUDIT_RETENTION}
EOL


run cf sync -y --context ${DIRECTORY}/cf-config.yml ${DIRECTORY}/deployment.stacks

rm ${DIRECTORY}/cf-config.yml
echo "call-recordings-bucket module COMPLETED"
