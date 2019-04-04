#!/bin/bash


if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ] || [ -z "$4" ]; then
    echo "Usage: update-customer-queue-intervals-trigger.sh CLIENT ENV SOLUTION TIME"
    echo "where SOLUTION is either 'queue' or 'agent'"
    echo "and TIME is either 'interval' or 'daily'"
    exit
fi

CLIENT=$1
ENV=$(echo $2 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
ENV_UPPER=$(echo $2 | awk '{print toupper($0)}')
ENV_LOWER=$(echo $2 | awk '{print tolower($0)}')
TIME=$4

SOL_LOWER=$(echo $3 | awk '{print tolower($0)}')
SOL_INIT_CAP=$(echo $3 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')

LAMBDA="lmbMI${SOL_INIT_CAP}Interval-ccm-${ENV_UPPER}"
PREFIX="connect/ccm-prd-${CLIENT}-connect/reports/${SOL_LOWER}_${TIME}/"
BUCKET="s3-capita-ccm-connect-${CLIENT}-${ENV_LOWER}-reporting"

echo "Adding trigger: reports to s3://${BUCKET}/${PREFIX} will trigger ${LAMBDA}"

aws lambda invoke --function-name lmbMiReportingModder-ccm-${ENV_UPPER} \
                  --payload "{\"bucket\": \"${BUCKET}\",\"prefix\": \"${PREFIX}\",\"lambda\": \"${LAMBDA}\"}" r.txt
