import boto3

client = boto3.client('kinesis', region_name='eu-west-2')

with open('samples/ctr/ctr-record-1.json', 'r') as f:
    d = f.read()

response = client.put_record(StreamName='ks-ccm-ctrs-dev',
                             Data=d,
                             PartitionKey='test'
                             )
print(response)
