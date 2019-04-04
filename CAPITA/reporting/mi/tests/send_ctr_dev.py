import boto3

client = boto3.client('firehose', region_name='eu-central-1')

with open('samples/ctr/kfh-ccm-dev-tradeuk-connect-dev01-ctr-6-2019-01-30-15-12-43-b2cdd549-7133-4d71-a9f3-9f8cf1b6d611.json', 'r') as f:
    d = f.read()

response = client.put_record(DeliveryStreamName='kfh-ccm-ctr-dev',
                             Record={
                                'Data': d
                             })
print(response)
