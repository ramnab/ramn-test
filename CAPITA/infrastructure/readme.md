# New Customer Baseline

Creates a set of resources for Connect Solutions in
a new customer account.

Deploys the following resources in the target customer
account:

- Lambda Distribution Bucket
- Customer Reporting Bucket
- Call Recordings Bucket
- Agent Event Stream
- Connect Master and Call Recordings Key


## Prerequisites

1. python 3.6+

2. aws cli - see https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html

3. awsume - see https://github.com/trek10inc/awsume

4. cfn-square - see https://github.com/KCOM-Enterprise/cfn-square

5. admin role in customer account that can be assumed

## Overview

The infrastructure area is designed for ad-hoc (potentially run once) modules. Modules that cannot fit
into the customer-baseline, mi or rta should go here. For example, the lambda function to alert on connect
ip range changes is here as it only needs to be run into a single account (common-non-prod).

For the moment, these modules won't be deployed by top level deployers, only the local deployer.

## Deployment

```bash
# Change to customer account
awsume CUSTOMER-PROFILE

From the infrastructure directory, cd into modules.
Locate the module you require (for example connect-ip-change-alerter).
Run the self-contained deployer.

# from project root directory, run
./scripts/deploy.sh DEPARTMENT CLIENT ENV

```

Where:
* *CUSTOMER-PROFILE* is the admin role profile name in aws credentials (see prerequisite 5, above), e.g. tradeuk
* *DEPARTMENT* is the CAPITA department, e.g. ccm
* *CLIENT* is the name of the client, e.g. tradeuk
* *ENV* is one of dev/test/prod

