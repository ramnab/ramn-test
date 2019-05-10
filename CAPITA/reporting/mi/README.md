# Deploying MI

This solution is to be deployed across a COMMON account and a CUSTOMER account (e.g. tradeuk)

There are a number of inter-dependencies which means deployment needs to occur in a specific sequence.

## Prerequisites

1. awsume

2. aws cli

3. pipenv

4. python 3.6+


This solution can leverage pipenv for a consistant deployment environment.

To change to the correct environment use:

```bash
# in directory reporting/mi
pipenv shell

# first time use, install dependencies with
pipenv install
```

## 1. Deploy Common Resources

```bash
# in common account run:
./scripts/deploy-common.sh DEPARTMENT ENV
```

where 
* DEPARTMENT is the CAPITA department code, e.g. ccm
* ENV is one of dev/test/prod

## 2. Deploy Customer MI 

### 2.1. Include python dependencies for firehose-mod

```bash
# if not run already, go to project root mi/ and run
pipenv shell

# install the dependencies
cd src/firehose-mod/code/
pip install -r requirements.txt -t .
``` 

This will add the dependencies such as boto3 to the code/ directory

### 2.2 Deploy / Update MI

```bash
# in *appropriate* customer account:
scripts/deploy-customer.sh DEPARTMENT CLIENT ENV
```

where
* DEPARTMENT and ENV are as above
* CLIENT is the customer name, e.g. tradeuk

You can choose to deploy an individual module rather than the entire solution, using the folder
name of the module, for example:

```bash
scripts/deploy-customer.sh ccm firstgroup test agent-interval
```

**Please note that the mapping from S3 to lambda for Agent / Queue intervals
currently needs changing manually since occassionally the name of the connect
instance doesn't map onto our current naming convention, e.g. the dev instance
used for test, or the use of 'non-prod' in the name. See the deployer.sh scripts
for agent-interval and queue-interval respectively**


## 3. Update Common Reporting Bucket Permissions 

```bash
# in common account: 
cf sync -y --context transforms/config-ccm-common-<env>.yml \
   modules/base-common/reporting-bucket-policies.stacks
```

*Make sure that the file modules/base-common/resources/reporting-bucket-policies.yml
is up to date for the firehose roles in the appropriate customer accounts*
