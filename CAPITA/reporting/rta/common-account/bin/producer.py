import boto3
import json

"""Simple script to send an event to the Agent Kinesis Stream"""

client = boto3.client('kinesis', region_name='eu-central-1')

# TradeUK Dev Connect kinesis stream
KINESIS_STREAM = 'str-ccm-dev-tradeuk-connect-dev01-agent-events'


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

payload = create(typ="LOGIN", username="P0001", ts="2019-01-21T07:33:00.012Z")

response = client.put_record(
    StreamName=KINESIS_STREAM,
    Data=json.dumps(payload),
    PartitionKey='capita-ccm-rta-producer'
)

print(response)
