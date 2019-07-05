#!/usr/bin/env bash

#REGION=$1
DEPT=$2
#DEPT_UPPER=$(echo "${DEPT}" | awk '{print toupper($0)}')
DIRECTORY=$(dirname $0)

# defaults
UploadTimeout=30
LogRetentionInDays=90
AuditRetentionDays=90


die2() { echo >&2 -e "\nERROR: $@\n"; exit 1; }
run() { "$@"; code=$?; [[ ${code} -ne 0 ]] && die2 "command [$*] failed with error code $code"; }


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
     Upload timeout of ${UploadTimeout} days
     CloudWatch Log retention of ${LogRetentionInDays} days
     CloudTrail Log retention of ${AuditRetentionDays} days

"""

run cf sync -y --context ${DIRECTORY}/../../transforms/config-deployer.yml ${DIRECTORY}/deployment.stacks

echo """

               CloudTrail: complete
----------------------------------------------------

"""
