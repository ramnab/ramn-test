"""Take in Amazon Connect agent stream, enrich slightly and output to common account stream"""
import base64
import json
import os
import boto3

def handler(event, __context):
    """Main Handler function"""
    events = []
    records = event.get('Records', [])
    for record in records:
        trigger = json.loads(
            base64.b64decode(record.get('kinesis', {}).get('data', '')).decode('utf8')
        )
        trigger['ClientName'] = os.environ.get('Client_Name')
        if trigger:
            events.append(trigger)

    recordsinput = build_records_input(events)

    remoterolearn = os.environ.get('Common_Account_Role_ARN')
    remotesession = switch_account(remoterolearn)
    remotekinesisclient = remotesession.client('kinesis')

    remotekinesisclient.put_records(
        Records=recordsinput,
        StreamName=os.environ.get('Target_Stream_Name')
    )


def switch_account(rolearn):
    """Assume role in common account, return session information."""
    stsclient = boto3.client('sts')
    assume = stsclient.assume_role(
        RoleArn=rolearn,
        RoleSessionName='Role_provisioner'
    )
    session = boto3.session.Session(
        aws_session_token=assume['Credentials']['SessionToken'],
        aws_access_key_id=assume['Credentials']['AccessKeyId'],
        aws_secret_access_key=assume['Credentials']['SecretAccessKey']
    )
    return session

def build_records_input(events):
    """Creates input list of records for kinesis command"""
    records = []
    for event in events:
        record = {}
        record['Data'] = json.dumps(event)
        record['PartitionKey'] = os.environ.get('Client_Name')
        records.append(record)
    return records
