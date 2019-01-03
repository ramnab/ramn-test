# Setting up the Capita Connect Environments

Setting up the environments takes a number of steps, some of which are dependent on each other. 

As a summary, you will need to

1. Set up the networking, common resources and active directory instance for the **common account**

2. Set up the networking for the target **customer account** (e.g. TradeUK Dev - `ccm-dev-tradeuk-connect`)

3. Create the VPC peering from **common account** to target **customer account**

4. Set up the routing in the **customer account** to allow routing to the common account


5. Set up the buckets, streams etc. in the **customer account** needed for Connect

<br>

**Note that steps 2-5 are now run via the helper python script**

> Switching between the accounts for deployment can easily be achieved using the python tool `awsume` https://github.com/trek10inc/awsume
>
> In the instructions below, the python tool  `cfn-square` https://github.com/KCOM-Enterprise/cfn-square is used

<br>

----
## 1. SET UP COMMON ACCOUNT

Instructions on setting up the Capita Common Environment used to host the managed Active Directory instance. 
This sets up the networking configuration (VPC, VPN Connection etc.), the secrets (KMS) key and the Active Directory instance, itself.

> Run all commands into **common account** , e.g. `ccm-prd-common-actvdir`


### Network Setup

Create the networking set up Active Directory in the *Capita Common Environment* (`ccm-prd-common-actvdir`) by running cfn-square in the target account as follows:

```bash
# AWS Account: ccm-prd-common-actvdir
# Directory: cloudformation/common-account/
cf sync network.stacks
```

<br>

### Common Resources (Secrets)

Create the Common resources - this needs to be completed **before** the AD instance stack is run, to provide a KMS key to encrypt the AD password:

```bash
# AWS Account: ccm-prd-common-actvdir
# Directory: cloudformation/common-account/
cf sync common.stacks
```

<br>

### Active Directory Instance
**Awaiting details from CAPITA-- do not deploy**


Use the KMS key to encrypt the password in the previous step to be used for the managed AD instance; the <KEY-ID> can be obtained via the console https://eu-central-1.console.aws.amazon.com/kms/home?region=eu-central-1#/kms/keys


```bash
# AWS Account: ccm-prd-common-actvdir
cf encrypt eu-central-1 <KEY-ID> <PASSWORD> 
```

The command will return the encrypted password, <ENCRYPTED-PASSWORD>

Update the file ad.stacks, replacing the parameter pADPassword with <ENCRYPTED-PASSWORD>

Create the managed AD instance as follows:

```bash
# AWS Account: ccm-prd-common-actvdir
# Directory: cloudformation/common-account/
cf sync ad.stacks
```

<br>

---
## FOR EACH CUSTOMER ACCOUNT

Steps 2 - 5 are currently via the `/bin/setup.py` command and can be run using the command from the root directory:

```bash
python3 bin/setup.py --config 'cloudformation/customer-account/tradeuk-dev.yaml' 
```

This runs ALL stacks - there are occassions where the stack status returns Null despite it actually being in progress. This may result in the script starting to deploy a dependent stack before it is complete. Individual stacks can be run by using the `--one` option, for example:

```bash
python3 bin/setup.py --config 'cloudformation/customer-account/tradeuk-dev.yaml' --one kinesis
```
Individual stack options are:
- vpc
- subnets
- sg - security groups
- peering - set up VPC peering with the Common account
- sqs - SQS for CTR upload via SFTP
- s3 - set up all buckets, other than CTR
- ctr - set up the CTR S3 bucket with the SQS notification trigger
- kms - connect master key
- kinesis - kinesis stream and firehose

-----
(Individual steps 2-5)
### 2. CONFIGURE FOR EACH CUSTOMER ACCOUNT

> Run all commands into **target customer account** , e.g. `ccm-dev-tradeuk-connect`

<br>

Each separate account needs the following networking set-up to be run, 
the account `ccm-dev-tradeuk-connect` is given here as an example.

```bash
# AWS Account: ccm-dev-tradeuk-connect
# Directory: cloudformation/customer-account/
cf sync tradeuk-dev-network.stacks
```

> **Make a note of the VPC ID and Peering Role that is returned as you'll need it for pairing next: see outputs  `oVpcId` and `oPeeringRole`**

<br>

----
### 3. SET UP VPC PEERING FOR EACH CUSTOMER ACCOUNT

> Run all commands into **common account** , e.g. `ccm-prd-common-actvdir`

For each customer account that has been configured with a VPC, run the appropriate stack config to peer the common account with the customer VPC.

First, replace the following parameters with the appropriate values from part 2 (Configure Customer Account):

1. `pPeerVpcID` - this is the customer VPC created in part 2, output `oVpcId`
2. `pPeerRoleArn` - this is the customer peering role created in part 2, output `oPeeringRole`
3. `pPeerAccountId` 

For example, for the account `ccm-dev-tradeuk-connect` account, run the following **in the common account**:

```bash
# AWS Account: ccm-prd-common-actvdir
# Directory: cloudformation/common-account/
cf sync vpc-peering-TradeUK-Dev.stacks
```

> **Make a note of the Peering Connection Identifier that is returned as you'll need it for setting up the routing for the customer accout next: see output  `oPeerConnectionId`**



<br>

----
### 4. SET UP ROUTING FOR EACH CUSTOMER ACCOUNT


> Run all commands into **target customer account** , e.g. `ccm-dev-tradeuk-connect`


Each separate account needs the routing to be wired in for the peer connection to the common account VPC (Active Directory instance). 

**You need the Peering Connection ID output from step 3 as  `oPeerConnectionId`.**

The account `ccm-dev-tradeuk-connect` is given here as an example.

Edit the parameter `pVPCPeeringConnectionId` in the .stacks file (`tradeuk-dev-ad-routing.stacks` in this instance) before running the following:



```bash
# AWS Account: ccm-dev-tradeuk-connect
# Directory: cloudformation/customer-account/
cf sync tradeuk-dev-ad-routing.stacks
```



<br>

----
### 5. SET UP CONNECT RESOURCES FOR EACH CUSTOMER ACCOUNT


> Run all commands into **target customer account** , e.g. `ccm-dev-tradeuk-connect`


Run the following set of stacks using the following command:

```bash
# AWS Account: ccm-dev-tradeuk-connect
# Directory: cloudformation/customer-account/
cf sync tradeuk-dev-connect.stacks
```

This will create the following:
- all S3 buckets (including the CTR bucket)
- call recording and master keys for Connect
- CTR Firehose and Agent Events Kinesis Stream and Firehose
