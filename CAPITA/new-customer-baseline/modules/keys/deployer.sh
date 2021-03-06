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
                customer KMS keys
                ------------------

        Deploying:
            - Connect Master and Call Recordings Key

"""

run cf sync -y --context ${DIRECTORY}/../../transforms/config-deployer.yml ${DIRECTORY}/deployment.stacks

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

echo """

              customer kms keys: complete
----------------------------------------------------

"""
