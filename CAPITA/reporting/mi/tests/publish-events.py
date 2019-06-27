import shutil
import boto3
from boto3.session import Session
import sys
import argparse
import os
from datetime import datetime
import json
from os import listdir
from os.path import isfile, join
from time import sleep
from progress.bar import PixelBar
import yaml


def load_conf(file):
    with open(file, 'r') as f:
        return yaml.safe_load(f.read())


def assume_role(arn, session_name):
    """aws sts assume-role --role-arn arn:aws:iam::00000000000000:role/example-role --role-session-name example-role"""

    client = boto3.client('sts')

    response = client.assume_role(RoleArn=arn, RoleSessionName=session_name)

    session = Session(aws_access_key_id=response['Credentials']['AccessKeyId'],
                      aws_secret_access_key=response['Credentials']['SecretAccessKey'],
                      aws_session_token=response['Credentials']['SessionToken'])

    client = session.client('sts')
    account_id = client.get_caller_identity()["Account"]
    print(f"Assumed role in account: {account_id}")
    return session


def get_ctrs(session, conf, hour):
    """Download the CTR records"""
    now = datetime.now()
    bucket = f"s3-capita-ccm-connect-{conf.get('client', 'tradeuk')}-{conf.get('source-env', 'prod')}-reporting"
    prefix = f"raw_ctr/{now.strftime('%Y/%m/%d/')}{hour}/"
    download_from_s3(session, bucket, prefix, "ctrs", conf.get("max-ctr-files", 1))


def get_agent_events(session, conf, hour):
    """Download the Agent Events records"""
    now = datetime.now()
    bucket = f"s3-capita-ccm-connect-{conf.get('client', 'tradeuk')}-{conf.get('source-env', 'prod')}-reporting"
    prefix = f"raw-agentevents/{now.strftime('%Y/%m/%d/')}{hour}/"
    download_from_s3(session, bucket, prefix, "agent_events", conf.get("max-agent-files", 1))


def publish_agent_events(session, conf):
    client = session.client('kinesis', conf.get("region", 'eu-central'))
    files = [f for f in listdir('agent_events') if isfile(join('agent_events', f))]
    stream = f'ks-ccm-agent-events-{conf.get("target-env", "test")}'
    print(f"\nPublishing agent events to {stream}")
    for i, file in enumerate(files):
        print(f"\nPublishing file {i+1} of {len(files)}: {file}")
        publish_file(client, stream, join('agent_events', file))
        sleep(1)


def publish_ctrs(session, conf):
    client = session.client('kinesis', conf.get("region", 'eu-central'))
    files = [f for f in listdir('ctrs') if isfile(join('ctrs', f))]
    stream = f'ks-ccm-ctrs-{conf.get("target-env", "test")}'
    print(f"\nPublishing ctrs to {stream}")
    for i, file in enumerate(files):
        print(f"Publishing file {i+1} of {len(files)}: {file}")
        publish_file(client, stream, join('ctrs', file))
        sleep(1)


def publish_file(kinesis_client, stream, file):
    with open(file, 'r') as f:
        t = "[" + f.read().replace("}{", "},{") + "]"
        records = json.loads(t)
        with PixelBar('Records in file: ', max=len(records)) as bar:
            for i, record in enumerate(records):
                publish(kinesis_client, stream, record)
                bar.next()


def publish(kinesis_client, stream, record):
    kinesis_client.put_record(StreamName=stream, Data=json.dumps(record), PartitionKey='kpub')


def download_from_s3(session, bucket, prefix, destination, max_files):
    """Downloads all files from a s3 location
    Adapted from https://stackoverflow.com/questions/31918960/boto3-to-download-all-files-from-a-s3-bucket
    """
    print(f"PREFIX: {prefix}")
    client = session.client("s3")
    resource = session.resource("s3")
    paginator = client.get_paginator('list_objects')
    if not os.path.exists(destination):
        os.mkdir(destination)
        print("Directory ", destination, " created ")
    for result in paginator.paginate(Bucket=bucket, Delimiter='/', Prefix=prefix):
        for file in result.get('Contents', [])[0:max_files]:
            key = file.get("Key", "")
            dest_path = os.path.join(destination, key[key.rfind("/")+1:])
            print(f"Downloading {file.get('Key')} to {dest_path}")
            resource.meta.client.download_file(bucket, file.get('Key'), dest_path)


def main():
    parser = argparse.ArgumentParser(description="""
Usage:
    python publish-events.py CONF HOUR   
    
Downloads CTR and Agent Events for a given hour from the SOURCE account
and publishes them to the ctr and agent events kinesis streams in the 
TARGET account.

Expected use is to download from PROD and upload to either DEV or TEST

Downloaded records are then deleted from local file system.

    """)
    parser.add_argument('conf', action="store")
    parser.add_argument('hour', action="store")

    args = parser.parse_args()

    conf = load_conf(args.conf)

    shutil.rmtree('ctrs', ignore_errors=True)
    shutil.rmtree('agent_events', ignore_errors=True)

    session = assume_role(conf['source-role'], 'source')
    get_ctrs(session, conf, args.hour)
    get_agent_events(session, conf, args.hour)

    session = assume_role(conf['target-role'], 'target')
    publish_agent_events(session, conf)
    publish_ctrs(session, conf)

    print("Cleaning up - deleting downloaded files")
    shutil.rmtree('ctrs', ignore_errors=True)
    shutil.rmtree('agent_events', ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
