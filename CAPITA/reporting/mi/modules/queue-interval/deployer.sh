#!/usr/bin/env bash

CLIENT=$1
ENV=$(echo $2 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
ENV_UPPER=$(echo $2 | awk '{print toupper($0)}')
ENV_LOWER=$(echo $2 | awk '{print tolower($0)}')

if [[ ${ENV_LOWER} = "prod" ]]; then
    LAMBDA_S3=s3-capita-ccm-${CLIENT}-prod-lambdas-eu-central-1
else
    LAMBDA_S3=s3-capita-ccm-${CLIENT}-nonprod-lambdas-eu-central-1
fi

DIRECTORY=`dirname $0`

echo """
----------------------------------------------------
                 Queue Intervals
                 ---------------

"""

echo """

         Deploying QI Lambda and Resources
         ---------------------------------

"""


# Get KMS ARN
KMS=$(python ${DIRECTORY}/../../scripts/get_kms_arn.py connect-master)

echo "KMS key = $KMS"

aws cloudformation package --region eu-central-1 \
                           --template-file ${DIRECTORY}/resources/queue-intervals.yml \
                           --s3-bucket ${LAMBDA_S3} \
                           --output-template-file deploy-queue-intervals.yml

aws cloudformation deploy --region eu-central-1 \
                          --template-file deploy-queue-intervals.yml \
                          --stack-name stCapita-MI-${ENV}-QueueIntervals  \
                          --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
                          --parameter-overrides \
                                pClient=${CLIENT} \
                                pEnvironment=${ENV_UPPER} \
                                pEnvironmentLowerCase=${ENV_LOWER} \
                                pDepartment=ccm \
                                pTransformationDb=gl_ccm_${ENV_LOWER} \
                                pCommonDestination=s3-capita-ccm-connect-common-${ENV_LOWER}-reporting \
                                pCustomerReportBucket=s3-capita-ccm-connect-${CLIENT}-${ENV_LOWER}-reporting \
                                pKMSArn=${KMS}


rm deploy-queue-intervals.yml

echo """

                 Updating QI Firehose
                 ---------------------

"""

aws lambda invoke --function-name lmbMiFirehoseModder-ccm-${ENV_UPPER} \
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


python ${DIRECTORY}/../../scripts/tag-firehose.py -f kfh-ccm-qi-${ENV_LOWER} \
                    -t sec:Compliance:Normal bus:BusinessUnit:ccm bus:ClientName:${CLIENT} \
                       tech:Environment:${ENV_LOWER} tech:ApplicationID:capita-ccm-connect \
                       tech:ApplicationRole:reporting



rm result.txt

echo """

              Updating QI Daily Firehose
              --------------------------

"""

aws lambda invoke --function-name lmbMiFirehoseModder-ccm-${ENV_UPPER} \
                  --payload "{
  \"debug\": true,
  \"ResourceProperties\": {
    \"FirehoseName\": \"kfh-ccm-qi-daily-${ENV_LOWER}\",
    \"Prefix\": \"queue_daily/clientname=${CLIENT}/rowdate=!{timestamp:yyyy-MM-dd}/\",
    \"ErrorPrefix\": \"errors/queue_daily/!{firehose:error-output-type}/clientname=${CLIENT}/rowdate=!{timestamp:yyyy-MM-dd}/\",
    \"TransformationDb\": \"gl_ccm_${ENV_LOWER}\",
    \"TransformationTable\": \"glt_queue_intervals_${ENV_LOWER}\",
    \"TransformationRole\": \"rl_mi_queue_interval_${ENV_LOWER}\"
  }
}" result.txt


python scripts/tag-firehose.py -f kfh-ccm-qi-daily-${ENV_LOWER} \
                    -t sec:Compliance:Normal bus:BusinessUnit:ccm bus:ClientName:${CLIENT} \
                       tech:Environment:${ENV_LOWER} tech:ApplicationID:capita-ccm-connect \
                       tech:ApplicationRole:reporting


rm result.txt

echo """

         Updating Customer Bucket trigger for QI
         ---------------------------------------

"""

aws lambda invoke --function-name lmbMiReportingModder-ccm-${ENV_UPPER} \
                  --payload "{
                    \"bucket\": \"s3-capita-ccm-connect-${CLIENT}-${ENV_LOWER}-reporting\",
                    \"prefix\": \"connect/ccm-prd-${CLIENT}-connect/reports/queue_interval/\",
                    \"lambda\": \"lmbMIQueueInterval-ccm-${ENV_UPPER}\"}" r.txt


echo """

      Updating Customer Bucket trigger for QI Daily
      ---------------------------------------------

"""

aws lambda invoke --function-name lmbMiReportingModder-ccm-${ENV_UPPER} \
                  --payload "{
                    \"bucket\": \"s3-capita-ccm-connect-${CLIENT}-${ENV_LOWER}-reporting\",
                    \"prefix\": \"connect/ccm-prd-${CLIENT}-connect/reports/queue_daily/\",
                    \"lambda\": \"lmbMIQueueInterval-ccm-${ENV_UPPER}\"}" result.txt


rm result.txt

echo """

                  queue interval: complete
----------------------------------------------------


"""
