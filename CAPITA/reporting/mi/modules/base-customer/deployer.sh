#!/usr/bin/env bash

CLIENT=$1
ENV=$(echo $2 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
ENV_LOWER=$(echo $2 | awk '{print tolower($0)}')
ENV_UPPER=$(echo $2 | awk '{print toupper($0)}')

DIRECTORY=`dirname $0`

echo """
----------------------------------------------------
                  base-customer
                  -------------

"""

echo """

        Deploying Customer Reporting Bucket
        -----------------------------------

"""

cf sync -y --context ${DIRECTORY}/../../transforms/config-ccm-${CLIENT}-${ENV_LOWER}.yml \
         ${DIRECTORY}/customer-reporting-bucket.stacks





echo """

          Deploying Firehose Modder Lambda
          --------------------------------

"""

if [[ ${ENV_LOWER} = "prod" ]]; then
    LAMBDA_S3=s3-capita-ccm-${CLIENT}-prod-lambdas-eu-central-1
else
    LAMBDA_S3=s3-capita-ccm-${CLIENT}-nonprod-lambdas-eu-central-1
fi



aws cloudformation package --region eu-central-1 \
                           --template-file ${DIRECTORY}/resources/fh-modder.yml \
                           --s3-bucket ${LAMBDA_S3} \
                           --output-template-file deploy-fh-modder.yml

aws cloudformation deploy --region eu-central-1 \
                          --template-file deploy-fh-modder.yml \
                          --stack-name stCapita-MI-${ENV}-FirehoseModder  \
                          --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
                          --parameter-overrides \
                                pClient=${CLIENT} \
                                pEnvironment=${ENV_UPPER} \
                                pEnvironmentLowerCase=${ENV_LOWER} \
                                pDepartment=ccm

rm deploy-fh-modder.yml


echo """

            Create Customer Glue Database
            ------------------------------

"""

cf sync -y --context ${DIRECTORY}/../../transforms/config-ccm-${CLIENT}-${ENV_LOWER}.yml \
        ${DIRECTORY}/common-db.stacks





echo """

             Deploy Customer Bucket Modder
             -----------------------------

"""

aws cloudformation package --region eu-central-1 \
                           --template-file ${DIRECTORY}/resources/customer-reporting-modder.yml \
                           --s3-bucket ${LAMBDA_S3} \
                           --output-template-file deploy-customer-reporting-modder.yml

aws cloudformation deploy --region eu-central-1 \
                          --template-file deploy-customer-reporting-modder.yml \
                          --stack-name stCapita-MI-${ENV}-ReportingBucketModder  \
                          --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
                          --parameter-overrides \
                                pClient=${CLIENT} \
                                pEnvironment=${ENV_UPPER} \
                                pEnvironmentLowerCase=${ENV_UPPER} \
                                pDepartment=ccm \
                                pCustomerReportingBucketArn=arn:aws:s3:::s3-capita-ccm-connect-${CLIENT}-${ENV_LOWER}-reporting


rm deploy-customer-reporting-modder.yml

echo """

              Deploy Customer Agent Events
              ----------------------------

"""

aws cloudformation package --region eu-central-1 \
                           --template-file ${DIRECTORY}/resources/agent-events.yml \
                           --s3-bucket ${LAMBDA_S3} \
                           --output-template-file deploy-agent-events.yml

aws cloudformation deploy --region eu-central-1 --template-file deploy-agent-events.yml \
                          --stack-name stCapita-MI-${ENV}-AgentEvents  \
                          --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
                          --parameter-overrides \
                                pClient=${CLIENT} \
                                pEnvironment=${ENV_UPPER} \
                                pEnvironmentLowerCase=${ENV_LOWER} \
                                pDepartment=ccm \
                                pCustomerReportBucket=s3-capita-ccm-connect-${CLIENT}-${ENV_LOWER}-reporting

python ${DIRECTORY}/../../scripts/tag-firehose.py -f kfh-ccm-agent-events-${ENV_LOWER} \
                    -t sec:Compliance:PII bus:BusinessUnit:ccm bus:ClientName:${CLIENT} \
                       tech:Environment:${ENV_LOWER} tech:ApplicationID:capita-ccm-connect \
                       tech:ApplicationRole:reporting

rm deploy-agent-events.yml

echo """

                  base-customer: complete
----------------------------------------------------


"""