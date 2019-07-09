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

set -e

DEPT=$1
ENV=$2
CONFIG=$3
MODULE=$4
DIRECTORY=$(echo "$(dirname $0)/../../../new-customer-baseline")

# Deploying module: call-recordings-bucket
if [[ ${MODULE} == 'all' || ${MODULE} == 'call-recordings-bucket' ]]; then
    echo "Deploying call-recordings-bucket"
    ${DIRECTORY}/modules/call-recordings-bucket/pipeline-deployer.sh ${DEPT} ${ENV} ${CONFIG}
fi

# Deploying module: baseline
if [[ ${MODULE} == 'all' || ${MODULE} == 'customer-baseline' ]]; then
    echo "Deploying customer baseline"
    ${DIRECTORY}/modules/customer-baseline/pipeline-deployer.sh ${DEPT} ${ENV} ${CONFIG}
fi

# Deploying module: keys
if [[ ${MODULE} == 'all' || ${MODULE} == 'keys' ]]; then
    echo "Deploying keys"
    ${DIRECTORY}/modules/keys/pipeline-deployer.sh ${DEPT} ${ENV} ${CONFIG}
fi

# Deploying module: cloudtrail
if [[ ${MODULE} == 'all' || ${MODULE} == 'cloudtrail' ]]; then
    echo "Deploying cloudtrail"
    ${DIRECTORY}/modules/cloudtrail/pipeline-deployer.sh ${DEPT} ${ENV} ${CONFIG}
fi
