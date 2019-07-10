#!/usr/bin/env bash
#
# deploy-pipeline.sh
#
# deploys the specified pipeline to the current assumed account
#
# Usage:
#   deploy-pipeline.sh <pipeline>
#
#  <pipeline>    : Pipeline to deploy, required

#DIRECTORY=$(dirname $0)

#------------------------------------------------------------------
# Set up internal variables from command line options

PIPELINE=$1

# get name (alias) of current account
ACCOUNT_ALIAS=$(aws iam list-account-aliases --query "AccountAliases | [0]" --output text)


#-----------------------------------------------------------------------------------
# Start up deployment process

echo """

----------------------------------------------------
           Set up / update a Pipeline
           --------------------------

            Account:     ${ACCOUNT_ALIAS}
            Pipeline:    ${PIPELINE}

"""

read -p "> Continue? (y/n) " cont
if [[ ${cont} != "y" ]]; then
    echo "Aborting..."
    exit
fi

do_deploy() {
   eval "${1}"
}

r=".*/${PIPELINE}/deploy\.sh"
deployer=$(find ./modules/ -type f -regex ${r})
do_deploy ${deployer}

echo """

===========================- COMPLETE -==========================

"""
