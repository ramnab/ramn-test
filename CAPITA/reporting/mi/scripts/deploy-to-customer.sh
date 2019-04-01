#!/usr/bin/env bash


# Deploy MI Solution to the Customer Account
#
# Prerequisits:
#     1. Common Reporting Bucket must be already deployed
#
#
# Ensure you are in the target account before running this script
# by using a tool such as 'awsume'

ENV=$(echo $1 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
ENV_LOWER=$(echo $1 | awk '{print tolower($0)}')
CLIENT=$2

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "
Usage:

    ./bin/deploy-to-customer.sh  ENV CLIENT
    
where ENV is the environment, e.g. 'Dev', 'Test', 'Prod'
(note the capitalisation)

and CLIENT is the client identifier, such as 'tradeuk'

** IMPORTANT: You need to switch to the target account
using a tool such as awsume before running this script **

"
    exit
fi

echo "Running into account: ${AWSUME_PROFILE}"
echo "Client ID: ${CLIENT}"
echo "Environment: ${ENV}"

echo ""
read -p "Continue? (y/n) " cont
if [ $cont != "y" ]; then
    echo "Aborting..."
    exit
fi

echo ""
echo "------------------------------------------"
echo "Deploying Customer Reporting Bucket"

cf sync -y --context transforms/config-ccm-${CLIENT}-${ENV_LOWER}.yml \
   modules/base-customer/customer-reporting-bucket.stacks


echo ""
echo "------------------------------------------"
echo "Deploying Firehose Modder Lambda"

scripts/customer-fh-modder.sh ${CLIENT} ${ENV}


echo ""
echo "------------------------------------------"
echo "Create Customer Glue Database"

cf sync -y --context transforms/config-ccm-${CLIENT}-${ENV_LOWER}.yml \
   modules/base-customer/common-db.stacks


echo ""
echo "------------------------------------------"
echo "Deploy Customer Reporting Bucket Modder Lambda"

scripts/customer-bucket-modder.sh ${CLIENT} ${ENV}

echo ""
echo "------------------------------------------"
echo "Deploy Customer Agent Events Kinesis Resources"

scripts/customer-agent-events.sh ${CLIENT} ${ENV}

echo ""
echo "------------------------------------------"
echo "Deploy CTR resources"

cf sync -y --context transforms/config-ccm-${CLIENT}-${ENV_LOWER}.yml \
   modules/base-customer/ctr-resources.stacks


echo ""
echo "------------------------------------------"
echo "Update the CTR Firehose"

scripts/update-customer-ctr-fh.sh ${CLIENT} ${ENV}


echo ""
echo "------------------------------------------"
echo "Deploy QI Lambda and Resources"

scripts/customer-queue-intervals.sh ${CLIENT} ${ENV}


echo ""
echo "------------------------------------------"
echo "Update the QI Firehose"

scripts/update-customer-queue-intervals-fh.sh ${CLIENT} ${ENV}


echo ""
echo "------------------------------------------"
echo "Update the Customer Bucket trigger for QI"

scripts/update-customer-bucket-trigger.sh ${CLIENT} ${ENV} queue


echo ""
echo "------------------------------------------"
echo "Deploy AI Lambda and Resources"

scripts/customer-agent-intervals.sh ${CLIENT} ${ENV}


echo ""
echo "------------------------------------------"
echo "Update the AI Firehose"

scripts/update-customer-agent-intervals-fh.sh ${CLIENT} ${ENV}


echo ""
echo "------------------------------------------"
echo "Update the Customer Bucket trigger for AI"

scripts/update-customer-bucket-trigger.sh ${CLIENT} ${ENV} agent


echo ""
echo "[Complete]"