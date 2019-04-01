#!/usr/bin/env bash


if [ -z "$1" ]; then
    echo "Usage: setup.sh <ENV>"
    exit
fi

CLIENT=$1

ENV=$(echo $2 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
ENV_UPPER=$(echo $2 | awk '{print toupper($0)}')
ENV_LOWER=$(echo $2 | awk '{print tolower($0)}')

if [ $ENV_LOWER = "prod" ]; then
    LAMBDA_S3=s3-capita-ccm-connect-common-prod-lambdas-eu-central-1
else
    LAMBDA_S3=s3-capita-ccm-${ENV_LOWER}-lambdas-eu-central-1
fi


echo "Deploying to ${CLIENT}, env $ENV_UPPER"

aws cloudformation package --region eu-central-1 --template-file modules/base-customer/resources/historic-intervals.yml \
                           --s3-bucket ${LAMBDA_S3} \
                           --output-template-file deploy-historic-agent-intervals.yml

aws cloudformation deploy --region eu-central-1 --template-file deploy-historic-agent-intervals.yml \
                          --stack-name stCapita-MI-${ENV}-HistoricAgentIntervals  \
                          --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
                          --parameter-overrides \
                                pEnvironment=${ENV_UPPER} \
                                pEnvironmentLowerCase=${ENV_LOWER} \
                                pDepartment=ccm \
                                pTransformationDb=gl_ccm_${ENV_LOWER} \
                                pTempDestination=s3-capita-ccm-connect-${CLIENT}-${ENV_LOWER}-reporting


aws lambda invoke --function-name lmbMiFirehoseModder-ccm-${ENV_UPPER} \
                  --payload "{
  \"debug\": true,
  \"ResourceProperties\": {
    \"FirehoseName\": \"kfh-ccm-historic-ai-${ENV_LOWER}\",
    \"TransformationDb\": \"gl_ccm_${ENV_LOWER}\",
    \"TransformationTable\": \"glt_agent_intervals_${ENV_LOWER}\",
    \"TransformationRole\": \"rl_mi_historic_${ENV_LOWER}\"
  }
}" result.txt


aws lambda invoke --function-name lmbMiFirehoseModder-ccm-${ENV_UPPER} \
                  --payload "{
  \"debug\": true,
  \"ResourceProperties\": {
    \"FirehoseName\": \"kfh-ccm-historic-qi-${ENV_LOWER}\",
    \"TransformationDb\": \"gl_ccm_${ENV_LOWER}\",
    \"TransformationTable\": \"glt_queue_intervals_${ENV_LOWER}\",
    \"TransformationRole\": \"rl_mi_historic_${ENV_LOWER}\"
  }
}" result.txt


aws lambda invoke --function-name lmbMiFirehoseModder-ccm-${ENV_UPPER} \
                  --payload "{
  \"debug\": true,
  \"ResourceProperties\": {
    \"FirehoseName\": \"kfh-ccm-historic-ctr-${ENV_LOWER}\",
    \"TransformationDb\": \"gl_ccm_${ENV_LOWER}\",
    \"TransformationTable\": \"glt_ctr_${ENV_LOWER}\",
    \"TransformationRole\": \"rl_mi_historic_${ENV_LOWER}\"
  }
}" result.txt
