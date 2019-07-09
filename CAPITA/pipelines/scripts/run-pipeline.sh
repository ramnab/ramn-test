#!/usr/bin/env bash

# run-pipeline
# Executes a named pipeline in pipeline account
#
# Usage:
#   ./run-pipeline.sh PIPELINE CONFIG ENV
#
# e.g.
#   ./run-pipeline.sh customer-baseline gassafe dev

PIPELINE=$1
CONFIG=$2
ENV=$3

exit_if_not_set () {
    if [[ ! $1 ]]; then
        echo """
Arguments missing, usage:
   ./run-pipeline.sh PIPELINE CONFIG ENV

"""
        exit 1
    fi
}
exit_if_not_set ${PIPELINE}
exit_if_not_set ${CONFIG}
exit_if_not_set ${ENV}

# get name (alias) of current account
ACCOUNT_ALIAS=$(aws iam list-account-aliases --query "AccountAliases | [0]" --output text)

if [[ ${ACCOUNT_ALIAS}  != "capita-ccm-common-pipeline" ]]; then
    echo "Please switch to the pipeline account: capita-ccm-common-pipeline"
    exit 1
fi

echo """

           Execute Pipeline
           ----------------

    Running pipeline: ${PIPELINE}
    Config:           ${CONFIG}
    Environment:      ${ENV}

"""
aws codebuild --region eu-central-1 start-build --project-name ${PIPELINE} \
              --source-version feature/cloudtrail-for-organisations \
              --environment-variables-override name=CONFIG,value=${CONFIG},type=PLAINTEXT \
                                               name=ENV,value=${ENV},type=PLAINTEXT &> /dev/null

BUILDID=$(aws codebuild --region eu-central-1 list-builds-for-project --project-name customer-baseline --query 'ids[0]' --output text)
echo -e "\nStarted build process for build id ${BUILDID}"

getBuildStatus () {
    buildid=$1
    status=$(aws codebuild batch-get-builds --ids ${buildid} --query 'builds[].{phase:currentPhase,status:buildStatus}' --output text)
}

echo -e "\nBuild phase and status:"
prevstatus=''
while ! [[ ${status} =~ 'COMPLETED' ]]; do

    getBuildStatus ${BUILDID}
    if [[ ${prevstatus} != ${status} ]]; then
        echo ${status}
    fi
    prevstatus=${status}
    sleep 3s

done

echo -e "\nPipeline completed"
LOGS=$(aws codebuild batch-get-builds --ids ${BUILDID} --query 'builds[].logs.deepLink' --output text)
echo "Cloudwatch logs are available at: ${LOGS}"
