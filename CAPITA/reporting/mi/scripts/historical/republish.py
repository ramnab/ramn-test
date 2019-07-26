import argparse
import boto3
import re
import os
import json
from os import listdir
from os.path import isfile, join
import shutil
from time import sleep


class Account:
    def __init__(self, **kwargs):
        self.account_id = kwargs.get("id")
        self.role_arn = f"arn:aws:iam::{self.account_id}:role/" + kwargs.get("role")
        self.client_name = kwargs.get("client")


accounts = {
    'tradeuk-nonprod': Account(id='907290942892', role='tradeuk_connect_nonprod_admin', client='tradeuk'),
    'tradeuk-prod': Account(id='443350248290', role='tradeuk_connect_prod_admin', client='tradeuk')
}


def assume_role(rolename):
    if not accounts.get(rolename):
        raise Exception(f"Role not found for '{rolename}'")

    account = accounts.get(rolename)
    response = boto3.client('sts').assume_role(
        RoleArn=account.role_arn,
        RoleSessionName=f'{rolename}-session'
    )
    return {
        'aws_access_key_id': response["Credentials"]["AccessKeyId"],
        'aws_secret_access_key': response["Credentials"]["SecretAccessKey"],
        'aws_session_token': response["Credentials"]["SessionToken"]
    }


def parse(s3_url):
    m = re.match(r'^s3\:\/\/(.+?)\/(.+?)\/?$', s3_url)
    print(f"Bucket={m.group(1)}")
    print(f"Prefix={m.group(2)}")
    if m:
        return {
            "Bucket": m.group(1),
            "Prefix": m.group(2)
        }
    raise Exception(f"Incorrect S3 URL format: {s3_url}")


def download_events(rolename, source):
    s3_location = parse(source)
    if os.path.exists('tmp_events'):
        raise Exception("Tmp directory already exists, please delete first")
    os.mkdir('tmp_events')
    session_tokens = assume_role(rolename)
    download(session_tokens, s3_location)


def download(session_tokens, s3_location, token=None):

    args = {
        'Bucket': s3_location['Bucket'],
        'Prefix': s3_location['Prefix']
    }
    if token:
        args['ContinuationToken'] = token

    response = boto3.client('s3', **session_tokens).list_objects_v2(**args)

    bucket = boto3.resource('s3', **session_tokens).Bucket(s3_location['Bucket'])
    for item in response['Contents']:
        key = item['Key']
        filename = key[key.rfind('/')+1:]
        print(f"Downloading {key} to tmp_events/{filename}")
        bucket.download_file(item['Key'], f'tmp_events/{filename}')

    if response.get('ContinuationToken'):
        download(session_tokens, s3_location, response['ContinuationToken'])


def create_historical_firehose(account_name, prefix, day, env: str):
    account = accounts[account_name]
    session_tokens = assume_role(account_name)
    fh_client = boto3.client('firehose', **session_tokens)
    response = fh_client.create_delivery_stream(
        DeliveryStreamName=f'fh_historic_{env}',
        DeliveryStreamType='DirectPut',
        ExtendedS3DestinationConfiguration={
            'RoleARN': f"arn:aws:iam::{account.account_id}:role/CA_MI_{env.upper()}",
            'BucketARN': f"arn:aws:s3:::s3-capita-ccm-connect-common-{env}-reporting",
            'Prefix': f"{prefix}/clientname={account.client_name}/rowdate={day.replace('/', '-')}/",
            'BufferingHints': {
                "SizeInMBs": 128,
                "IntervalInSeconds": 60
            },
            'DataFormatConversionConfiguration': {
                'SchemaConfiguration': {
                    'RoleARN': f"arn:aws:iam::{account.account_id}:role/rl_mi_agent_events_{env}",
                    'DatabaseName': f"gl_ccm_{env}",
                    'TableName': f"glt_{prefix}_{env}",
                    'Region': 'eu-central-1'
                },
                "InputFormatConfiguration": {
                    "Deserializer": {
                        "OpenXJsonSerDe": {}
                    }
                },
                "OutputFormatConfiguration": {
                    "Serializer": {
                        "ParquetSerDe": {
                            "Compression": "SNAPPY",
                            "EnableDictionaryCompression": True
                        }
                    }
                },
                "Enabled": True
            }
        }
    )
    print(response)


def republish(rolename, firehose):
    session_tokens = assume_role(rolename)
    fh_client = boto3.client('firehose', **session_tokens)
    files = [f for f in listdir('tmp_events')
             if isfile(join('tmp_events', f))]
    for file in files:
        publish_file(fh_client, firehose, join('tmp_events', file))
        sleep(3)


def publish_file(fh_client, firehose, file):
    with open(file, 'r') as f:
        file_json = "[" + f.read().replace('}{', '},{') + "]"
        print(f"Republishing {len(file_json)} records from file {file}")
        records = chunks(json.loads(file_json), 500)
        for record_chunk in records:
            fh_client.put_record_batch(
                DeliveryStreamName=firehose,
                Records=[{'Data': json.dumps(record)} for record in record_chunk]
            )


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def cleanup(account_name, firehose):
    shutil.rmtree('tmp_events')
    session_tokens = assume_role(account_name)
    fh_client = boto3.client('firehose', **session_tokens)
    fh_client.delete_delivery_stream(DeliveryStreamName=firehose)


def wait_for_firehose(account_name, firehose):
    session_tokens = assume_role(account_name)
    fh_client = boto3.client('firehose', **session_tokens)
    wait_for_firehose1(fh_client, firehose)


def wait_for_firehose1(fh_client, firehose):
    response = fh_client.describe_delivery_stream(
        DeliveryStreamName=firehose
    )
    if response['DeliveryStreamDescription']['DeliveryStreamStatus'] == 'CREATING':
        print(f"{firehose} creating...")
        sleep(10)
        wait_for_firehose1(fh_client, firehose)
    print(f"{firehose} created.")


def main():
    parser = argparse.ArgumentParser(description='''
    Republishes a given day's events
    Usage:
        python republish.py [-r REGION] SOURCE SOURCE_ENV DEST DEST_ENV DAY
    
    For example: 
        python republish.py -r eu-central-1 tradeuk-prod prod tradeuk-nonprod test 2019/06/03
        
    Will republish the agent events from 2019/06/03 from tradeuk-prod to common test account
    using tradeuk-nonprod account

    ''')
    parser.add_argument('-r', '--region',
                        help='AWS Region',
                        default='eu-central')

    parser.add_argument('source', help=f'source account name, one of {accounts.keys()}', required=True)
    parser.add_argument('source_env', help=f'source environment: dev, test or prod', required=True)
    parser.add_argument('destination', help=f'destination account name, one of {accounts.keys()}', required=True)
    parser.add_argument('destination_env', help='destination environment: dev, test or prod', required=True)
    parser.add_argument('day', help='date in format YYYY/MM/DD', required=True)

    args = parser.parse_args()
    firehose_name = f'fh_historic_{args.env}'
    source_account = accounts[args.source]
    source_bucket = (f"s3://s3-capita-ccm-connect-{source_account.client_name}-{args.source_env}"
                     f"-reporting/raw-agentevents/{args.day}/")
    download_events(args.source, source_bucket)
    create_historical_firehose(args.source, 'agent_events', args.day, args.destination_env)
    wait_for_firehose(args.destination, firehose_name)
    republish(args.destination, firehose_name)
    cleanup('args.destination', firehose_name)


if __name__ == '__main__':
    main()
