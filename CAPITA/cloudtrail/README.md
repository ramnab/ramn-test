# CAPITA CloudTrail

The following describes the CloudTrail setup for the CAPITA AWS Organisation.
Deploying the solution at the root (billing) account will lead to automatic
propagation to child accounts. 

There are currently no CloudWatch metrics or alarms set up, but they can be
readily added and sent via the SNS Topic created here. The topic ARN is stored
both as a stack output `oCloudWatchAlarmTopicArn` and the System Parameter
`/CAPITA/${pDepartment}/CloudWatch/SNSAlertTopicArn`

To deploy the solution, run:

```bash
# in target account (root/billing)
scripts/deploy.sh DEPARTMENT

# for example,
scripts/deploy.sh ccm

```

This will deploy the following resources:

Resource | Type | Purpose
--- | --- | ---
AccessLoggingS3Bucket | S3 Bucket | Capture CloudTrail bucket access
CloudTrailKMSKey | KMS Key | Encrypt logs
CloudTrailKMSKeyAlias | KMS Key Alias | Human-readable key alias
CloudTrailS3Bucket | S3 Bucket | For CloudTrail logs
CloudTrailS3BucketPolicy | S3 Bucket Policy | Bucket access policy
CloudWatchLogGroup | LogGroup | LogGroup for CloudWatch usage
CloudWatchLogGroupRole | IAM Role | Allow CloudTrail to write to logs
CloudTrail | CloudTrail Trail | CloudTrail Config
CloudWatchAlarmSNSTopic | SNS Topic | For future alarms
SSMParameterCloudWatchAlarmTopicArn | SSM Parameter | Parameter storing SNS Topic ARN
