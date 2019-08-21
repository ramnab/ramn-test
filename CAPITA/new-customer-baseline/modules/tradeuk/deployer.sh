#!/usr/bin/env bash

DIRECTORY=$(dirname $0)

echo """
----------------------------------------------------
                tradeuk patching
                -----------------

        Deploying:
            - Call Recordings Bucket

"""

# look up appropriate key ID from alias
#KEY_ALIAS=$(grep master_key ${DIRECTORY}/../../transforms/config-deployer.yml | awk '{print $2}')
##KEY_ID=$(aws kms list-aliases --query "Aliases[?AliasName=='${KEY_ALIAS}'].TargetKeyId" --output text)
##
##echo "${KEY_ALIAS} => ${KEY_ID}"
##
##cat >> ${DIRECTORY}/../../transforms/config-deployer.yml <<EOL
##kms_key_id: ${KEY_ID}
##EOL

cf sync -y --context ${DIRECTORY}/../../transforms/config-deployer.yml ${DIRECTORY}/tradeuk.stacks



echo """

              customer baseline: complete
----------------------------------------------------

"""
