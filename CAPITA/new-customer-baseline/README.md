# New Customer Baseline

Creates a set of resources for Connect Solutions in
a new customer account.

Deploys the following resources in the target customer
account:

- Lambda Distribution Bucket
- Customer Reporting Bucket
- Call Recordings Bucket
- Agent Event Stream + Firehose
- Connect Master and Call Recordings Key


## Prerequisites

1. python 3.6+

2. aws cli - see https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html

3. awsume - see https://github.com/trek10inc/awsume

4. cfn-square - see https://github.com/KCOM-Enterprise/cfn-square

5. admin role in customer account that can be assumed

## Deployment

```bash
# Change to customer account
awsume CUSTOMER-PROFILE

# from project root directory, run
./scripts/deploy.sh DEPARTMENT CLIENT ENV

```

Where:
* *CUSTOMER-PROFILE* is the admin role profile name in aws credentials (see prerequisite 5, above), e.g. tradeuk
* *DEPARTMENT* is the CAPITA department, e.g. ccm
* *CLIENT* is the name of the client, e.g. tradeuk
* *ENV* is one of dev/test/prod

## Updating Connect

On completion, the deploy script will give instructions
on what settings to change in Connect, including:

* Call recordings bucket and encryption key
* Exported reports bucket, prefix and encryption key

*Note that CTR settings are updated as part of the deployment
of the MI solution*
