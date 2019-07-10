# Amazon Connect Dashboard Metrics
Capita have a requirement for a real-time dashboard to display KPI metrics from the various Amazon Connect client
instances. The metrics will be displayed as a PowerBI dashboard. Due to the complexity of the Metrics API calls and 
responses and the need to support multiple clients, a script will be provide to retrieve the metrics and ingest them 
into PowerBI.

Two scripts are provided to support the solution:

* connectmetrics.py - A python script that invokes the `get_metric_data` and `get_current_metric_data` APIs and flattens
the results in JSON format.
* connect-metrics-cli.ps1 - A powershell wrapper that invokes the `connectmetrics.py` script and sends the results to
PowerBI.

## connectmetrics.py python script
The Amazon Connect API is currently limited in the functionality it provides; there is no option to enumerate the
Connect instances or queues. The Metrics API require the Connect instance Id and the Queue Ids to know what to query.

To work around this limitation, the `connectmetrics.py` script is driven by configuration files that hold this information,
if a new instance or queue is added, the configuration files will need to be updated to reflect the change.

The configuration files are in JSON format in the `config` directory and are named using the following convention:

`<AWS Profile Name>-instance-queues.json`, e.g. `capita-tradeuk-dev-instance-queues.json` 
 
The format of the file is detailed below.

```json
{
  "clientName": "<name of the client to identify the metrics in PowerBI, e.g. TradeUK>",
  "accountId": "<the id of the account to access>",
  "environment": "<the environment to connect to, either DEV, TEST or PROD>",
  "instanceId": "<connect instance GUID>",
  "queues": {
      "<Queue Id GUID>": "<Queue Name>",
      "<Queue Id GUID>": "<Queue Name>"
    }
}
```
For example:
```json
{
  "clientName": "TradeUK",
  "accountId": "111111111111",
  "environment": "DEV",
  "instanceId": "0d525d33-c2af-4b86-9d67-393db396e896",
  "queues": {
      "e42fa1d8-620e-4bf8-bd9a-eafc60b9c0ef": "BasicQueue"
    }
}
```

The script requires three arguments to run, the name of the client, the environment  and the AWS Profile to use to 
connect to the instance. The AWS Profile is used to look up the appropriate configuration and to authenticate with the 
Metrics API.

```powershell
python src\connectmetrics\code\connectmetrics.py --client <client> --environment <environment> --profile <profile>
```

For example:
```powershell
python src\connectmetrics\code\connectmetrics.py --client tradeuk --environment dev --profile capita-tradeuk-dev
```

The script outputs the metrics to an `output` directory which it will create if it does not already exist. The
output will be a JSON file with a flattened JSON structure. The file will be named using a similar convention
to the configuration file.

`.\output\<client name>-<environment>-metric-data.json`, e.g. `tradeuk-dev-metric-data.json`

The format of the file is shown below.

```json
[
  {
    "Date": "2019-04-30T10:44:13.032914",
    "Client": "TradeUK",
    "QueueName": "Customer Services",
    "Call": 0,
    "CONTACTS_HANDLED": 5,
    "Abandoned": 0,
    "Agents": 1,
    "AGENTS_ON_CALL": 0,
    "MaxOCW": 0,
    "InQueue": 0,
    "ACW": 0,
    "Available": 0
  },
  {
    "Date": "2019-04-30T10:44:13.032914",
    "Client": "TradeUK",
    "QueueName": "Collections",
    "Agents": 1,
    "AGENTS_ON_CALL": 0,
    "MaxOCW": 0,
    "InQueue": 0,
    "ACW": 0,
    "Available": 0
  }
]
```

## connect-metrics-cli.ps1 powershell script
This powershell script is a wrapper to the python script, that invokes the python script and pushes the 
resulting metrics to PowerBI. The script takes four arguments, the client name, the environment and the AWS Profile and
the endpoint for PowerBI.

```powershell
.\scripts\connect-metrics-cli.ps1 -Client tradeuk -Environment dev -ProfileName capita-tradeuk-dev -PowerBIUrl http://localhost:8080
```

### Cross Account Access
The API operates at the Amazon Connect instance level, that is, you invoke the API to retrieve metrics for the
queues associated with a specific Amazon Connect instance identifier.

To simplify the authentication to these different instances, the solution will make use of cross account access.
A user will be created that will have permissions to assume a role in the Client accounts. The role will grant
the user the `connect:GetCurrentMetricData` and `connect:GetMetricData` permissions.


#### AWS Credential Configuration
The following configuration should be defined in the AWS ~/.aws/credentials to facilitate the
cross account access.

##### Credentials
Credentials will be provided for each of the environments (dev, test and prod), these need to be added to the 
`credentials` file with a suitable key name, for example:


```ini
[capita-common-dashboard-dev]
aws_access_key_id = <access-key>
aws_secret_access_key = <secret-access-key>

[capita-common-dashboard-prod]
aws_access_key_id = <access-key>
aws_secret_access_key = <secret-access-key>
```

This user will have the relevant permission to assume the connect metric role in the client accounts. 

## Deploying the Dashboard resources

This solution is to be deployed across a COMMON account and a CUSTOMER account (e.g. tradeuk)

There are a number of inter-dependencies which means deployment needs to occur in a specific sequence.

### Prerequisites

1. awsume

2. aws cli

3. pipenv

4. python 3.6+


This solution can leverage pipenv for a consistent deployment environment.

To change to the correct environment use:

```bash
# in directory reporting/mi
pipenv shell

# first time use, install dependencies with
pipenv install
```

### 1. Deploy Common Resources

```bash
# in common account run:
./scripts/deploy-common.sh DEPARTMENT ENV
```

where 
* DEPARTMENT is the CAPITA department code, e.g. ccm
* ENV is one of dev/test/prod

### 2. Deploy Customer Cross account role 

```bash
# in *appropriate* customer account:
./scripts/deploy-customer.sh DEPARTMENT CLIENT ENV
```

where
* DEPARTMENT and ENV are as above
* CLIENT is the customer name, e.g. tradeuk

## Packaging the dashboard scripts for distribution
A script has been provided to generate a distribution package to provide to the MI team at Capita. To create the
packaged distribution, run the following script:
```bash
./scripts/package.sh
```

This will create a `./dist` folder containing the `connect-dashboard-metrics.zip` file for distribution.


