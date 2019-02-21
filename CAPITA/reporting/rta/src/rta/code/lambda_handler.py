import json
import base64
import logging
import re
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr
import os
from datetime import datetime
from db import *
from alarms import *


logger = logging.getLogger()
# INFO = 20
# DEBUG = 10
LOGGING_LEVEL = int(os.environ.get("LOGGING_LEVEL", "20"))
logger.setLevel(LOGGING_LEVEL)
s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')


def handler(event, context):
    """
    Handles Agent Events from Kinesis and calculates RTA alarm states

    """

    logger.debug("Called with events:" + json.dumps(event, indent=2))

    try:

        schedule_uri = os.environ.get("AGENT_SCHEDULE")
        (bucket, key) = split_s3(schedule_uri)
        schedule = read_schedule(bucket, key)
        logger.info(f"SCHEDULE={str(schedule)}")

        # get agent history
        historyTablename = os.environ.get("HISTORY_DB")
        history = DbTable(historyTablename)
        logger.debug(f"Agent history={history.items}")

        if event.get("EventType") == "SP_HEART_BEAT":
            logger.info(f"Special Heart Beat")
            prepared_records = prepare_heart_beat_update(schedule, history)
        elif event.get("Records"):
            prepared_records = prepare_records(event.get("Records"))
            capture_history(schedule, prepared_records, history)

        alarmTablename = os.environ.get("ALARM_DB")
        active_alarms = DbTable(alarmTablename)

        logger.info(f"Active alarms = {str(active_alarms.items)}")
        recalculate_alarms(schedule,
                           prepared_records,
                           active_alarms,
                           history)

    except Exception as e:
        logger.error(e)

    return {}


def prepare_heart_beat_update(schedule, history):
    '''
    Generate a new event for each agent in the schedule,
    using their last known status from the history db
    (or offline, if no status present)
    '''
    now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    logger.info(f"@ALARM|SPECIAL_HB|ts={now}")
    prep = {}
    for username, entry in schedule.items():
        agent_info = entry.get("AGENT_INFO", {})
        firstname = agent_info.get("first_name")
        lastname = agent_info.get("last_name")
        if not firstname or not lastname:
            raise Exception(f"No first/last name found for {username}")
        agent_state = history.get(username, "agent_status") \
                             .get("val", "Offline")
        prep[username] = [{
            "EventType": "SP_HEART_BEAT",
            "EventTimestamp": now,
            "CurrentAgentSnapshot": {
                "Configuration": {
                    "FirstName": firstname,
                    "LastName": lastname
                },
                "AgentStatus": {
                    "Name": agent_state
                }
            }
        }]

    logger.info(f"Special HB prepared events: {json.dumps(prep, indent=2)}")
    return prep


def prepare_records(records):
    '''Decodes each kinesis record grouped by username'''
    prep = {}
    logger.info(f"Processing {len(records)} kinesis records")
    for record in records:
        data = record.get('kinesis', {}).get('data', '')
        event_as_str = base64.b64decode(data).decode('utf8')
        try:
            event = json.loads(event_as_str)
            logger.debug(f"Event decoded to json: {event}")
            if event:
                username = event.get("CurrentConfiguration", {}) \
                                .get("Configuration", {}) \
                                .get("Username")
                if "@" in username:
                    logger.info(f"Skipping ADMIN login "
                                f"from Console: {username}")
                    continue

                log_event(event)
                username = get_username(event)
                if username:
                    if not prep.get(username):
                        prep[username] = []
                    prep[username].append(event)
        except json.JSONDecodeError:
            logger.error("Unable to decode json record from string: "
                         f"{event_as_string}")

    logger.debug(f"Prepared records: {prep}")
    return prep


def log_event(event):
    username = get_username(event)
    event_type = event.get("EventType", "UNK_TYPE")
    ts = event.get("EventTimestamp", "UNK_TS")
    status = event.get("CurrentAgentSnapshot", {}) \
                  .get("AgentStatus", {}) \
                  .get("Name", "UNK_STATUS")
    logger.info(f"@ALARM|EVENT|{username}|{event_type}|{ts}|{status}")


def read_schedule(bucket, key):
    '''Reads in JSON schedule from specified S3 bucket / key'''
    try:
        logger.debug(f"Reading schedule from s3://{bucket}/{key}")
        schedule = s3.Object(bucket, key).get()['Body'].read().decode('utf-8')
        schedule_as_json = json.loads(schedule)
        logger.debug(f"Schedule: {json.dumps(schedule_as_json)}")
        return schedule_as_json
    except ClientError as e:
        raise Exception(f"Cannot read schedule file from s3://{bucket}/{key}")


