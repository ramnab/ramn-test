# CAPITA RTA Application

*This document is updated as RTA tasks are completed*

## 0. Environment set-up

This solution uses a combination of cloudformation templates and SAM templates, deployed using python-based tools and the aws framework. The following set-up is recommended to follow the instructions below, although the solution can be deployed by manual means.

### AWS CLI Account Access

The solution requires deployment of resources into target AWS accounts. This requires CLI account access from the accounts themselves; on the deployment machine, the aws cli should be installed and configured for the AWS accounts that will be deployed to.

#### 1. Set-up access to accounts
In the case where there is a single credentials account that allows access to the deployment account, create an access key for the user in question (AWS Console -> IAM -> Users -> Security Credentials tab). The Access Key ID and Secret Access Key should be stored safely as they will be used later on.

In each deployment account, you should already have a role defined that allows admin access from anyone that has authorised through the credentials account. For example, the TradeUK Dev account has the role TradeUK_Dev_Admin. The ARN of this will be used later to configure the AWS CLI.

#### 2. Install AWS CLI
Install AWS CLI by following the instructions at https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html


#### 3. Configure account access for the CLI
The Access Key ID and Secret Access Key can be used to configure access using the following command:

```bash
aws configure --profile capita
```

This will prompt you for the ID and Secret, along with a range of optional default settings. The configuration will be stored under the profile 'capita'

To add access to the deployment accounts, you can edit the file ~/aws/config and add a profile for each account, as the following example demonstrates for TradeUK Dev account:

```
[profile capita-tradeuk-dev]
region=eu-central-1
source_profile=capita
role_arn=arn:aws:iam::907290942892:role/TradeUK_Dev_Admin
```



### CFN Square

CFN-Square is utility to deploy CloudFormation templates with a few handy features...

### Awsume

Awsume is a utility for easily switching between AWS accounts/Roles in the command line. Install via the instructions at https://github.com/trek10inc/awsume

Further details are available at https://www.trek10.com/blog/awsume-aws-assume-made-awesome/

Awsume uses the configuration at ~/.aws/ to switch roles, so ensure the profiles have been set up. From the TradeUK Dev profile example above, to switch to this account, run:

```sh
awsume capita-common-nonprod

```

For set up on a Windows machine using Linux sub-system, if you get the error message `error: command 'x86_64-linux-gnu-gcc' failed with exit status 1` try installing the correct python-dev package first.

```
sudo apt-get install python3.6-dev
sudo pip install awsume
```

<br>

# Automated Deployment Script

The deployment script deploys the entire stack into Capita Common dev/test/prod environments.

```bash
# switch to the target account
awsume capita-common-nonprod

# Replace ENV with Dev / Test / Prod
./bin/deploy.sh <ENV>

```

# Individual Steps

## 1. Identity Management, Dashboard CDN and Bucket

Run DEPLOYMENT SCRIPT 1 to create:
* a Cognito User Pool and the association with the client (web app) 
* Dashboard CDN and bucket

## 2. Verify    

Create the Verify stack, run DEPLOYMENT SCRIPT 2.

## 3. RTA

Create the RTA application, run DEPLOYMENT SCRIPT 3.

## 4. API

Create API resources and lambda, run DEPLOYMENT SCRIPT 4.

## 5. Dashboard

Update the HTML for the web application by running DEPLOYMENT SCRIPT 5 below.

<br>

________
## DEPLOYMENT SCRIPT 1

```bash
# Switch to the appropriate account to deploy to, e.g. 'dev'
awsume dev

# Run the config file for the appropriate environment
cf sync deploy-dev.stacks
```

*Note that the -dev.stacks configuration file deploys using the 'DEV' environment tag.*
______



## DEPLOYMENT SCRIPT 2: Verify

* DEPLOY-BUCKET is the s3 bucket name part from DEPLOYMENT SCRIPT 1, output `oLambdaDeploymentBucketArn`
* SCHEDULE-BUCKET is the output `oAgentScheduleBucket`, e.g. s3-capita-ccm-common-dev-rta-agentschedules
* ENV and ENV-LOWERCASE are the environments, e.g. 'Dev' and 'dev', respectively
* DEPT is the department code, lowercase, e.g. 'ccm'
* INPUT-ARN is the S3 bucket where the schedules are uploaded, from the 
* OUTPUT-ARN is the S3 bucket where the processed schedules are uploaded
* OUTPUT-PATH is the key for the processed schedules
* ALARM-CFG is the key to the alarm config file

