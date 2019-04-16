#!/usr/bin/env bash

# Update the RTA alarms that the user can view for a specified client

ENV=$1
USERNAME=$2
CLIENT=$3

TESTPOOLID="eu-central-1_5vpngTHt2"
DEVPOOLID="eu-central-1_VvHvpO1fe"
POOLID=${TESTPOOLID}

if [[ ${ENV} == "dev" ]]; then
    POOLID=${DEVPOOLID}
fi

USERATTR="Name=custom:client,Value=${CLIENT}"

echo "[${POOLID}] Allowing user ${USERNAME} to access client(s) ${CLIENT}"
echo ${USERATTR}

aws cognito-idp admin-update-user-attributes --user-pool-id ${POOLID} \
                                             --username ${USERNAME} \
                                             --user-attributes Name=custom:client,Value=\"${CLIENT}\"

