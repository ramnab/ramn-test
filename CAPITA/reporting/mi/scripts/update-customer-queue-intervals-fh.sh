#!/bin/bash


if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: update-customer-agent-intervals-fh.sh <CLIENT> <ENV>"
    exit
fi

CLIENT=$1
ENV=$(echo $2 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
ENV_UPPER=$(echo $2 | awk '{print toupper($0)}')
ENV_LOWER=$(echo $2 | awk '{print tolower($0)}')

echo "Updating queue interval firehose for client $CLIENT, env $ENV_UPPER"

aws lambda invoke --function-name lmbMiFirehoseModder-ccm-$ENV_UPPER \
                  --payload "{
  \"debug\": true,
  \"ResourceProperties\": {
    \"FirehoseName\": \"kfh-ccm-qi-${ENV_LOWER}\",
    \"Prefix\": \"queue_interval/clientname=${CLIENT}/rowdate=!{timestamp:yyyy-MM-dd}/\",
    \"ErrorPrefix\": \"errors/queue_interval/!{firehose:error-output-type}/clientname=${CLIENT}/rowdate=!{timestamp:yyyy-MM-dd}/\",
    \"TransformationDb\": \"gl_ccm_${ENV_LOWER}\",
    \"TransformationTable\": \"glt_queue_intervals_${ENV_LOWER}\",
    \"TransformationRole\": \"rl_mi_queue_interval_${ENV_LOWER}\"
  }
}" result.txt

echo "Adding tags to firehose kfh-ccm-qi-${ENV_LOWER}"

python scripts/tag-firehose.py -f kfh-ccm-qi-${ENV_LOWER} \
                    -t sec:Compliance:Normal bus:BusinessUnit:ccm bus:ClientName:${CLIENT} \
                       tech:Environment:${ENV_LOWER} tech:ApplicationID:capita-ccm-connect \
                       tech:ApplicationRole:reporting
