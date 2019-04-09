"""Retrieve agent schedule from s3, process it into json and upload to different s3"""
import json
import csv
import os
import re
from datetime import datetime
from datetime import timedelta
import boto3
import logging

logger = logging.getLogger()
# INFO = 20
# DEBUG = 10
LOGGING_LEVEL = int(os.environ.get("LOGGING_LEVEL", "20"))
logger.setLevel(LOGGING_LEVEL)


def handler(event, _context):
    """Main Handler function"""
    logger.info(f"Received event: {str(event)}")

    try:
        reader = get_schedule_from_s3(event)
        (schedule, errors) = convert_schedule_to_json(event, reader)
        validate_work_presence(schedule, errors)

        alarm_config = json.loads(get_alarm_config_from_s3())
        for agent in schedule:
            schedule[agent]["ALARMS"] = create_alarms(schedule, agent, alarm_config)

        logger.info(f"Returning schedule: {json.dumps(schedule, indent=2)}")
        upload_schedule_to_s3(schedule)
        if errors:
            sns_error(event, errors)
    except Exception as e:
        logger.error(f"Exception: {str(e)}")


def get_schedule_from_s3(event):
    """Download schedule from s3, as defined by event"""
    s3client = boto3.resource('s3')
    bucketname = event["Records"][0]["s3"]["bucket"]["name"]
    objectkey = event["Records"][0]["s3"]["object"]["key"]
    schedule = s3client.Object(bucketname, objectkey).get()['Body'].read().decode('utf-8')
    schedulelist = schedule.splitlines()
    schedule = csv.DictReader(schedulelist)
    return schedule


def upload_schedule_to_s3(schedule):
    """Convert file to bytes format and upload to s3"""
    s3client = boto3.client('s3')

    schedulebytes = json.dumps(schedule).encode('utf-8')

    bucketname = os.environ.get("output_s3_bucket")
    objectkey = os.environ.get("output_file_path")

    s3client.put_object(Bucket=bucketname, Key=objectkey, Body=schedulebytes)


def verify_schedule_contents(row):
    """Confirm row contains all required information in correct format"""
    redate = re.compile("\\d{2}-\\d{2}-\\d{4}\\s+\\d{2}:\\d{2}:\\d{2}")
    errors = []
    if not redate.match(row.get('start_moment', "")):
        errors.append(f'The start moment for user {row.get("payroll_no", "UNK")} was incorrect/missing')
    if not redate.match(row.get('stop_moment', "")):
        errors.append(f'The stop moment for user {row.get("payroll_no", "UNK")} was incorrect/missing')
    if not (row.get('code') and row.get('cat')):
        errors.append(f'Schedule missing code/cat information for {row.get("payroll_no", "UNK")}')
    return errors


def sns_error(event, errors):
    """Generate error message and send to SNS, then raise exception"""
    if not errors:
        return

    snsclient = boto3.client('sns')

    s3key = event["Records"][0]["s3"]["object"]["key"]
    eventtime = event["Records"][0]["eventTime"]
    bucketname = event["Records"][0]["s3"]["bucket"]["name"]

    filepath = s3key.split('/')
    filename = filepath.pop()

    bucketpath = bucketname
    for folder in filepath:
        bucketpath = bucketpath + "/" + folder

    message = (f"""
The following file
    {filename} 

uploaded at {eventtime} to 

    {bucketpath}

had the following validation error(s):

""")

    for error in errors:
        message += f"\t * {error}\n"

    logger.warning(message)

    snsclient.publish(
        TopicArn=os.environ.get('sns_failure_topic'),
        Message=message,
        Subject=f'RTA Schedule Error for: {filename}'
    )


def get_alarm_config_from_s3():
    """Fetch alarm config json from s3"""
    s3client = boto3.resource('s3')

    bucketname = os.environ.get("input_s3_bucket")
    objectkey = os.environ.get("alarm_config_file_path")

    alarm_config = s3client.Object(bucketname, objectkey).get()['Body'].read().decode('utf-8')

    return alarm_config


