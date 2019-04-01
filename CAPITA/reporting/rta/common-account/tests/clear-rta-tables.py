import boto3
import argparse

client = boto3.client('kinesis', region_name='eu-central-1')
dynamodb = boto3.resource('dynamodb')


def clear_alarms_table():
    global alarms_table
    print("Clearing alarms table")
    response = alarms_table.scan(ConsistentRead=True)
    items = response.get("Items")
    with alarms_table.batch_writer() as batch:
        for item in items:
            batch.delete_item(Key={
                "username": item.get("username"),
                "alarmcode": item.get("alarmcode")
            })


def clear_status_table():
    global status_table
    print("Clearing status table")
    response = status_table.scan(ConsistentRead=True)
    items = response.get("Items")
    with status_table.batch_writer() as batch:
        for item in items:
            batch.delete_item(Key={
                "username": item.get("username"),
                "prop": item.get("prop")
            })

parser = argparse.ArgumentParser('''
Clear RTA Tables

usage:
    python clear-rta-tables.py --env <ENV>

ENV: which capita-common-nonprod env to use, dev or test, required

''')

parser.add_argument(
    '-e', '--env',
    help='''
Environment to target in capita-common: dev or test
''',
    required=True
)
args = parser.parse_args()
env = args.env
alarms_table = dynamodb.Table(f'rta-alarmsdb-ccm-{env}')
status_table = dynamodb.Table(f'rta-eventhistory-ccm-{env}')

clear_alarms_table()
clear_status_table()
