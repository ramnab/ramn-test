#!/usr/bin/env bash

DEPARTMENT=$1
DEPT_UPPER=$(echo "${DEPARTMENT}" | awk '{print toupper($0)}')
DIRECTORY=$(dirname $0)

# Defaults
UploadTimeout=30
LogRetentionInDays=90
AuditRetentionDays=90
REGION="eu-central-1"
# get name (alias) of current account
ACCOUNT_ALIAS=$(aws iam list-account-aliases --query "AccountAliases | [0]" --output text)

echo """
---------------------------------------
           Setting up CloudTrail
           ---------------------

         Account:    ${ACCOUNT_ALIAS}
         Region:     ${REGION}
         Department: ${DEPARTMENT}

 with
     Upload timeout of ${UploadTimeout} days
     CloudWatch Log retention of ${UploadTimeout} days
     CloudTrail Log retention of ${AuditRetentionDays} days

"""

read -p "> Continue? (y/n) " cont
if [[ ${cont} != "y" ]]; then
    echo "Aborting..."
    exit
fi


cat > ${DIRECTORY}/config-deployer.yml <<EOL
department: ${DEPARTMENT}
department_upper: ${DEPT_UPPER}
region: ${REGION}
upload_timeout_days: ${UploadTimeout}
log_retention_days: ${LogRetentionInDays}
audit_retention_days: ${AuditRetentionDays}
EOL

cf sync -y --context ${DIRECTORY}/config-deployer.yml ${DIRECTORY}/../modules/cloudtrail-base/deployment.stacks

rm ${DIRECTORY}/config-deployer.yml

echo """

[Completed]
"""
