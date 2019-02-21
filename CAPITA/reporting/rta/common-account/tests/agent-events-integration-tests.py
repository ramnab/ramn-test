import boto3
import json
from time import sleep
import argparse

"""
    Send test events to a target Kinesis Stream

    Generates and sends events to the specified
    kinesis stream, waiting the specified duration
    between each (default 10 seconds)

"""

client = boto3.client('kinesis', region_name='eu-central-1')
dynamodb = boto3.resource('dynamodb')
table = None


def upload_schedule(env):
    with open('agent-schedule.json', 'r') as f:
        schedule = f.read()
        s3 = boto3.resource('s3')
        bucket = f's3-capita-ccm-common-{env}-rta-agentschedules'
        key = 'processed/agent-schedule.json'
        print(f"Uploading local schedule to s3://{bucket}/key")
        s3.Object(bucket, key) \
          .put(Body=open('agent-schedule.json', 'rb'))


def clear_table():
    global table
    print(f"Clearing table '{table.table_name}'")
    items = read()
    with table.batch_writer() as batch:
        for item in items:
            batch.delete_item(Key={
                "username": item.get("username"),
                "alarmcode": item.get("alarmcode")
            })


def read():
    global table
    response = table.scan(ConsistentRead=True)
    return response.get("Items")


def test_pass(test, items):
    if not test.get("expected"):
        return True

    for item in items:
        all_match = True
        for attr, val in test.get("expected").items():
            if not item.get(attr):
                all_match = False
                break
            if item.get(attr) != val:
                all_match = False
                break
        if all_match:
            return True
    return False


def run_test(test, stream):
    print(f"\n\n{test.get('title')}")
    send(stream, test.get("event"))
    sleep(5)
    db = read()
    print(f"Expected passed? {test_pass(test, db)}")


def send(stream, event):
    print(f"Sending event: {json.dumps(event)}")
    response = client.put_record(
        StreamName=stream,
        Data=json.dumps(event),
        PartitionKey='capita-ccm-rta-producer'
    )


def create(**kwargs):
    return {
        "EventType": kwargs.get("typ"),
        "CurrentAgentSnapshot": {
            "Configuration": {
                "Username": kwargs.get("username"),
                "FirstName": kwargs.get("firstname", "Fred"),
                "LastName": kwargs.get("lastname", "Blogs")
            },
            "AgentStatus": {
                "Name": kwargs.get("status", "Available")
            }
        },
        "EventTimestamp": kwargs.get("ts")
    }


def main():
    parser = argparse.ArgumentParser('''
Agent events Integration Tests

usage:
    python agent-events-integration-tests.py --env <ENV> --test <TEST>

ENV: which capita-common-nonprod env to use, dev or test, required
TEST: an individual test to run, e.g. BBE, optional; if not specified
will run all tests

''')

    parser.add_argument(
        '-e', '--env',
        help='''
Environment to target in capita-common: dev or test
''',
        required=True
    )

    parser.add_argument(
        '-t', '--test', help='Test to run, e.g. BBE',
        required=False
    )

    args = parser.parse_args()

    tests = {
        "BSL": [
            # SHIFT START=2019-02-20T08:15 END=2019-02-20T17:15
            # T1=2019-02-20T08:20 T2=2019-02-20T17:15
            {
                "title": "BSL Activated with SHB",
                "event": create(typ="SP_HEART_BEAT",
                                username="P21207381",
                                ts="2019-02-20T08:21:00.012Z")
            },
            {
                "title": "BSL TS Updated with SHB",
                "event": create(typ="SP_HEART_BEAT",
                                username="P21207381",
                                ts="2019-02-20T08:22:00.012Z")
            }
        ],
        "WOB": [
            # BREAK START=2019-02-20T12:30 END=2019-02-20T13:00
            # T1=2019-02-20T12:35 T2=2019-02-20T12:55
            {
                "title": "WOB Activated with SHB",
                "event": create(typ="SP_HEART_BEAT",
                                username="P21207381",
                                ts="2019-02-20T12:36:00.012Z")
            },
            {
                "title": "WOB TS Updated with SHB",
                "event": create(typ="SP_HEART_BEAT",
                                username="P21207381",
                                ts="2019-02-20T12:37:00.012Z")
            }
        ],
        "WOE": [
            # EXC START=2019-02-20T13:00 END=2019-02-20T17:15
            # T1=2019-02-20T13:05 T2=2019-02-20T17:10, status=Available
            {
                "title": "WOE Activated with SHB",
                "event": create(typ="SP_HEART_BEAT",
                                username="P21207381",
                                ts="2019-02-20T13:06:00.012Z")
            },
            {
                "title": "WOE TS Updated with SHB",
                "event": create(typ="SP_HEART_BEAT",
                                username="P21207381",
                                ts="2019-02-20T13:07:00.012Z")
            }
        ],
        "BBE": [
            # BREAK START=2019-02-20T12:30 END=2019-02-20T13:00
            # T1=019-02-20T12:15 T2=2019-02-20T12:25
            {
                "title": "BBE Activated with SHB",
                "event": create(typ="STATE_CHANGE",
                                username="P21207381",
                                ts="2019-02-20T12:16:00.012Z",
                                status="Break"),
                "expected": {
                    "username": "P21207381",
                    "alarmcode": "BBE"
                }
            }
        ],
        "ESE": [
            # SHIFT START=2019-02-20T08:15 END=2019-02-20T17:15
            # T1=2019-02-20T17:10
            {
                "title": "ESE Activated with LOGOUT",
                "event": create(typ="LOGOUT",
                                username="P21207381",
                                ts="2019-02-20T17:05:00.012Z"),
                "expected": {
                    "username": "P21207381",
                    "alarmcode": "ESE"
                }
            }
        ]
    }
    env = args.env
    print(f"\n\nStarting tests for envrionment '{env}'")
    stream = f"ks-ccm-agent-events-{env}"

    upload_schedule(env)

    global table
    table = dynamodb.Table(f'rta-alarmsdb-ccm-{env}')
    clear_table()
    if args.test and not tests.get(args.test):
        raise Exception(f"Test '{args.test}' not found")

    if args.test:
        print(f"\n\nRunning test set for {args.test}")
        for test in tests.get(args.test):
            run_test(test, stream)
            sleep(5)
    else:
        for test_set, test_items in tests.items():
            print(f"\n\nRunning test set for {test_set}")
            for test in test_items:
                run_test(test, stream)
                sleep(5)

    print("Completed")

if __name__ == '__main__':
    main()
