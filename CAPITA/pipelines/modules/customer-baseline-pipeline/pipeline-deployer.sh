#!/usr/bin/env bash

# pipeline-deployer
#
# deploys the new customer baseline, can be run either in pipeline or locally
#
# Usage:
#   pipeline-deployer.sh DEPT ENV CONFIG
#
# where
#   DEPT    is department, for example, 'ccm'
#   ENV     is environment such as 'dev'
#   CONFIG  is the name of the config file, e.g. 'gassafe' will use /pipelines/config/gassafe.conf


DEPT=$1
ENV=$2
CONFIG=$3
DIRECTORY=$(echo "$(dirname $0)/../../../new-customer-baseline")

# Deploying module: call-recordings-bucket
${DIRECTORY}/modules/call-recordings-bucket/pipeline-deployer.sh ${DEPT} ${ENV} ${CONFIG}

# Deploying module: baseline
${DIRECTORY}/modules/customer-baseline/pipeline-deployer.sh ${DEPT} ${ENV} ${CONFIG}

# Deploying module: keys
${DIRECTORY}/modules/keys/pipeline-deployer.sh ${DEPT} ${ENV} ${CONFIG}


