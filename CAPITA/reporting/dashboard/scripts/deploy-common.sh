#!/usr/bin/env bash

if [[ -z "$1" ]];
then
    echo """
Usage: ./deploy-common.sh DEPT ENV
"""
    exit
fi


DEPT=$1
DEPT_UPPER=$(echo "$1" | awk '{print toupper($0)}')
ENV=$(echo $2 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
ENV_LOWER=$(echo ${ENV} | awk '{print tolower($0)}')
ENV_UPPER=$(echo ${ENV} | awk '{print toupper($0)}')
REGION='eu-central-1'
ACCOUNT_ALIAS=$(aws iam list-account-aliases --query "AccountAliases | [0]" --output text)

echo """

----------------------------------------------------
     Deploying Dashboard Solution into Common Account
     -----------------------------------------

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
department_upper: ${DEPT_UPPER}
region: ${REGION}
EOL

do_deploy() {
   eval "${1} ${DEPT} ${ENV_LOWER}"
}

modules=( base-common )
for m in "${modules[@]}"
do
    r=".*/${m}/deployer\.sh"
    deployer=`find ./modules/ -type f -regex ${r}`
    do_deploy ${deployer}
done

rm  ${DIRECTORY}/../transforms/config-common-deployer.yml
