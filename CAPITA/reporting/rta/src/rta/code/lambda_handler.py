import json
import base64
import logging
import re
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr
import os
from alarms import *


logger = logging.getLogger()
logger.setLevel(20)
s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')


def handler(event, context):
    """
    Handles Agent Events from Kinesis and calculates RTA alarm states

    """

    print("Called with event:" + json.dumps(event, indent=2))

    try:
        prepared_records = prepare_records(event.get("Records"))

        schedule_uri = os.environ.get("AGENT_SCHEDULE")
        (bucket, key) = split_s3(schedule_uri)
        schedule = read_schedule(bucket, key)

        tablename = os.environ.get("ALARM_DB")
        agents = list(prepared_records.keys())
        current_alarms = get_current_alarms(tablename, agents)

        recalculate_alarms(tablename,
                           schedule,
                           prepared_records,
                           current_alarms)

    except Exception as e:
        logger.error(e)

    return {}


def prepare_records(records):
    '''Decodes each kinesis record grouped by username'''
    prep = {}
    for record in records:
        data = record.get('kinesis', {}).get('data', '')
        event_as_str = base64.b64decode(data).decode('utf8')
        try:
            event = json.loads(event_as_str)
            logger.info(f"Event decoded to json: {event}")
            if event:
                username = get_username(event)
                if username:
                    if not prep.get(username):
                        prep[username] = []
                    prep[username].append(event)
        except json.JSONDecodeError:
            logger.error("Unable to decode json record from string: "
                         f"{event_as_string}")

    logger.info(f"Prepared records: {prep}")
    return prep


def read_schedule(bucket, key):
    '''Reads in JSON schedule from specified S3 bucket / key'''
    try:
        logger.info(f"Reading schedule from s3://{bucket}/{key}")
        schedule = s3.Object(bucket, key).get()['Body'].read().decode('utf-8')
        schedule_as_json = json.loads(schedule)
        logger.info(f"Schedule: {json.dumps(schedule_as_json)}")
        return schedule_as_json
    except ClientError as e:
        raise Exception(f"Cannot read schedule file from s3://{bucket}/{key}")


def get_current_alarms(tablename, usernames):
    '''Queries alarms db table for alarm states for specified usernames'''

    fe = Attr('username').eq(usernames[0])
    table = dynamodb.Table(tablename)
    for username in usernames[1::]:
        fe = fe | Attr('username').eq(username)

    response = table.scan(FilterExpression=fe)
    logger.info(f"get_current_alarms response={str(response)}")
    return response.get('Items', [])


def recalculate_alarms(tablename, schedule, prepared_records, current_alarms):
    table = dynamodb.Table(tablename)
    alarms = get_alarms(schedule, table)

    for username, events in prepared_records.items():
        if schedule.get(username):
            for alarm in alarms:
                current_state = get_current_state(current_alarms, username, alarm)
                logger.info(f"Re-processing alarm {alarm.alarmcode} "
                            f"for {username},"
                            f"current state = {current_state}")
                logger.info(f"Calling {alarm.alarmcode}.process("
                            f"{json.dumps(events)}, "
                            f"{username}, "
                            f"{current_state})")
                alarm.process(events, username, current_state)


def get_current_state(current_alarms, username, alarm):
    for current in current_alarms:
        if current.get("username") == username \
           and current.get("alarmcode") == alarm.alarmcode:
            return current
    return {}


def get_alarms(schedules, table):
    alarms = [
        BSE(schedules),
        BSL(schedules),
        ESE(schedules),
        ESL(schedules),
        BBE(schedules),
        EBL(schedules),
        SIU(schedules),
        SOU(schedules),
        WOB(schedules),
        WOE(schedules)
    ]
    for alarm in alarms:
        alarm.set_table(table)
    return alarms


def get_username(event):
    '''Returns the username from a Connect Agent Log event'''
    return event.get("CurrentAgentSnapshot", {}) \
                .get("Configuration", {}) \
                .get("Username")


def split_s3(uri):
    match = re.match(r's3://(.+?)/(.*)', uri)
    if match:
        return (match.group(1), match.group(2))
