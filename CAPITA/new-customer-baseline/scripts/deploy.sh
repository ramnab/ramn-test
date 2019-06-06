#!/bin/bash

# Deploy new customer baseline to target customer account

# Usage:
#   deploy.sh [-r|--region <arg>] [-d|--department <arg>] [-h|--help] <env> <client> [<module>]
#
# Where
#  -r|--region is the AWS region, default is 'eu-central-1' (Frankfurt)
#  -d|--department is the short code for the department, default 'ccm'
#  <env> is the environment tag, one of 'dev', 'test', 'prod', required
#  <client> is the short name for the customer, for example 'tradeuk', required
#  module is an optional identifier for the module to be be deployed, default is 'all'

# -h|--help prints the usage instructions and options



#-----------------------------------------------------------------------
# Get command line args using argbash.io
# When updating, regenerate file by copy and pasting config into
# http://argbash.io/generate
# Please reflect any changes to usage docs above

DIRECTORY=$(dirname $0)
source ${DIRECTORY}/deployargs.sh "$@"


#------------------------------------------------------------------
# Set up internal variables from command line options

DEPT=$(echo ${_arg_department} | awk '{print tolower($0)}')
DEPT_UPPER=$(echo "${DEPT}" | awk '{print toupper($0)}')
CLIENT=$(echo ${_arg_client} | awk '{print tolower($0)}')
ENV=$(echo ${_arg_env} | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
ENV_LOWER=$(echo ${ENV} | awk '{print tolower($0)}')
ENV_UPPER=$(echo ${ENV} | awk '{print toupper($0)}')
REGION=${_arg_region}

# Defaults for KMS keys
MASTER_KEY="alias/connect-master-${ENV_LOWER}"
CALL_KEY="alias/connect-recordings-${ENV_LOWER}"
# KMS names for production
test "${ENV_LOWER}" == 'prod' && MASTER_KEY="alias/connect-master" && CALL_KEY="alias/connect-recordings"

modules=( customer-baseline )
test ${_arg_module} != 'all' && modules=( ${_arg_module} )

# ensure environment is one of dev/test/prod (or a variation, e.g. dev01)

if ! [[ ${ENV_LOWER} =~ dev|test|prod ]]; then
    echo "${ENV_LOWER} is not a valid environment name"
    exit 1
fi

# get name (alias) of current account
ACCOUNT_ALIAS=$(aws iam list-account-aliases --query "AccountAliases | [0]" --output text)


#-----------------------------------------------------------------------------------
# Start up deployment process

echo """

----------------------------------------------------
        Set up / update a Customer Account
        ----------------------------------

            Account:     ${ACCOUNT_ALIAS}
            Region:      ${REGION}
            Department:  ${DEPT}
            Client:      ${CLIENT}
            Environment: ${ENV_LOWER}
            Modules:     ${modules[@]}

"""

read -p "> Continue? (y/n) " cont
if [[ ${cont} != "y" ]]; then
    echo "Aborting..."
    exit
fi

# create cfn-square context file from args
mkdir -p ${DIRECTORY}/../transforms

cat > ${DIRECTORY}/../transforms/config-deployer.yml <<EOL
env: ${ENV}
env_lower: ${ENV_LOWER}
env_upper: ${ENV_UPPER}
department: ${DEPT}
department_upper: ${DEPT_UPPER}
client: ${CLIENT}
region: ${REGION}
master_key: ${MASTER_KEY}
call_key: ${CALL_KEY}
EOL


do_deploy() {
   eval "${1} ${DEPT} ${CLIENT} ${ENV_LOWER}"
}

getStackOutput () {
    STACKNAME=$1
    KEY=$2
    aws cloudformation --region ${REGION} describe-stacks --query "Stacks[?StackName == '$STACKNAME'].Outputs[]| [?OutputKey=='$KEY'].[OutputValue] | [0]" --output text
}

for m in "${modules[@]}"
do
    r=".*/${m}/deployer\.sh"
    deployer=$(find ./modules/ -type f -regex ${r})
    do_deploy ${deployer}
done

# Look up call recordings / reporting bucket names from previously deployed stacks
CALL_RECORDINGS=$(getStackOutput stCapita-${DEPT_UPPER}-Customer-Connect-${ENV}-CallRecordingsBucket oCallRecordingBucket)
REPORT_BUCKET=$(getStackOutput stCapita-${DEPT_UPPER}-Customer-Connect-${ENV}-ReportingBucket oCustomerReportingBucketArn)

# Tidy up cfn-square context file
rm ${DIRECTORY}/../transforms/config-deployer.yml

echo """
===============================================================
UPDATE CONNECT with following settings:

    Data Storage:
        Call recordings:
            Existing S3 bucket:  ${CALL_RECORDINGS}
            Encryption KMS key:  ${CALL_KEY}

        Exported reports:
            Existing S3 bucket:  ${REPORT_BUCKET}
            Prefix            :  reports
            Encryption KMS key:  ${MASTER_KEY}


=========================- COMPLETE -=========================

"""
