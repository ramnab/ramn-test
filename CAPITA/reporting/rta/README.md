# CAPITA RTA Application

Deployment instructions

## Pre-requisites

This solution uses a combination of cloudformation templates and SAM templates,
deployed using python-based tools and the aws framework.
The following set-up is recommended to follow the instructions below,
although the solution can be deployed by manual means.

1. AWS account - for admin access in target Common account
2. aws cli
3. cfn-square
4. awsume


The deployment script deploys the entire stack into Capita Common dev/test/prod environments.

```bash
# switch to the target account
awsume capita-common-nonprod

# Replace ENV with Dev / Test / Prod
./bin/deploy.sh ENV

```

## Adding new users, changing permissions

The helper script `bin/create_users.py` can create individual dashboard users or create
from a CSV file. If the user exists then the custom attribute 'client' is updated instead.

```bash
# to add / update a single user

python create_users.py --pool POOLID --username USERNAME --email EMAIL --clients CLIENTS 

# to add / update multiple users from a csv

python create_users.py --pool POOLID --file CSV

```
