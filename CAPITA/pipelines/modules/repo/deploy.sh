#!/usr/bin/env bash

# deploy.sh
#
# Creates a source code repository
#
# Usage:
#   deploy.sh
#

source ../scripts/helpers.sh

echo """
---------------------------------------
Creating Source Code Repository

"""

run cf sync -y resources/code-commit-repo.yml

echo """

------------- completed --------------
"""
