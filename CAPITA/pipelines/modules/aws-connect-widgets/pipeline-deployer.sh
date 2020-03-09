#!/usr/bin/env bash

# pipeline-deployer
#
# Deploys AWS Connect Widgets located in CAPITA/connect-widgets/common/modules.
# Widgets can be run locally, or using CodeBuild project (build spec located CAPITA/pipelines/modules/aws-connect-widgets/
#
# Usage:
#   pipeline-deployer.sh DEPT ENV CONFIG WIDGET
#
# where
#   DEPT    is department, for example, 'ccm'
#   ENV     is environment such as 'dev', 'test', or 'prod'
#   CONFIG  is the name of the config file, e.g. 'gassafe' will use /pipelines/config/gassafe.conf
#   WIDGET  is the name of the widget that you wish to deploy.
#           Allowed values: all; blacklist; ddi-branch; special-days; variable-store

set -e

DEPT=$1
ENV=$2
CONFIG=$3
WIDGET=$4
DIRECTORY=$(echo "$(dirname $0)/../../../connect-widgets/common/modules")

# Deploying widget: blacklist
if [[ ${WIDGET} == 'all' || ${WIDGET} == 'blacklist' ]]; then
    echo "Deploying blacklist widget"
    ${DIRECTORY}/blacklist/pipeline-deployer.sh ${DEPT} ${ENV} ${CONFIG}
fi

# Deploying widget: ddi-branch
if [[ ${WIDGET} == 'all' || ${WIDGET} == 'ddi-branch' ]]; then
    echo "Deploying ddi-branch"
    ${DIRECTORY}/ddi-branch/pipeline-deployer.sh ${DEPT} ${ENV} ${CONFIG}
fi

# Deploying widget: special-days
if [[ ${WIDGET} == 'all' || ${WIDGET} == 'special-days' ]]; then
    echo "Deploying special-days"
    ${DIRECTORY}/special-days/pipeline-deployer.sh ${DEPT} ${ENV} ${CONFIG}
fi

# Deploying widget: variable-store
if [[ ${WIDGET} == 'all' || ${WIDGET} == 'variable-store' ]]; then
    echo "Deploying variable-store"
    ${DIRECTORY}/variable-store/pipeline-deployer.sh ${DEPT} ${ENV} ${CONFIG}
fi