```bash

aws cloudformation package --region eu-central-1 --template-file templates/verify.yml \
                           --s3-bucket <DEPLOY-BUCKET> \
                           --output-template-file deploy-verify.yml

aws cloudformation deploy  --region eu-central-1 --template-file deploy-verify.yml \
                           --stack-name stCapita-RTA-<ENV>-Verify \
                           --capabilities CAPABILITY_IAM \
                           --parameter-overrides \
                                pInputBucketArn=<INPUT-ARN> \
                                pOutputBucketArn=<OUTPUT-ARN> \
                                pOutputFilePath=<OUTPUT-PATH> \
                                pAlarmConfigFilePath=<ALARM-CFG> \
                                pEnvironment=<ENV> \
                                pEnvironmentLowerCase=<ENV-LOWERCASE> \
                                pDepartment=ccm

```


## DEPLOYMENT SCRIPT 3: RTA App

* DEPLOY-BUCKET is the s3 bucket name part from DEPLOYMENT SCRIPT 1, output `oLambdaDeploymentBucketArn`
* SCHEDULE-BUCKET is the output `oAgentScheduleBucket`, e.g. s3-capita-ccm-common-dev-rta-agentschedules
* ENV and ENV-LOWERCASE are the environments, e.g. 'Dev' and 'dev', respectively
* DEPT is the department code, lowercase, e.g. 'ccm'

```bash

aws cloudformation package --region eu-central-1 --template-file templates/rta.yml \
                           --s3-bucket <DEPLOY-BUCKET> \
                           --output-template-file deploy-rta.yml

aws cloudformation deploy  --region eu-central-1 --template-file deploy-rta.yml \
                           --stack-name stCapita-RTA-<ENV>-App \
                           --capabilities CAPABILITY_IAM \
                           --parameter-overrides \
                                pAgentSchedule=s3://<SCHEDULE-BUCKET>/processed/schedule.json \
                                pEnvironment=<ENV> \
                                pEnvironmentLowerCase=<ENV-LOWERCASE> \
                                pDepartment=ccm

```


## DEPLOYMENT SCRIPT 4: API

* DEPLOY-BUCKET is the s3 bucket name part from DEPLOYMENT SCRIPT 1, output `oLambdaDeploymentBucketArn`
* COGNITO-ARN is the Arn for the Cognito User Pool, output `oUserPoolArn`
* ENV and ENV-LOWERCASE are the environments, e.g. 'Dev' and 'dev', respectively
* DEPT is the department code, lowercase, e.g. 'ccm'
* ALARMDB is the name of the DynamoDB table created in deployment script 2 (APP), output `oRtaAlarmsDb`
* ALARMDB-ARN is the ARN of the DynamoDB table created in deployment script 2 (APP), output `oRtaAlarmsDbArn`

```bash

aws cloudformation package --region eu-central-1 --template-file templates/api.yml \
                           --s3-bucket <DEPLOY-BUCKET> \
                           --output-template-file deploy-api.yml

aws cloudformation deploy --region eu-central-1 \
                          --template-file deploy-api.yml \
                          --stack-name stCapita-RTA-<ENV>-Api \
                          --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
                          --parameter-overrides \
                                pUserPoolArn=<COGNITO-ARN> \
                                pEnvironmentLowerCase=<ENV-LOWERCASE> \
                                pEnvironment=<ENV> \
                                pDepartment=<DEPT> \
                                pRtaAlarmsDb=<ALARMDB> \
                                pRtaAlarmsDbArn=<ALARMDB-ARN>

```


_____


## DEPLOYMENT SCRIPT 5: HTML

#### 1. Update file html/js/config.js with the values from the stack outputs:


* userPoolClientId: use output oUserPoolClientId
* userPoolId: use output oUserPoolId


#### 2. Update the invoke_url with the REST API URL


To find the URL, run 

```bash
aws cloudformation describe-stacks --stack-name stCapita-RTA-Dev-API --query "Stacks[0].Outputs[0].OutputValue"
```

This will return the API-ID parameter to use as the API Invoke Url:

`https://<API-ID>.execute-api.eu-central-1.amazonaws.com/prod/rta`

For example, `https://baoc3xefbc.execute-api.eu-central-1.amazonaws.com/prod/rta`


#### 3. Deploy the HTML to the web bucket


```bash
# Switch to the appropriate account to deploy to, e.g. 'dev'
awsume dev

# Replace BUCKET with the bucket name for the web app
aws s3 sync html/. s3://<BUCKET>
```

______
