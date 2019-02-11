"""Retrieve agent schedule from s3, process it into json and upload to different s3"""
import json
import csv
import os
import re
from datetime import datetime
from datetime import timedelta
import boto3

def handler(event, __context):
    """Main Handler function"""
    reader = get_schedule_from_s3(event)
    schedule = convert_schedule_to_json(reader)
    # validate_schedule(schedule)

    alarm_config = json.loads(get_alarm_config_from_s3())
    for agent in schedule:
        schedule[agent]["ALARMS"] = create_alarms(schedule, agent, alarm_config)
    upload_schedule_to_s3(schedule)

def get_schedule_from_s3(event):
    """Download schedule from s3, as defined by event"""
    s3client = boto3.resource('s3')
    bucketname = event["Records"][0]["s3"]["bucket"]["name"]
    objectkey = event["Records"][0]["s3"]["object"]["key"]
    schedule = s3client.Object(bucketname, objectkey).get()['Body'].read().decode('utf-8')
    schedulelist = schedule.split('\r\n')
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
    if 'start_moment' not in row:
        print(row['payroll_no'])
    redate = re.compile("\\d{2}/\\d{2}/\\d{4} \\d{2}:\\d{2}")
    if not redate.match(row['start_moment']):
        raise Exception(f'Schedule start_moment malformed for payroll_no {row["payroll_no"]}')
    if not redate.match(row['stop_moment']):
        raise Exception(f'Schedule stop_moment malformed for payroll_no {row["payroll_no"]}')
    if not (row['code'] and row['cat']):
        raise Exception(f'Schedule missing information for {row["payroll_no"]}')

def get_alarm_config_from_s3():
    """Fetch alarm config json from s3"""
    s3client = boto3.resource('s3')

    bucketname = os.environ.get("input_s3_bucket")
    objectkey = os.environ.get("alarm_config_file_path")

    alarm_config = s3client.Object(bucketname, objectkey).get()['Body'].read().decode('utf-8')

    return alarm_config

def convert_schedule_to_json(reader):
    """Convert reader-format schedule to json"""
    schedule_as_json = {}
    for row in reader:
        if row['cat'] != "Record_count":
            verify_schedule_contents(row)
            time1 = convert_datetime(row['start_moment'])
            time2 = convert_datetime(row['stop_moment'])
            times = {
                "T1":time1,
                "T2":time2
            }
            agentid = "P" + row['payroll_no']
            if agentid not in schedule_as_json:
                schedule_as_json[agentid] = {"SCHEDULE": {}, "ALARMS": {}}
            schedule_as_json[agentid]['SCHEDULE'][row['cat']] = times

    return schedule_as_json

# def validate_schedule(schedule):
#     """Run validation tests against input schedule"""
#     validate_shift_presence(schedule)

# def validate_shift_presence(schedule):
#     """Validate all agents on schedule contain SHIFT"""
#     noshiftagents = []
#     for agent in schedule:
#         if "WORK" not in schedule[agent]['SCHEDULE']:
#             noshiftagents.append(agent)
#     if noshiftagents:
#         raise Exception(f'These agents have no WORK information in the schedule: {noshiftagents}')
#         print("Some agents have no WORK information")

def create_alarms(schedule, agent, config):
    """Create all alarm time windows for agent, return alarms as json"""
    alarmsdict = {}
    for alarm in config:
        for code in config[alarm]["codes"]:
            if code in schedule[agent]["SCHEDULE"]:
                if alarm not in alarmsdict:
                    alarmsdict[alarm] = []
                codedict = {}
                codedict['code'] = code
                codedict['start'] = schedule[agent]["SCHEDULE"][code]["T1"]
                codedict['end'] = schedule[agent]["SCHEDULE"][code]["T2"]
                codedict['T1'] = create_alarm_time(config, alarm, code, schedule, agent, 'T1')
                if "T2" in config[alarm]:
                    codedict['T2'] = create_alarm_time(config, alarm, code, schedule, agent, 'T2')
                alarmsdict[alarm].append(codedict)
    return alarmsdict

def create_alarm_time(alarm_config, alarm, code, schedule, agent, time_code):
    """Create and return specific alarm time"""
    time = alarm_config[alarm][time_code].split(',')
    timepath = time[0].split('.')
    if timepath[1] == "CODE":
        timepath[1] = code
    schedtime = schedule[agent][timepath[0]][timepath[1]][timepath[2]]
    schedtime = datetime.strptime(schedtime, '%Y-%m-%dT%H:%M')
    alarm_time = calulate_alarm_time(schedtime, time, alarm_config)
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

def convert_datetime(time):
    """Convert datetime format to one usable by process lambda"""
    time = datetime.strptime(time, '%d/%m/%Y %H:%M')
    convert = time.strftime('%Y-%m-%dT%H:%M')
    return convert
