#!/usr/bin/env bash

DEPT=$1
CLIENT=$2
ENV=$(echo $3 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
ENV_LOWER=$(echo ${ENV} | awk '{print tolower($0)}')
ENV_UPPER=$(echo ${ENV} | awk '{print toupper($0)}')

DIRECTORY=$(dirname $0)


echo """
----------------------------------------------------
                  base-customer
                  -------------

"""


echo """

        Creating Cross-Account Role for Dashboard Metrics
        -------------------------------------------------

"""

cf sync -y --context ${DIRECTORY}/../../transforms/config-customer-deployer.yml \
        ${DIRECTORY}/cross-account-metrics-role.stacks


echo """

                  base-customer: complete
----------------------------------------------------


"""
