# Deploying MI

This solution is to be deployed across a COMMON account and a CUSTOMER account (e.g. tradeuk)


There are a number of inter-dependencies which means deployment needs to occur in a specific sequence.



## 1 Create Common Reporting Bucket

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

## 2 Deploy Reporting Baseline in Customer Account

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
scripts/customer-<client>-ctr-modder-<env>.sh
```

for example, to deploy the customer Firehose modder in dev:

```bash
scripts/customer-tradeuk-ctr-modder-dev.sh
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

### 2.4 Deploy CTR Solution:

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


## 3 Update the Common Reporting Bucket Permissions

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

## 4 Create Common Athen User and DB

```bash
# in common account:
scripts/common-athena-<env>.sh
```

```bash
scripts/common-athena-dev.sh
```

TODO: Create Athena CTR table in COMMON