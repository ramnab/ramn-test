#!/usr/bin/env bash

# deploy.sh
#
# Deploys the customer-baseline-pipeline
# Run directly into pipelines account
#
# Usage:
#   deploy.sh ENV
#

ENV=$1
DIRECTORY=$(dirname $0)
source ${DIRECTORY}/../../scripts/helpers.sh

echo """
---------------------------------------------
Deploying pipeline customer-baseline-pipeline

"""

run cf sync -y ${DIRECTORY}/deployment.template

echo """

------------- completed --------------
"""
