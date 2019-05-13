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

# Replace DEPARTMENT with ccm
# Replace ENV with dev / test / prod
./bin/deploy.sh DEPARTMENT ENV

```

## Adding new users, changing permissions for existing users

The helper script `bin/users.py` creates or updates RTA dashboard users.
Either create an individual user by providing the params on the command line
or specify a CSV file. See `config/users_v1.0.csv` for the current set of users.

Note that this script will update which clients the user can access if the user 
already exists.

Note that when adding a single user via the command line, the client list is comma
delimited. In the CSV file, the client list is space-delimited. The special client 
token `all` is used as a wildcard to allow the user access to all clients.

```bash
# to view all commands
python users.py --help

# to view help for a given command, for example 'create-user'
python users.py create-user --help

# to add / update a single user, note that CLIENTS must be comma-delimited
python users.py create-user --pool-id POOLID --username USERNAME --email EMAIL --clients CLIENTS 

# to add / update multiple users from a csv
python users.py create-user --pool-id POOLID --csv CSV

# to list all pools in current account
python users.py list-pools

# to list all users in a given user pool
python users.py list-users POOLID

# to export all users from the given user pool to a CSV file (can be used for importing)
python users.py list-users POOLID --export FILE

```
