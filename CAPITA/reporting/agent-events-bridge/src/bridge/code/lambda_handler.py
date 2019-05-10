"""Take in Amazon Connect agent stream,
enrich with Client name and send to
kinesis stream in common account"""

import base64
import json
import os
import boto3
import logging


logger = logging.getLogger()
# INFO = 20, DEBUG = 10
LOGGING_LEVEL = int(os.environ.get("LOGGING_LEVEL", "20"))
logger.setLevel(LOGGING_LEVEL)


def handler(event, _context):
    """Main Handler function"""
    connect_events = []
    records = event.get('Records', [])
    logger.info(f"Received {len(records)} records")
    for record in records:
        data = record.get('kinesis', {}).get('data', '')
        decoded = base64.b64decode(data).decode('utf8')
        connect_event = json.loads(decoded)

        if connect_event and not is_excluded_event(connect_event):
            logger.info(f"Adding event: {connect_event}")
            connect_event['ClientName'] = os.environ.get('Client_Name')
            connect_events.append(connect_event)

    kinesis_records = to_kinesis(connect_events)
    if kinesis_records:
        logger.info(f"Sending {len(kinesis_records)} records onwards")
        destination_role = os.environ.get('Common_Account_Role_ARN')
        session = switch_account(destination_role)
        stream_name = os.environ.get('Target_Stream_Name')
        logger.info(f"Payload to {stream_name}: {kinesis_records}")
        session.client('kinesis').put_records(
            Records=kinesis_records,
            StreamName=stream_name
        )
    else:
        logger.info(f"Sending zero records onwards")


def is_excluded_event(event):
    return event.get("EventType", "") == "HEART_BEAT"


def switch_account(role_arn):
    """Assume role in common account, return session information."""
    sts_client = boto3.client('sts')
    assume = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName='role_provisioner'
    )
    session = boto3.session.Session(
        aws_session_token=assume['Credentials']['SessionToken'],
        aws_access_key_id=assume['Credentials']['AccessKeyId'],
        aws_secret_access_key=assume['Credentials']['SecretAccessKey']
    )
    return session


def to_kinesis(events):
    """Creates input list of records for kinesis command"""
    records = []
    for event in events:
        record = {
            'Data': json.dumps(event),
            'PartitionKey': os.environ.get('Client_Name')
        }
        records.append(record)
    return records
