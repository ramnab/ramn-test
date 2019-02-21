import boto3
import json
from datetime import datetime

"""Simple script to send an event to the Agent Kinesis Stream"""

client = boto3.client('kinesis', region_name='eu-central-1')

# TradeUK Dev Connect kinesis stream
# KINESIS_STREAM = 'str-ccm-dev-tradeuk-connect-dev01-agent-events'
KINESIS_STREAM = 'ks-ccm-agent-events-test'


def create(**kwargs):
    return {
        "EventType": kwargs.get("typ"),
        "CurrentAgentSnapshot": {
            "Configuration": {
                "Username": kwargs.get("username"),
                "FirstName": kwargs.get("firstname", "Fred"),
                "LastName": kwargs.get("lastname", "Blogs")
            },
            "AgentStatus": {
                "Name": kwargs.get("status", "Available")
            }
        },
        "EventTimestamp": kwargs.get("ts")
    }

# shift starts at 2019-02-14T07:30
# BSE should fire if log in between 07:00 and 07:25
ts=datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
payload = create(typ="LOGIN", username="P0001",
                 ts=ts)

response = client.put_record(
    StreamName=KINESIS_STREAM,
    Data=json.dumps(payload),
    PartitionKey='capita-ccm-rta-producer'
)

print(response)
