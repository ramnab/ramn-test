#!/usr/bin/env bash

if [[ -z "$1" ]] || [[ -z "$2" ]] || [[ -z "$3" ]]; then
    echo """

Usage: ./deploy.sh DEPT CLIENT ENV [MODULE]

If no module is specified then all will be deployed

    """
    exit
fi

# if no module specified in args, deploy all
if [[ -z "$4" ]]; then
    modules=( customer-baseline )
else
    modules=( $4 )
fi

DEPT=$1
DEPT_UPPER=$(echo "$1" | awk '{print toupper($0)}')
CLIENT=$(echo "$2")
ENV=$(echo $3 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
ENV_LOWER=$(echo $3 | awk '{print tolower($0)}')
ENV_UPPER=$(echo $3 | awk '{print toupper($0)}')
DIRECTORY=`dirname $0`
REGION='eu-central-1'
MASTER_KEY="alias/connect-master-${ENV_LOWER}"
CALL_KEY="alias/connect-recordings-${ENV_LOWER}"

if [[ ${ENV_LOWER} == 'prod' ]]; then
    MASTER_KEY="alias/connect-master"
    CALL_KEY="alias/connect-recordings"
fi

ACCOUNT_ALIAS=$(aws iam list-account-aliases --query "AccountAliases | [0]" --output text)

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
    deployer=`find ./modules/ -type f -regex ${r}`
    do_deploy ${deployer}
done


CALL_RECORDINGS=`getStackOutput stCapita-${DEPT_UPPER}-Customer-Connect-${ENV}-CallRecordingsBucket oCallRecordingBucket`
REPORT_BUCKET=`getStackOutput stCapita-${DEPT_UPPER}-Customer-Connect-${ENV}-ReportingBucket oCustomerReportingBucketArn`
AGENT_STREAM=`getStackOutput stCapita-${DEPT_UPPER}-Customer-Connect-${ENV}-AgentEvents oAgentEventsStream`

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
