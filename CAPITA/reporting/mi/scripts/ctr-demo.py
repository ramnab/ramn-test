from pathlib import Path
from time import sleep
import boto3
import json


client = boto3.client('firehose', region_name='eu-central-1')

'''Feed in a set of records into CTR from existing files'''

dir_src = "../../../../../../Downloads/capita-connect/tradeuk5/12/"

pathlist = Path(dir_src).glob("**/TradeUK*")
max_count = 1000
sent_count = 0

for path in pathlist:
    print(f"Reading {str(path)}")
    with open(path, 'r') as f:
        for line in f:
            if line:
                try:
                    d = json.loads(line)
                    client.put_record(DeliveryStreamName='kfh-ccm-ctr-test',
                                      Record={
                                         'Data': json.dumps(d)
                                      })
                    print(f"Sending: {line}")
                    sent_count += 1
                    max_count -= 1
                    if max_count == 0:
                        print(f"\nSent {sent_count} records")
                        exit()
                    sleep(2)

                except Exception as e:
                    print(f"Exception in data: {e}")
    sleep(5)
print(f"\nSent {sent_count} records")
