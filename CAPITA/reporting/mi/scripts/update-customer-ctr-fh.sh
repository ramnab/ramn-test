#!/bin/bash


if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: update-customer-ctr-fh.sh <CLIENT> <ENV>"
    exit
fi

CLIENT=$1
ENV=$(echo $2 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
ENV_UPPER=$(echo $2 | awk '{print toupper($0)}')
ENV_LOWER=$(echo $2 | awk '{print tolower($0)}')

echo "Updating ctr firehose for client $CLIENT, env $ENV_UPPER"

aws lambda invoke --function-name lmbMiFirehoseModder-ccm-$ENV_UPPER \
                  --payload "{
  \"debug\": true,
  \"ResourceProperties\": {
    \"FirehoseName\": \"kfh-ccm-ctr-dev\",
    \"Prefix\": \"contact_record/clientname=${CLIENT}/rowdate=!{timestamp:yyyy-MM-dd}/\",
    \"ErrorPrefix\": \"errors/contact_record/!{firehose:error-output-type}/clientname=${CLIENT}/rowdate=!{timestamp:yyyy-MM-dd}/\",
    \"TransformationDb\": \"gl_ccm_${ENV_LOWER}\",
    \"TransformationTable\": \"glt_ctr_${ENV_LOWER}\",
    \"TransformationRole\": \"rl_mi_agent_interval_${ENV_LOWER}\"
  }
}" result.txt
