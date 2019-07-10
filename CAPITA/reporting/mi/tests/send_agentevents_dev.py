import boto3

client = boto3.client('kinesis', region_name='eu-central-1')

with open('samples/agent_events/agent-event-1.json', 'r') as f:
    d = f.read()

response = client.put_record(StreamName='ks-gc-agent-events-dev',
                             Data=d,
                             PartitionKey='test'
                             )
print(response)
