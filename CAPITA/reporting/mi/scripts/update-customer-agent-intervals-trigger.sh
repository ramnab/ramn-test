#!/bin/bash


if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: update-customer-agent-intervals-trigger.sh <CLIENT> <ENV>"
    exit
fi

CLIENT=$1
ENV=$(echo $2 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
ENV_UPPER=$(echo $2 | awk '{print toupper($0)}')
ENV_LOWER=$(echo $2 | awk '{print tolower($0)}')

echo "Updating agent interval report trigger for client $CLIENT, env $ENV_UPPER"

aws lambda invoke --function-name lmbMiReportingModder-ccm-$ENV_UPPER \
                  --payload "{
  \"bucket\": \"s3-capita-ccm-connect-${CLIENT}-${ENV_LOWER}-reporting\",
  \"prefix\": \"reports/agent_interval/\",
  \"lambda\": \"lmbMIAgentInterval-ccm-${ENV_UPPER}\"
}" result.txt
