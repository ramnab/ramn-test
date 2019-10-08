#!/usr/bin/env bash

REGION=$1
DEPT=$2
ENV=$(echo $3 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
ENV_UPPER=$(echo ${ENV} | awk '{print toupper($0)}')
ENV_LOWER=$(echo ${ENV} | awk '{print tolower($0)}')
DIRECTORY=$(dirname $0)


echo """
----------------------------------------------------
                   common-ca-roles
                   -----------

"""

echo """

         Deploying Cross Account Roles Trusting Credentials Account
         ----------------------------

"""

cf sync -y --context ${DIRECTORY}/../../transforms/config-common-deployer.yml \
                     ${DIRECTORY}/common-ca-roles.stacks
