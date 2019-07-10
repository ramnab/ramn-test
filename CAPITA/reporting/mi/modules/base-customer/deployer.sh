#!/usr/bin/env bash

REGION=$1
DEPT=$2
CLIENT=$3
ENV=$(echo $4 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
ENV_UPPER=$(echo ${ENV} | awk '{print toupper($0)}')
ENV_LOWER=$(echo ${ENV} | awk '{print tolower($0)}')

DIRECTORY=$(dirname $0)

getStackOutput () {
    STACKNAME=$1
    KEY=$2
    aws cloudformation describe-stacks --query "Stacks[?StackName == '${STACKNAME}'].Outputs[]| [?OutputKey=='${KEY}'].[OutputValue] | [0]" --output text
}

echo """
----------------------------------------------------
                  base-customer
                  -------------

"""


echo """
          Deploying Firehose Modder Lambda
          --------------------------------

"""

LAMBDA_S3=s3-capita-${DEPT}-connect-${CLIENT}-${ENV_LOWER}-lambdas-${REGION}


aws cloudformation package --region ${REGION} \
                           --template-file ${DIRECTORY}/resources/fh-modder.yml \
                           --s3-bucket ${LAMBDA_S3} \
                           --output-template-file deploy-fh-modder.yml

aws cloudformation deploy --region ${REGION} \
                          --template-file deploy-fh-modder.yml \
                          --stack-name stCapita-MI-${ENV}-FirehoseModder  \
                          --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
                          --parameter-overrides \
                                pClient=${CLIENT} \
                                pEnvironment=${ENV_UPPER} \
                                pEnvironmentLowerCase=${ENV_LOWER} \
                                pDepartment=${DEPT}

rm deploy-fh-modder.yml


echo """

            Create Customer Glue Database
            ------------------------------

"""

cf sync -y --context ${DIRECTORY}/../../transforms/config-customer-deployer.yml \
        ${DIRECTORY}/common-db.stacks





echo """

             Deploy Customer Bucket Modder
             -----------------------------

"""

aws cloudformation package --region ${REGION} \
                           --template-file ${DIRECTORY}/resources/customer-reporting-modder.yml \
                           --s3-bucket ${LAMBDA_S3} \
                           --output-template-file deploy-customer-reporting-modder.yml

aws cloudformation deploy --region ${REGION} \
                          --template-file deploy-customer-reporting-modder.yml \
                          --stack-name stCapita-MI-${ENV}-ReportingBucketModder  \
                          --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
                          --parameter-overrides \
                                pClient=${CLIENT} \
                                pEnvironment=${ENV_UPPER} \
                                pEnvironmentLowerCase=${ENV_UPPER} \
                                pDepartment=${DEPT} \
                                pCustomerReportingBucketArn=arn:aws:s3:::s3-capita-${DEPT}-connect-${CLIENT}-${ENV_LOWER}-reporting


rm deploy-customer-reporting-modder.yml


echo """

        Creating Cross-Account Role for Firehose
        ----------------------------------------

"""

cf sync -y --context ${DIRECTORY}/../../transforms/config-customer-deployer.yml \
        ${DIRECTORY}/cross-account-firehose-role.stacks

cross_account_role=$(getStackOutput stCapita-MI-${ENV}-CrossAccountRole oCrossAccountRoleArn)
echo """
    * Remember to add the following role to the bucket policy for
        s3-capita-${DEPT}-connect-common-${ENV_LOWER}-reporting

        ${cross_account_role}

"""

echo """

                  base-customer: complete
----------------------------------------------------


"""
