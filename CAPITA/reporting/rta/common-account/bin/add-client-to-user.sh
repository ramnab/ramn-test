#!/usr/bin/env bash

# Update the RTA alarms that the user can view for a specified client

ENV=$1
USERNAMES=$2
CLIENT=$3
OIFS=$IFS
IFS="|"

USERS=(${USERNAMES})

PRODPOOLID="eu-central-1_l3AJqGcNs"
TESTPOOLID="eu-central-1_5vpngTHt2"
DEVPOOLID="eu-central-1_VvHvpO1fe"
POOLID=${TESTPOOLID}

if [[ ${ENV} == "dev" ]]; then
    POOLID=${DEVPOOLID}
elif [[ ${ENV} == "prod" ]]; then
    POOLID=${PRODPOOLID}
fi

USERATTR="Name=custom:client,Value=${CLIENT}"

for ((i=0; i<${#USERS[@]}; ++i)); do
    echo "[${POOLID}] Allowing user ${USERS[$i]} to access client(s) ${CLIENT}"

    aws cognito-idp admin-update-user-attributes --user-pool-id ${POOLID} \
                                                 --username ${USERS[$i]} \
                                                 --user-attributes Name=custom:client,Value=\"${CLIENT}\"
done
IFS=${OIFS}
