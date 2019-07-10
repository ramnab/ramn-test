#!/usr/bin/env bash

# deploy.sh
#
# Creates a source code repository
#
# Usage:
#   deploy.sh
#
DIRECTORY=$(dirname $0)

echo """
---------------------------------------
Creating Source Code Repository

"""

cf sync -y ${DIRECTORY}/deployment.template

echo """

------------- completed --------------
"""
