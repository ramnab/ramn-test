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

#-----------------------------------------------------------------------------------------
# Argbash v2.6.1 ###
# Argbash is a bash code generator used to get arguments parsing right.
# Argbash is FREE SOFTWARE, see https://argbash.io for more info
# Generated online by https://argbash.io/generate
# Argbash config:
#
# ARG_OPTIONAL_SINGLE([region],[r],[AWS Region],[eu-central-1])
# ARG_OPTIONAL_SINGLE([department],[d],[Department code],[ccm])
# ARG_POSITIONAL_SINGLE([env],[Environment 'dev', 'test', 'prod', required])
# ARG_POSITIONAL_SINGLE([client],[Client short name, required])
# ARG_POSITIONAL_SINGLE([module],[Module to deploy, optional],[all])
# ARG_HELP([Deploy new-customer-baseline])
# ARGBASH_GO()

die()
{
	local _ret=$2
	test -n "$_ret" || _ret=1
	test "$_PRINT_HELP" = yes && print_help >&2
	echo "$1" >&2
	exit ${_ret}
}

# THE DEFAULTS INITIALIZATION - POSITIONALS
_positionals=()
_arg_module="all"
# THE DEFAULTS INITIALIZATION - OPTIONALS
_arg_region="eu-central-1"
_arg_department="ccm"

print_help ()
{
	printf '%s\n' "Deploy new-customer-baseline"
	printf 'Usage: %s [-r|--region <arg>] [-d|--department <arg>] [-h|--help] <env> <client> [<module>]\n' "$0"
	printf '\t%s\n' "<env>: Environment 'dev', 'test', 'prod', required"
	printf '\t%s\n' "<client>: Client short name, required"
	printf '\t%s\n' "<module>: Module to deploy, default is all (default: 'all')"
	printf '\t%s\n' "-r,--region: AWS Region, default is eu-central-1 (default: 'eu-central-1')"
	printf '\t%s\n' "-d,--department: Department code, default is ccm (default: 'ccm')"
	printf '\t%s\n' "-h,--help: Prints help"
}

parse_commandline ()
{
	while test $# -gt 0
	do
		_key="$1"
		case "$_key" in
			-r|--region)
				test $# -lt 2 && die "Missing value for the optional argument '$_key'." 1
				_arg_region="$2"
				shift
				;;
			--region=*)
				_arg_region="${_key##--region=}"
				;;
			-r*)
				_arg_region="${_key##-r}"
				;;
			-d|--department)
				test $# -lt 2 && die "Missing value for the optional argument '$_key'." 1
				_arg_department="$2"
				shift
				;;
			--department=*)
				_arg_department="${_key##--department=}"
				;;
			-d*)
				_arg_department="${_key##-d}"
				;;
			-h|--help)
				print_help
				exit 0
				;;
			-h*)
				print_help
				exit 0
				;;
			*)
				_positionals+=("$1")
				;;
		esac
		shift
	done
}


handle_passed_args_count ()
{
	_required_args_string="'env' and 'client'"
	test ${#_positionals[@]} -ge 2 || _PRINT_HELP=yes die "FATAL ERROR: Not enough positional arguments - we require between 2 and 3 (namely: $_required_args_string), but got only ${#_positionals[@]}." 1
	test ${#_positionals[@]} -le 3 || _PRINT_HELP=yes die "FATAL ERROR: There were spurious positional arguments --- we expect between 2 and 3 (namely: $_required_args_string), but got ${#_positionals[@]} (the last one was: '${_positionals[*]: -1}')." 1
}

assign_positional_args ()
{
	_positional_names=('_arg_env' '_arg_client' '_arg_module' )

	for (( ii = 0; ii < ${#_positionals[@]}; ii++))
	do
		eval "${_positional_names[ii]}=\${_positionals[ii]}" || die "Error during argument parsing, possibly an Argbash bug." 1
	done
}

parse_commandline "$@"
handle_passed_args_count
assign_positional_args

#echo "Region: $_arg_region"
#echo "Dept: $_arg_department"
#echo "Client: $_arg_client"
#echo "Env: $_arg_env"
#echo "Module: $_arg_module"

#------------------------------------------------------------------
# Set up internal variables from command line options

DEPT=$(echo ${_arg_department} | awk '{print tolower($0)}')
DEPT_UPPER=$(echo "${DEPT}" | awk '{print toupper($0)}')
CLIENT=$(echo ${_arg_client} | awk '{print tolower($0)}')
ENV=$(echo ${_arg_env} | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
ENV_LOWER=$(echo ${ENV} | awk '{print tolower($0)}')
ENV_UPPER=$(echo ${ENV} | awk '{print toupper($0)}')
DIRECTORY=$(dirname $0)
REGION=${_arg_region}

# Defaults for KMS keys
MASTER_KEY="alias/connect-master-${ENV_LOWER}"
CALL_KEY="alias/connect-recordings-${ENV_LOWER}"
# KMS names for production
test "${ENV_LOWER}" == 'prod' && MASTER_KEY="alias/connect-master" && CALL_KEY="alias/connect-recordings"

modules=( customer-baseline )
test ${_arg_module} != 'all' && modules=( ${_arg_module} )

# ensure environment is one of dev/test/prod

#test ${ENV_LOWER} == 'dev' || test ${ENV_LOWER} == 'test' || test ${ENV_LOWER} == 'prod' || _PRINT_HELP=yes die "FATAL ERROR: Environment needs to be one of 'dev', 'test', 'prod'"

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
