#!/usr/bin/env bash

CLIENT=$1
ENV=$(echo $2 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
ENV_LOWER=$(echo $2 | awk '{print tolower($0)}')
ENV_UPPER=$(echo $2 | awk '{print toupper($0)}')

DIRECTORY=`dirname $0`

echo """
----------------------------------------------------
                tradeuk patching
                -----------------

        Deploying:
            - Call Recordings Bucket

"""

cf sync -y --context ${DIRECTORY}/../../transforms/config-deployer.yml ${DIRECTORY}/tradeuk.stacks



echo """

              customer baseline: complete
----------------------------------------------------

"""