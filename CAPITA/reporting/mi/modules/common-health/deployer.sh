#!/usr/bin/env bash

REGION=$1
DEPT=$2
ENV=$(echo $3 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
ENV_UPPER=$(echo ${ENV} | awk '{print toupper($0)}')
ENV_LOWER=$(echo ${ENV} | awk '{print tolower($0)}')


LAMBDA_S3=s3-capita-ccm-connect-common-${ENV_LOWER}-lambdas-${REGION}
DIRECTORY=$(dirname $0)

echo """
----------------------------------------------------
          Healthcheck for Common Account
          ------------------------------

"""

echo """

    Deploying Healthcheck Lambda and Resources
    ------------------------------------------

"""
getStackOutput () {
    STACKNAME=$1
    KEY=$2
    aws cloudformation describe-stacks --query "Stacks[?StackName == '${STACKNAME}'].Outputs[]| [?OutputKey=='${KEY}'].[OutputValue] | [0]" --output text
}

REPORT_BUCKET=$(getStackOutput stCapita-MI-${ENV}-CommonReportingBucket oCommonReportingBucket)


aws cloudformation package --region ${REGION} \
                           --template-file ${DIRECTORY}/resources/health-checker.yml \
                           --s3-bucket ${LAMBDA_S3} \
                           --output-template-file deploy-healthchecker.yml

aws cloudformation deploy --region ${REGION} \
                          --template-file deploy-healthchecker.yml \
                          --stack-name stCapita-MI-${ENV}-Health \
                          --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
                          --parameter-overrides \
                                pEnvironment=${ENV_UPPER} \
                                pEnvironmentLowerCase=${ENV_LOWER} \
                                pDepartment=${DEPT} \
                                pClients=tradeuk \
                                pReportingBucket=${REPORT_BUCKET} \
                                pSchedule="cron(0/10 6-22 * * ? *)"


rm deploy-healthchecker.yml

cf sync -y --context ${DIRECTORY}/../../transforms/config-common-deployer.yml \
                     ${DIRECTORY}/common-health.stacks


echo """

            healthcheck common: complete
----------------------------------------------------


"""
