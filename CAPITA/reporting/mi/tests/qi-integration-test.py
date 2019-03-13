import boto3
from pathlib import Path

print(f"Sending a new CSV report to TRADE UK Dev")

s3 = boto3.client('s3')

cwd = Path(__file__).parents[0]

with open(cwd / 'queue_interval_test.csv', 'r') as f:
    response = s3.put_object(
        Body=f.read(),
        Bucket='s3-capita-ccm-connect-tradeuk-dev-reporting',
        Key='reports/queue_interval/queue_interval_test.csv'
    )
    print(f"Response:\n{response}")
