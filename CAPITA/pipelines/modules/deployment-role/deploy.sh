#!/usr/bin/env bash

# deploy.sh
#
# Deploys a role for the pipelines to assume
# Run in to the customer target account / environment directly
#
# Usage:
#   deploy.sh ENV
#

#ENV=$1
DIRECTORY=$(dirname $0)
source ${DIRECTORY}/../../scripts/helpers.sh

echo """
---------------------------------------
Deploying pipeline deployment role...

"""

run cf sync -y ${DIRECTORY}/deployment.template

echo """

------------- completed --------------
"""
