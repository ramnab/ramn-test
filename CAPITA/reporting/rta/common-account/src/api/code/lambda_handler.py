import json
import boto3
import logging
from botocore.exceptions import ClientError
import os


dynamodb = boto3.resource('dynamodb')
logger = logging.getLogger()
logger.setLevel(20)


def handler(event, context):
    """
    Handles API call from RTA dashboard

    """

    print("Called with event:" + json.dumps(event, indent=2))

    try:
        tablename = os.environ.get("ALARM_DB")
        items = get_current_alarms(tablename)
        # remove ttl
        for item in items:
            if item.get('ttl'):
                del item['ttl']

        return {
            "statusCode": 200,
            "body": json.dumps(items),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }
    except Exception as e:
        logger.error(e)
        return {
            "statusCode": 500,
            "body": str(e),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }


def get_current_alarms(tablename):
    '''Queries alarms db table for alarm states for specified usernames'''

    table = dynamodb.Table(tablename)
    try:
        response = table.scan()
        logger.info(f"get_current_alarms response={str(response)}")
        return response.get('Items', [])
    except ClientError as e:
        raise Exception(e)
