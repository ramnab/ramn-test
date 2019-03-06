import boto3
from pathlib import Path
cwd = Path(__file__).parents[0]

print(f"cwd={cwd}")

fh = "kfh-ccm-ctr-test"
file = cwd / "samples/ctr/kfh-ccm-dev-tradeuk-connect-dev01-ctr-6-2019-01-30-15-12-43-b2cdd549-7133-4d71-a9f3-9f8cf1b6d611.json"
client = boto3.client('firehose', region_name='eu-central-1')

with open(file, 'r') as f:
    d = f.read()

print(f"\nSending to {fh}")
response = client.put_record(DeliveryStreamName=fh,
                             Record={
                                'Data': d
                             })
print(f"\nResponse: {response}")
