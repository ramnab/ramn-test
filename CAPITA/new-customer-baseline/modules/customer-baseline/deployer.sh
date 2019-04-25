#!/usr/bin/env bash

DEPT=$1
CLIENT=$2
ENV=$(echo $3 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
ENV_LOWER=$(echo ${ENV} | awk '{print tolower($0)}')
ENV_UPPER=$(echo ${ENV} | awk '{print toupper($0)}')

DIRECTORY=`dirname $0`

echo """
----------------------------------------------------
                customer baseline
                -----------------

        Deploying:
            - Lambda Distribution Bucket
            - Customer Reporting Bucket
            - Call Recordings Bucket
            - Agent Event Stream + Firehose
            - Connect Master and Call Recordings Key

"""

cf sync -y --context ${DIRECTORY}/../../transforms/config-deployer.yml ${DIRECTORY}/deployment.stacks

echo "Tagging Agent Event Firehose..."
python ${DIRECTORY}/../../scripts/tag-firehose.py -f kfh-ccm-agent-events-${ENV_LOWER} \
                    -t sec:Compliance:PII bus:BusinessUnit:ccm bus:ClientName:${CLIENT} \
                       tech:Environment:${ENV_LOWER} tech:ApplicationID:capita-${DEPT}-connect \
                       tech:ApplicationRole:reporting
echo """

              customer baseline: complete
----------------------------------------------------

"""
