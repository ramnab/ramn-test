# Deploying MI

This solution is to be deployed across a COMMON account and a CUSTOMER account (e.g. tradeuk)


There are a number of inter-dependencies which means deployment needs to occur in a specific sequence.



## 1. Create Common Reporting Bucket

```bash
# in common account: 
cf sync -y --context transforms/config-ccm-common-<ENV>.yml \
   modules/base-common/common-reporting-bucket.stacks
```

for example, to deploy the common reporting bucket for DEV:

```bash
cf sync -y --context transforms/config-ccm-common-dev.yml \
   modules/base-common/common-reporting-bucket.stacks
```

<br>

## 2. Deploy Reporting Baseline in Customer Account

### 2.1 Deploy the customer reporting bucket:

```bash
# in customer account, e.g. tradeuk
cf sync -y stacks-<client>/<env>/deploy-reporting-bucket.stacks
e.g. > cf sync -y stacks-tradeuk/dev/deploy-reporting-bucket.stacks
```

for example, to deploy the customer reporting bucket for tradeuk dev:
```bash
cf sync -y --context transforms/config-ccm-tradeuk-dev.yml \
   modules/base-customer/customer-reporting-bucket.stacks
```

### 2.2 Deploy the Firehose Modder:

```bash
# in customer account, e.g. tradeuk
scripts/customer-fh-modder.sh CLIENT ENV
```

for example, to deploy the customer Firehose modder in dev:

```bash
scripts/customer-tradeuk-ctr-modder-dev.sh tradeuk dev
```


### 2.3 Deploy Customer Glue DB:

```bash
# in customer account, e.g. tradeuk
cf sync -y --context transforms/config-ccm-<client>-<env>.yml \
   modules/base-customer/common-db.stacks
```

for example, to deploy the customer glue db in tradeuk dev:
```bash
cf sync -y --context transforms/config-ccm-tradeuk-dev.yml \
   modules/base-customer/common-db.stacks
```
<br>

## 3. Deploy CTR Solution:

```bash
# in customer account, e.g. tradeuk
cf sync -y --context transforms/config-ccm-<client>-<env>.yml \
   modules/base-customer/ctr-resources.stacks
```

for example, to deploy the CTR solution to tradeuk dev:
```bash
cf sync -y --context transforms/config-ccm-tradeuk-dev.yml \
   modules/base-customer/ctr-resources.stacks
```

### 3.1 Update CTR Firehose

(manual process for now - run lambda with)

```json
{
  "debug": true,
  "ResourceProperties": {
    "FirehoseName": "kfh-ccm-ctr-ENV",
    "Prefix": "contact_record/clientname=CLIENT/rowdate=!{timestamp:yyyy-MM-dd}/",
    "ErrorPrefix": "errors/contact_record/!{firehose:error-output-type}/clientname=CLIENT/rowdate=!{timestamp:yyyy-MM-dd}/",
    "TransformationDb": "gl_ccm_ENV",
    "TransformationTable": "glt_ctr_ENV",
    "TransformationRole": "arn:aws:iam::907290942892:role/rl_mi_ctr_ENV"
  }
}
```

for example, to deploy for tradeuk dev:

```json
{
  "debug": true,
  "ResourceProperties": {
    "FirehoseName": "kfh-ccm-ctr-dev",
    "Prefix": "contact_record/clientname=tradeuk/rowdate=!{timestamp:yyyy-MM-dd}/",
    "ErrorPrefix": "errors/contact_record/!{firehose:error-output-type}/clientname=tradeuk/rowdate=!{timestamp:yyyy-MM-dd}/",
    "TransformationDb": "gl_ccm_dev",
    "TransformationTable": "glt_ctr_dev",
    "TransformationRole": "arn:aws:iam::907290942892:role/rl_mi_ctr_dev"
  }
}
```


<br>

## 4. Update the Common Reporting Bucket Permissions

```bash
# in common account: 
cf sync -y --context transforms/config-ccm-common-<env>.yml \
   modules/base-common/reporting-bucket-policies.stacks
```

for example, to deploy to common dev:
```bash
cf sync -y --context transforms/config-ccm-common-dev.yml \
   modules/base-common/reporting-bucket-policies.stacks
```

<br>

## 5. Create Common Athena User and DB

```bash
# in common account:
scripts/common-athena.sh ENV
```

for example, to create the athena user in common account dev:
```bash
scripts/common-athena-dev.sh dev
```

TODO: Create Athena CTR table in COMMON

<br>

## 6. Deploy MI Queue Interval Solution 

This section deploys the MI Queue Interval Solution. Note that the reporting bucket updates
for both the customer and common accounts are to be merged with the Agent Interval 
solution once in place.

There are three steps to this solution: 
1. The QI Lambda, Firehose and supporting infrastructure in the customer account
2. Updating the customer reporting bucket to trigger the QI lambda
3. Updating the common reporting bucket to allow the QI Firehose to write to it

<br>

### 6.1 Deploy QI Lambda to Customer Account

```bash
# in customer account
scripts/customer-queue-intervals.sh CLIENT ENV
```

for example, to deploy to tradeuk dev:
```bash
scripts/customer-queue-intervals.sh tradeuk dev
```

#### 6.1.1 Update the firehose config

Currently a manual step - this will be run as a custom resource

Go to the lmbQueueInterval-ccm-ENV lambda in the AWS Console and run the following test event:

Example for dev environment:
```json
{
  "debug": true,
  "ResourceProperties": {
    "FirehoseName": "kfh-ccm-qi-dev",
    "Prefix": "reports/queue_interval/",
    "TransformationDb": "gl_ccm_dev",
    "TransformationTable": "glt_queue_intervals_dev",
    "TransformationRole": "arn:aws:iam::907290942892:role/rl_mi_queue_interval_dev"
  }
}
``` 

<br>

### 6.2 Update Customer Reporting Bucket Notifications

#### 6.2.1 Deploy Customer Reporting Bucket Modder

(note that this will merge with Agent intervals)

```bash
# in customer account
scripts/customer-bucket-modder.sh CLIENT ENV
```

for example, to update for tradeuk dev:
```bash
scripts/customer-bucket-modder.sh tradeuk dev
```

#### 6.2.2 Update Notification policy

(currently a manual job)
Go to the console for the lambda function and test with the following event:

```json
{
  "bucket": "s3-capita-ccm-connect-CLIENT-ENV-reporting",
  "prefix": "reports/queue_interval/",
  "lambda": "arn:aws:lambda:eu-central-1:907290942892:function:lmbQueueInterval-ccm-ENV"
}
```

for example to update for tradeuk, dev:
```json
{
  "bucket": "s3-capita-ccm-connect-tradeuk-dev-reporting",
  "prefix": "reports/queue_interval/",
  "lambda": "arn:aws:lambda:eu-central-1:907290942892:function:lmbQueueInterval-ccm-DEV"
}
```

<br>

### 6.3 Update Common Reporting Bucket Policy

(note that this will merge with Agent intervals)

```bash
# in common account
cf sync -y --context transforms/config-ccm-common-ENV.yml \
   modules/base-common/reporting-bucket-policies.stacks
```

for example, to update for dev:
```bash
# in common account
cf sync -y --context transforms/config-ccm-common-dev.yml \
   modules/base-common/reporting-bucket-policies.stacks
```
