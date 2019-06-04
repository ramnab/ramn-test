#!/usr/bin/env bash

DEPT=$1
DEPT_UPPER=$(echo "${DEPT}" | awk '{print toupper($0)}')
CLIENT=$2
ENV=$(echo $3 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
ENV_LOWER=$(echo ${ENV} | awk '{print tolower($0)}')
DIRECTORY=$(dirname $0)

die2() { echo >&2 -e "\nERROR: $@\n"; exit 1; }
run() { "$@"; code=$?; [[ ${code} -ne 0 ]] && die2 "command [$*] failed with error code $code"; }


echo """
----------------------------------------------------
                customer baseline
                -----------------

        Deploying:
            - Lambda Distribution Bucket
            - Customer Reporting Bucket
            - Call Recordings Bucket
            - Agent Event Stream + Firehose
            - Connect Master and Call Recordings Key

"""

run cf sync -y --context ${DIRECTORY}/../../transforms/config-deployer.yml ${DIRECTORY}/deployment.stacks

echo "Protecting KMS keys..."
KMS_STACK="stCapita-${DEPT_UPPER}-Customer-Connect-${ENV}-Keys"

run aws cloudformation --region eu-central-1 set-stack-policy \
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
run aws cloudformation --region eu-central-1  update-termination-protection  \
                   --enable-termination-protection --stack-name ${KMS_STACK}


echo "Tagging Agent Event Firehose..."
python ${DIRECTORY}/../../scripts/tag-firehose.py -f kfh-ccm-agent-events-${ENV_LOWER} \
                    -t sec:Compliance:PII bus:BusinessUnit:ccm bus:ClientName:${CLIENT} \
                       tech:Environment:${ENV_LOWER} tech:ApplicationID:capita-${DEPT}-connect \
                       tech:ApplicationRole:reporting
echo """

              customer baseline: complete
----------------------------------------------------

"""
