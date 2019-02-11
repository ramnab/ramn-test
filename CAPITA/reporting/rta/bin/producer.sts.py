import boto3
import json

"""Simple script to send an event to the Agent Kinesis Stream"""

sts_client = boto3.client('sts', region_name='eu-central-1')
sts_response = sts_client.assume_role(
                                      RoleArn='arn:aws:iam::561300540183:role/CA_RTA',
                                      RoleSessionName='testing'
)


print("STS response: " + str(sts_response))

session = boto3.Session(
    aws_access_key_id=sts_response['Credentials']['AccessKeyId'],
    aws_secret_access_key=sts_response['Credentials']['SecretAccessKey'],
    aws_session_token=sts_response['Credentials']['SessionToken']
)

client = session.client('kinesis', region_name='eu-central-1')

payload = {
    "AWSAccountId": "443350248290",
    "AgentARN": "arn:aws:connect:eu-central-1:443350248290:instance/0b89d1f7-ab32-48f8-9870-67be7409181f/agent/7548134e-7c46-4898-9136-09f1b69fff53",
    "CurrentAgentSnapshot": {
        "AgentStatus": {
            "ARN": "arn:aws:connect:eu-central-1:443350248290:instance/0b89d1f7-ab32-48f8-9870-67be7409181f/agent-state/17559a2a-abc0-41f7-834c-a15fcde2be2a",
            "Name": "Available",
            "StartTimestamp": "2019-01-21T09:10:08.008Z"
        },
        "Configuration": {
            "AgentHierarchyGroups": 'null',
            "FirstName": "Tracy",
            "LastName": "Brown",
            "RoutingProfile": {
                "ARN": "arn:aws:connect:eu-central-1:443350248290:instance/0b89d1f7-ab32-48f8-9870-67be7409181f/routing-profile/618ec0df-0c99-44c8-b102-997bc2830d4a",
                "DefaultOutboundQueue": {
                    "ARN": "arn:aws:connect:eu-central-1:443350248290:instance/0b89d1f7-ab32-48f8-9870-67be7409181f/queue/0e23d0d0-9fa5-4422-9b49-ed356cfbf4c1",
                    "Name": "National Accounts"
                },
                "InboundQueues": [{
                    "ARN": "arn:aws:connect:eu-central-1:443350248290:instance/0b89d1f7-ab32-48f8-9870-67be7409181f/queue/b4da2122-0538-46b7-b271-6e1c78e6d1ff",
                    "Name": "Fraud"
                }, {
                    "ARN": "arn:aws:connect:eu-central-1:443350248290:instance/0b89d1f7-ab32-48f8-9870-67be7409181f/queue/ef261328-0843-448e-bb59-8417a6093f91",
                    "Name": "Fraud Internal"
                }, {
                    "ARN": "arn:aws:connect:eu-central-1:443350248290:instance/0b89d1f7-ab32-48f8-9870-67be7409181f/queue/0e23d0d0-9fa5-4422-9b49-ed356cfbf4c1",
                    "Name": "National Accounts"
                }, {
                    "ARN": "arn:aws:connect:eu-central-1:443350248290:instance/0b89d1f7-ab32-48f8-9870-67be7409181f/queue/fb4e9a0b-3100-48ff-aac4-c81786c1949d",
                    "Name": "National Accounts Internal"
                }, {
                    "ARN": "arn:aws:connect:eu-central-1:443350248290:instance/0b89d1f7-ab32-48f8-9870-67be7409181f/queue/agent/7548134e-7c46-4898-9136-09f1b69fff53",
                    "Name": 'null'
                }, {
                    "ARN": "arn:aws:connect:eu-central-1:443350248290:instance/0b89d1f7-ab32-48f8-9870-67be7409181f/queue/3cf4b107-8df3-495e-b557-b37e24d5decd",
                    "Name": "TracyBrown"
                }],
                "Name": "TracyBrown"
            },
            "Username": "P12288098"
        },
        "Contacts": []
    },
    "EventId": "145e8a1e-8c00-41d4-b5e3-d9e4ead754f9",
    "EventTimestamp": "2019-01-21T09:16:02.002Z",
    "EventType": "STATE_CHANGE",
    "InstanceARN": "arn:aws:connect:eu-central-1:443350248290:instance/0b89d1f7-ab32-48f8-9870-67be7409181f",
    "PreviousAgentSnapshot": {
        "AgentStatus": {
            "ARN": "arn:aws:connect:eu-central-1:443350248290:instance/0b89d1f7-ab32-48f8-9870-67be7409181f/agent-state/17559a2a-abc0-41f7-834c-a15fcde2be2a",
            "Name": "Available",
            "StartTimestamp": "2019-01-21T09:10:08.008Z"
        },
        "Configuration": {
            "AgentHierarchyGroups": 'null',
            "FirstName": "Tracy",
            "LastName": "Brown",
            "RoutingProfile": {
                "ARN": "arn:aws:connect:eu-central-1:443350248290:instance/0b89d1f7-ab32-48f8-9870-67be7409181f/routing-profile/618ec0df-0c99-44c8-b102-997bc2830d4a",
                "DefaultOutboundQueue": {
                    "ARN": "arn:aws:connect:eu-central-1:443350248290:instance/0b89d1f7-ab32-48f8-9870-67be7409181f/queue/0e23d0d0-9fa5-4422-9b49-ed356cfbf4c1",
                    "Name": "National Accounts"
                },
                "InboundQueues": [{
                    "ARN": "arn:aws:connect:eu-central-1:443350248290:instance/0b89d1f7-ab32-48f8-9870-67be7409181f/queue/b4da2122-0538-46b7-b271-6e1c78e6d1ff",
                    "Name": "Fraud"
                }, {
                    "ARN": "arn:aws:connect:eu-central-1:443350248290:instance/0b89d1f7-ab32-48f8-9870-67be7409181f/queue/ef261328-0843-448e-bb59-8417a6093f91",
                    "Name": "Fraud Internal"
                }, {
                    "ARN": "arn:aws:connect:eu-central-1:443350248290:instance/0b89d1f7-ab32-48f8-9870-67be7409181f/queue/0e23d0d0-9fa5-4422-9b49-ed356cfbf4c1",
                    "Name": "National Accounts"
                }, {
                    "ARN": "arn:aws:connect:eu-central-1:443350248290:instance/0b89d1f7-ab32-48f8-9870-67be7409181f/queue/fb4e9a0b-3100-48ff-aac4-c81786c1949d",
                    "Name": "National Accounts Internal"
                }, {
                    "ARN": "arn:aws:connect:eu-central-1:443350248290:instance/0b89d1f7-ab32-48f8-9870-67be7409181f/queue/agent/7548134e-7c46-4898-9136-09f1b69fff53",
                    "Name": 'null'
                }, {
                    "ARN": "arn:aws:connect:eu-central-1:443350248290:instance/0b89d1f7-ab32-48f8-9870-67be7409181f/queue/3cf4b107-8df3-495e-b557-b37e24d5decd",
                    "Name": "TracyBrown"
                }],
                "Name": "TracyBrown"
            },
            "Username": "P12288098"
        },
        "Contacts": [{
            "Channel": "VOICE",
            "ConnectedToAgentTimestamp": 'null',
            "ContactId": "e848581d-df3f-4096-af25-1abb4fa3cfc5",
            "InitialContactId": 'null',
            "InitiationMethod": "INBOUND",
            "Queue": {
                "ARN": "arn:aws:connect:eu-central-1:443350248290:instance/0b89d1f7-ab32-48f8-9870-67be7409181f/queue/0e23d0d0-9fa5-4422-9b49-ed356cfbf4c1",
                "Name": "National Accounts"
            },
            "QueueTimestamp": "2019-01-21T09:15:53.053Z",
            "State": "ERROR",
            "StateStartTimestamp": "2019-01-21T09:15:54.054Z"
        }]
    },
    "Version": "2017-10-01"
}

response = client.put_record(
    StreamName='ks-ccm-agent-events-dev',
    Data=json.dumps(payload),
    PartitionKey='capita-ccm-rta-producer'
)

print(response)
