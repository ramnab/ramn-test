# KCOM CAPITA DEPLOYMENTS

Detailed design: https://kcom-enterprise.atlassian.net/wiki/spaces/DEVOPS/pages/524878119/Detailed+Design


The code in this directory 'KCOM' is for internal use only and should not be shared with the customer.

`bin/setup.py`

Deploys a child or 'customer' account using a customer-specific config.

Individual resource stacks can be deployed individually by using the `--one` option.

Possible values for individual stacks are: 

- vpc
- subnets
- sg
- peering
- sqs
- s3
- ctr
- kms
- kinesis