def recalculate_alarms(schedule, prepared_records,
                       alarm_states_db, history_db):

    alarms = get_all_alarms(schedule, alarm_states_db)

    for username, events in prepared_records.items():
        # if schedule.get(username):
        user_history = history_db.get(username)
        alarm_states = alarm_states_db.get(username)
        for alarm in alarms:
            alarm_state = {}
            for state in alarm_states:
                if state.get("alarmcode") == alarm.alarmcode:
                    alarm_state = state

            logger.info(f"Re-processing alarm {alarm.alarmcode} "
                        f"for {username},"
                        f"current state = {alarm_state}, "
                        f"user history = {user_history}")
            alarm.process(events, username, alarm_state, user_history)


def get_all_alarms(schedules, table):
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
        WOE(schedules),
        BXE(schedules),
        EXL(schedules)
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


def get_end_of_current_shift(username, schedule, ts):
    '''
    Find the current or next shift
    and return the end time of it
    '''
    bses = schedule.get(username, {}) \
                   .get("ALARMS", {}) \
                   .get("BSE", [])
    number_of_shifts = len(bses)

    logger.info(f"{username} has {number_of_shifts} shifts in schedule")
    if number_of_shifts == 1:
        logger.info(f"get_end_of_current_shift: "
                    f"end of shift for {username} "
                    f"is {bses[0].get('end')} "
                    f"based on a single shift")
        return datetime.strptime(bses[0].get("end"), '%Y-%m-%dT%H:%M')

    if number_of_shifts > 1:
        logger.info(f"get_end_of_current_shift: "
                    f"more than one shift scheduled")
        current_ts = Alarm.get_ts(ts)
        end_of_shift = None
        for shift in bses:
            if current_ts < Alarm.get_ts(shift.get("end")):
                end_of_shift = shift.get("end")
                break
        if not end_of_shift:
            end_of_shift = bses[number_of_shifts-1].get("end")
        return datetime.strptime(end_of_shift, '%Y-%m-%dT%H:%M')

    logger.warn(f"get_end_of_current_shift: "
                f"No shifts found for {username}")
    return None


def capture_history(schedule, records, history):
    '''
    Gets the  agent status from the last event received
    and writes to the history db

    LOGIN / LOGOUT events are also written to the
    history db, but only if there is not already
    an entry present. These events are automatically
    deleted by TTL based on the end of the current
    shift
    '''
    history_updates = []
    for username, recordset in records.items():
        logger.info(f"Processing event for capture: "
                    f"{username}: {json.dumps(recordset, indent=2)}")

        # capture current agent state from latest record
        latest = get_latest(recordset)
        logger.info(f"Latest record: {latest}")
        agent_status = latest.get("CurrentAgentSnapshot", {})  \
                             .get("AgentStatus", {}) \
                             .get("Name")

        agent_historic_status = history.get(username, "agent_status") \
                                       .get("val", "UNK")
        logger.info(f"Agent {username} "
                    f"historic status={agent_historic_status}"
                    f", current status={agent_status}")

        if agent_status and agent_status != agent_historic_status:
            history_updates.append({
                "username": username,
                "prop": "agent_status",
                "val": agent_status
            })

        # capture FIRST LOGIN / LOGOUT events
        for record in recordset:
            logger.info(f"Processing record: {str(record)}")
            if record.get("EventType") == "LOGIN" and \
               not history.get(username, "LOGIN"):
                ts = record.get("EventTimestamp")
                end_of_shift = get_end_of_current_shift(username, schedule, ts)
                logger.info(f"end of shift={end_of_shift}")
                if end_of_shift:
                    history_updates.append({
                        "username": username,
                        "prop": "LOGIN",
                        "ts": ts,
                        "ttl": int(end_of_shift.timestamp())
                    })
            if record.get("EventType") == "LOGOUT" and \
               not history.get(username, "LOGOUT"):
                history_updates.append({
                    "username": username,
                    "prop": "LOGOUT"
                })
    logger.info(f"Agent history new/updates: {str(history_updates)}")
    history.write(history_updates)


def get_latest(records):
    latest = records[0]
    latest_ts = datetime.strptime(latest.get("EventTimestamp"),
                                  '%Y-%m-%dT%H:%M:%S.%fZ')
    for record in records[1:]:
        ts = datetime.strptime(record.get("EventTimestamp"),
                               '%Y-%m-%dT%H:%M:%S.%fZ')
        if ts > latest_ts:
            latest_ts = ts
            latest = record
    return latest
