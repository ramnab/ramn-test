#!/usr/bin/env bash

if [[ -z "$1" ]] || [[ -z "$2" ]];
then
    echo """Usage: ./deploy-customer.sh CLIENT ENV [MODULE]

If no module is specified then all will be deployed

    """
    exit
fi


if [[ -z "$3" ]];
then
    modules=( base-customer ctr queue-interval agent-interval )
else
    modules=( $3 )
fi


ENV=$(echo $2 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
ENV_LOWER=$(echo $2 | awk '{print tolower($0)}')
CLIENT=$1

echo """

----------------------------------------------------
   Deploying MI Solution into Customer Account
   -------------------------------------------

            Account:     ${AWSUME_PROFILE}
            Client:      ${CLIENT}
            Environment: ${ENV_LOWER}
            Modules:     ${modules[@]}

"""

read -p "> Continue? (y/n) " cont
if [[ ${cont} != "y" ]]; then
    echo "Aborting..."
    exit
fi



do_deploy() {
   eval "${1} ${CLIENT} ${ENV_LOWER}"
}

for m in "${modules[@]}"
do
    r=".*/${m}/deployer\.sh"
    deployer=`find ./modules/ -type f -regex ${r}`
    do_deploy ${deployer}
done
