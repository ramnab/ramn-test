#!/usr/bin/env bash

if [[ -z "$1" ]];
then
    echo """Usage: ./deploy-customer.sh ENV

    """
    exit
fi



ENV=$(echo $1 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
ENV_LOWER=$(echo $1 | awk '{print tolower($0)}')


echo """

----------------------------------------------------
     Deploying MI Solution into Common Account
     -----------------------------------------

            Account:     ${AWSUME_PROFILE}
            Environment: ${ENV_LOWER}

"""

read -p "> Continue? (y/n) " cont
if [[ ${cont} != "y" ]]; then
    echo "Aborting..."
    exit
fi



do_deploy() {
   eval "${1} ${ENV_LOWER}"
}

modules=( base-common )
for m in "${modules[@]}"
do
    r=".*/${m}/deployer\.sh"
    deployer=`find ./modules/ -type f -regex ${r}`
    do_deploy ${deployer}
done