def convert_schedule_to_json(event, reader):
    """Convert reader-format schedule to json"""
    schedule_as_json = {}
    errors = []
    number_of_rows = 0

    for row in reader:
        number_of_rows += 1
        if row['first_name'] != "Record_count":
            row_errors = verify_schedule_contents(row)
            if row_errors:
                errors.extend(row_errors)
                continue
            time1 = convert_datetime(row['start_moment'])
            time2 = convert_datetime(row['stop_moment'])
            times = {
                "T1": time1,
                "T2": time2
            }
            agentid = "P" + row['payroll_no']
            if agentid not in schedule_as_json:
                schedule_as_json[agentid] = {
                  "SCHEDULE": {},
                  "ALARMS": {},
                  "AGENT_INFO": {
                      "first_name": row['first_name'],
                      "last_name": row['last_name'],
                      "depts_code": row['depts_code'],
                      "acd_login_id": row['acd_login_id'],
                      "depts_descr": row['depts_descr']
                  }
                }
            if not schedule_as_json[agentid]['SCHEDULE'].get(row['cat']):
                schedule_as_json[agentid]['SCHEDULE'][row['cat']] = []
            schedule_as_json[agentid]['SCHEDULE'][row['cat']].append(times)
    logger.info(f"Number of rows processed: {number_of_rows}")

    if number_of_rows == 0:
        errors.append(f"Schedule provided had no rows")
        sns_error(event, errors)
        raise Exception("Schedule empty")

    logger.info(f"Schedule: {str(schedule_as_json)}")
    logger.info(f"Errors: {str(errors)}")

    return schedule_as_json, errors


def validate_work_presence(schedule, errors):
    """Validate all agents on schedule contain WORK"""
    invalid_agents = []
    logger.info(f"Validating schedule for agents")
    for agent in schedule:
        if "WORK" not in schedule[agent]['SCHEDULE']:
            agent_info = schedule.get(agent, {}).get("AGENT_INFO", {})
            first_name = agent_info.get("first_name", "")
            last_name = agent_info.get("last_name", "")
            if first_name and last_name:
                errors.append(f"There is no work shift defined for user {first_name} {last_name} (P{agent})")
            else:
                errors.append(f"There is no work shift defined for user P{agent}")
            invalid_agents.append(agent)
    for agent in invalid_agents:
        del schedule[agent]


def create_alarms(schedule, agent, config):
    """Create all alarm time windows for agent, return alarms as json"""
    alarmsdict = {}
    for alarm in config:  # e.g. BBE
        for code in config[alarm]["codes"]:  # code in ['BREAK']
            if code in schedule[agent]["SCHEDULE"]:
                if alarm not in alarmsdict:
                    alarmsdict[alarm] = []

                schedule_entries = schedule[agent]["SCHEDULE"][code]

                for schedule_entry in schedule_entries:
                    codedict = dict()
                    codedict['code'] = code
                    codedict['start'] = schedule_entry.get("T1")
                    codedict['end'] = schedule_entry.get("T2")
                    codedict['T1'] = create_alarm_time(config, alarm, code, schedule_entry, agent, 'T1')
                    if "T2" in config[alarm]:
                        codedict['T2'] = create_alarm_time(config, alarm, code, schedule_entry, agent, 'T2')

                    alarmsdict[alarm].append(codedict)
    return alarmsdict


def create_alarm_time(alarm_config, alarm, code, schedule, agent, time_code):
    """Create and return specific alarm time"""

    # for example, time_config = ["SCHEDULE.CODE.T2", "+ESL.window", "+SIU.grace"]
    # starting_time is the base timestamp to adjust

    time_config = alarm_config[alarm][time_code].split(',')
    starting_time = time_config[0].split('.')
    if starting_time[1] == "CODE":
        starting_time[1] = code

    schedtime = schedule[starting_time[2]]

    schedtime = datetime.strptime(schedtime, '%Y-%m-%dT%H:%M')
    alarm_time = calulate_alarm_time(schedtime, time_config, alarm_config)
    # logger.info(f"Created alarm {agent} for {agent}: {schedtime} -{time_code}-> {str(alarm_time)}")
    return str(alarm_time)


def calulate_alarm_time(schedtime, alarm, alarm_config):
    """Calculate T1/T2 for alarm based on alarm-config and schedule, return schedule time"""
    for adjustment in alarm:
        if adjustment != alarm[0]:
            if adjustment[0] == '+':
                path = adjustment[1:].split('.')
                delta = alarm_config[path[0]][path[1]]
                delta = timedelta(minutes=delta)
                schedtime = schedtime + delta
            elif adjustment[0] == '-':
                path = adjustment[1:].split('.')
                delta = alarm_config[path[0]][path[1]]
                delta = timedelta(minutes=delta)
                schedtime = schedtime - delta
            else:
                raise Exception(f'Alarm {alarm} not formatted correctly in config')
    return schedtime.strftime('%Y-%m-%dT%H:%M')


def convert_datetime(timestamp):
    """Convert datetime format to one usable by process lambda"""
    timestamp = datetime.strptime(timestamp, '%d-%m-%Y %H:%M:%S')
    convert = timestamp.strftime('%Y-%m-%dT%H:%M')
    return convert
