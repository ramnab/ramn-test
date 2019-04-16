#!/usr/bin/env bash

ENV=$1
USERNAME=$2
EMAIL=$3
CLIENT=$4

TESTPOOLID="eu-central-1_5vpngTHt2"
DEVPOOLID="eu-central-1_VvHvpO1fe"
POOLID=${TESTPOOLID}

if [[ ${ENV} == "dev" ]]; then
    POOLID=${DEVPOOLID}
fi

USERATTR="Name=email,Value=${EMAIL} Name=email_verified,Value=true"
echo "CLIENT=${CLIENT}"
if [[ ! -z "${CLIENT}" ]]; then
    USERATTR="${USERATTR} Name=custom:client,Value=${CLIENT}"
fi

echo "[${POOLID}] Creating user: username=${USERNAME}, email=${EMAIL}"
echo ${USERATTR}

aws cognito-idp admin-create-user --user-pool-id ${POOLID} \
                                  --username ${USERNAME} \
                                  --user-attributes ${USERATTR} \
                                  --temporary-password Let.me.in1

