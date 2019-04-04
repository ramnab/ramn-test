#!/usr/bin/env bash

if [[ -z "$1" ]];
then
    echo """Usage: ./update-customer.sh ENV

    """
    exit
fi



ENV=$(echo $1 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
ENV_LOWER=$(echo $1 | awk '{print tolower($0)}')


echo """

--------------------------------------------------------
   Updating Common Account for a deployed MI Solution
   --------------------------------------------------

            Account:     ${AWSUME_PROFILE}
            Environment: ${ENV_LOWER}

"""

read -p "> Continue? (y/n) " cont
if [[ ${cont} != "y" ]]; then
    echo "Aborting..."
    exit
fi

echo "Updating bucket policy for bucket:
ensure that modules/base-common/resources/reporting-bucket-policies.yml is up to date"

cf sync -y --context transforms/config-ccm-common-${ENV_LOWER}.yml \
   modules/base-common/reporting-bucket-policies.stacks


