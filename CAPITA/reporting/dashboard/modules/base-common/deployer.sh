#!/usr/bin/env bash

DEPT=$1
ENV=$(echo $2 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
ENV_UPPER=$(echo ${ENV} | awk '{print toupper($0)}')
ENV_LOWER=$(echo ${ENV} | awk '{print tolower($0)}')
DIRECTORY=$(dirname $0)


echo """
----------------------------------------------------
                   base-common
                   -----------

"""

echo """

    Creating/Updating Dashboard Connect Metrics User
    ------------------------------------------

"""


cf sync -y --context ${DIRECTORY}/../../transforms/config-common-deployer.yml \
                     ${DIRECTORY}/common-dashboard-user.stacks


