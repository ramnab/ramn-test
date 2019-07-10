import boto3
from boto3.dynamodb.conditions import Attr
from datetime import datetime
from datetime import timedelta

'''
Deletes all BSL alarms and adds fake login events into
agent history db
'''
# clear all BSL alarms
dynamodb = boto3.resource('dynamodb')
alarm_table = dynamodb.Table('rta-alarmsdb-ccm-test')
history_table = dynamodb.Table('rta-eventhistory-ccm-test')

alarms = alarm_table.scan(FilterExpression=Attr('alarmcode').eq('BSL'))

with alarm_table.batch_writer() as batch:
    for alarm in alarms.get("Items"):
        username = alarm.get("username")
        alarmcode = alarm.get("alarmcode")
        if username and alarmcode == "BSL":
            print(f"Deleting username={username}, alarmcode={alarmcode}")
            batch.delete_item(Key={
                "username": username,
                "alarmcode": "BSL"
            })
        else:
            raise Exception(f"ERROR for username={username}, "
                            f"alarmcode={alarmcode}")

now = datetime.now()
ttl = now + timedelta(hours=12)

with history_table.batch_writer() as batch:
    for alarm in alarms.get("Items"):
        username = alarm.get("username")
        if username:
            print(f"Adding LOGIN for {username}")
            batch.put_item(Item={
                "username": username,
                "prop": "LOGIN",
                "ts": now.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                "ttl": int(ttl.timestamp())
            })
