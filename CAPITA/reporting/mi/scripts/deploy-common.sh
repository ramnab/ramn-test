#!/usr/bin/env bash


# Deploy MI Solution to Common Account
# Usage:
#   deploy-common.sh [-r|--region <arg>] [-d|--department <arg>] [-h|--help] <env> [<module>]
#
# where:
#	<env>              :  Environment tag
#	<module>           :  Specific module to deploy (default: 'all')
#	-r,--region        :  AWS region (default: 'eu-central-1')
#	-d,--department    :  Department (default: 'ccm')"
#	-h,--help          :  Prints help


#-----------------------------------------------------------------------
# Get command line args using argbash.io
# When updating, regenerate file by copy and pasting config into
# http://argbash.io/generate
# Please reflect any changes to usage docs above

DIRECTORY=$(dirname $0)
source ${DIRECTORY}/deploycommonargs.sh "$@"


#-----------------------------------------------------------------------
# Generate local variables

if [[ ${_arg_module} == 'all' ]];
then
    modules=( base-common common-health )
else
    modules=( ${_arg_module} )
fi

REGION=${_arg_region}
DEPT=${_arg_department}
DEPT_UPPER=$(echo "${DEPT}" | awk '{print toupper($0)}')
ENV=$(echo ${_arg_env} | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
ENV_LOWER=$(echo ${ENV} | awk '{print tolower($0)}')
ENV_UPPER=$(echo ${ENV} | awk '{print toupper($0)}')

ACCOUNT_ALIAS=$(aws iam list-account-aliases --query "AccountAliases | [0]" --output text)


#-----------------------------------------------------------------------
# Begin deployment

echo """

----------------------------------------------------
     Deploying MI Solution into Common Account
     -----------------------------------------

            Account:     ${ACCOUNT_ALIAS}
            Region:      ${REGION}
            Department:  ${DEPT}
            Environment: ${ENV_LOWER}
            Module(s):   ${modules}

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
   eval "${1} ${REGION} ${DEPT} ${ENV_LOWER}"
}


for m in "${modules[@]}"
do
    r=".*/${m}/deployer\.sh"
    deployer=`find ./modules/ -type f -regex ${r}`
    do_deploy ${deployer}
done

rm  ${DIRECTORY}/../transforms/config-common-deployer.yml
