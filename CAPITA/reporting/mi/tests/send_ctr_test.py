import boto3
from pathlib import Path
cwd = Path(__file__).parents[0]

print(f"cwd={cwd}")

fh = "kfh-ccm-ctr-test"
file = cwd / "samples/ctr/ctr-record-1.json"
client = boto3.client('firehose', region_name='eu-central-1')

with open(file, 'r') as f:
    d = f.read()

print(f"\nSending to {fh}")
response = client.put_record(DeliveryStreamName=fh,
                             Record={
                                'Data': d
                             })
print(f"\nResponse: {response}")
