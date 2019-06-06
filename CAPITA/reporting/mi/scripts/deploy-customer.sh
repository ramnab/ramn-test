#!/usr/bin/env bash


# Deploy MI Solution to Customer Account
#
# Usage:
#   deploy-customer.sh [-r|--region <arg>] [-d|--department <arg>] [-h|--help] <client> <env>
#
# where:
# 	<client>          :  Client short name, e.g. tradeuk (required)
#	<env>             :  Environment tag, e.g. dev (required)
#	-r,--region       :  AWS region (default: 'eu-central-1')
#	-d,--department   :  Department (default: 'ccm')
#	-h,--help         :  Prints help (usage instructions)


#-----------------------------------------------------------------------
# Get command line args using argbash.io
# When updating, regenerate file by copy and pasting config into
# http://argbash.io/generate
# Please reflect any changes to usage docs above

DIRECTORY=$(dirname $0)
source ${DIRECTORY}/deploycustomerargs.sh "$@"


#-----------------------------------------------------------------------
# Generate local variables

if [[ ${_arg_module} == 'all' ]];
then
    modules=( base-customer ctr queue-interval agent-interval )
else
    modules=( ${_arg_module} )
fi

DEPT=${_arg_department}
DEPT_UPPER=$(echo "${DEPT}" | awk '{print toupper($0)}')
CLIENT=${_arg_client}
ENV=$(echo ${_arg_env} | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
ENV_LOWER=$(echo ${ENV} | awk '{print tolower($0)}')
ENV_UPPER=$(echo ${ENV} | awk '{print toupper($0)}')
REGION=${_arg_region}
ACCOUNT_ALIAS=$(aws iam list-account-aliases --query "AccountAliases | [0]" --output text)


#-----------------------------------------------------------------------
# Begin deployment

echo """

----------------------------------------------------
   Deploying MI Solution into Customer Account
   -------------------------------------------

            Account:     ${ACCOUNT_ALIAS}
            Region:      ${REGION}
            Department:  ${DEPT}
            Client:      ${CLIENT}
            Environment: ${ENV_LOWER}
            Module(s):   ${modules[@]}

"""

read -p "> Continue? (y/n) " cont
if [[ ${cont} != "y" ]]; then
    echo "Aborting..."
    exit
fi


# Create transform file

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
   eval "${1} ${REGION} ${DEPT} ${CLIENT} ${ENV_LOWER}"
}

for m in "${modules[@]}"
do
    r=".*/${m}/deployer\.sh"
    deployer=`find ./modules/ -type f -regex ${r}`
    do_deploy ${deployer}
done

rm ${DIRECTORY}/../transforms/config-customer-deployer.yml
