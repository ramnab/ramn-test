#!/usr/bin/env bash

if [[ -z "$1" ]];
then
    echo """Usage: ./update-customer.sh DEPT ENV

    """
    exit
fi


DEPT=$1
ENV=$(echo $2 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
ENV_UPPER=$(echo ${ENV} | awk '{print toupper($0)}')
ENV_LOWER=$(echo ${ENV} | awk '{print tolower($0)}')
REGION="eu-central-1"
ACCOUNT_ALIAS=$(aws iam list-account-aliases --query "AccountAliases | [0]" --output text)

echo """

--------------------------------------------------------
   Updating Common Account for a deployed MI Solution
   --------------------------------------------------

            Account:     ${ACCOUNT_ALIAS}
            Department:  ${DEPT}
            Environment: ${ENV_LOWER}

"""

read -p "> Continue? (y/n) " cont
if [[ ${cont} != "y" ]]; then
    echo "Aborting..."
    exit
fi

# Create transform file
DIRECTORY=$(dirname $0)
mkdir -p ${DIRECTORY}/../transforms

cat > ${DIRECTORY}/../transforms/config-common-deployer.yml <<EOL
env: ${ENV}
env_lower: ${ENV_LOWER}
env_upper: ${ENV_UPPER}
department: ${DEPT}
region: ${REGION}
EOL

echo """
Updating bucket policy for common reporting bucket in ${ENV}:
ensure that modules/base-common/resources/reporting-bucket-policies*.yml is up to date"""

echo
cf sync -y --context ${DIRECTORY}/../transforms/config-common-deployer.yml \
   modules/base-common/reporting-bucket-policies.stacks

#rm ${DIRECTORY}/../transforms/config-common-deployer.yml
