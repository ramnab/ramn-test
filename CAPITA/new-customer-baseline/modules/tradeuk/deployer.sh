#!/usr/bin/env bash

DIRECTORY=$(dirname $0)

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
