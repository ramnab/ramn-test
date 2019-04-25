#!/usr/bin/env bash

if [[ -z "$1" ]] || [[ -z "$2" ]] || [[ -z "$3" ]];
then
    echo """Usage: ./deploy-customer.sh DEPT CLIENT ENV [MODULE]

If no module is specified then all will be deployed

    """
    exit
fi


if [[ -z "$4" ]];
then
    modules=( base-customer ctr queue-interval agent-interval )
else
    modules=( $4 )
fi

DEPT=$1
DEPT_UPPER=$(echo "$1" | awk '{print toupper($0)}')
CLIENT=$2
ENV=$(echo $3 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
ENV_LOWER=$(echo ${ENV} | awk '{print tolower($0)}')
ENV_UPPER=$(echo ${ENV} | awk '{print toupper($0)}')
REGION='eu-central-1'
ACCOUNT_ALIAS=$(aws iam list-account-aliases --query "AccountAliases | [0]" --output text)

echo """

----------------------------------------------------
   Deploying MI Solution into Customer Account
   -------------------------------------------

            Account:     ${ACCOUNT_ALIAS}
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

# Create transform file
DIRECTORY=$(dirname $0)
mkdir -p ${DIRECTORY}/../transforms

cat > ${DIRECTORY}/../transforms/config-customer-deployer.yml <<EOL
env: ${ENV}
env_lower: ${ENV_LOWER}
env_upper: ${ENV_UPPER}
department: ${DEPT}
department_upper: ${DEPT_UPPER}
region: ${REGION}
client: ${CLIENT}
EOL


do_deploy() {
   eval "${1} ${DEPT} ${CLIENT} ${ENV_LOWER}"
}

for m in "${modules[@]}"
do
    r=".*/${m}/deployer\.sh"
    deployer=`find ./modules/ -type f -regex ${r}`
    do_deploy ${deployer}
done

#rm ${DIRECTORY}/../transforms/config-customer-deployer.yml
