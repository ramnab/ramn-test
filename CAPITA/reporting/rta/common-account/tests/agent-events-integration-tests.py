import boto3
import json
from time import sleep
import argparse
from pathlib import Path

"""
    Send test events to a target Kinesis Stream

    Generates and sends events to the specified
    kinesis stream, waiting the specified duration
    between each (default 10 seconds)

"""

client = boto3.client('kinesis', region_name='eu-central-1')
dynamodb = boto3.resource('dynamodb')
alarms_table = None
status_table = None
lambda_client = boto3.client("lambda")


def slp(t):
    if t:
        print(f"... pausing for {t} seconds...", end='\r')
        sleep(1)
        t -= 1
        slp(t)
    else:
        print("\n")


def upload_schedule(env):

    s3 = boto3.resource('s3')
    bucket = f's3-capita-ccm-common-{env}-rta-agentschedules'
    key = 'processed/agent-schedule-testing.json'
    print(f"Uploading local schedule to s3://{bucket}/key")
    cwd = Path(__file__).parents[0]
    agent_file_path = cwd / 'agent-schedule-testing.json'

    s3.Object(bucket, key) \
        .put(Body=open(agent_file_path, 'rb'))


def clear_alarms_table():
    global alarms_table
    print("Clearing alarms table")
    items = read_alarms()
    with alarms_table.batch_writer() as batch:
        for item in items:
            batch.delete_item(Key={
                "username": item.get("username"),
                "alarmcode": item.get("alarmcode")
            })
    sleep(2)


def clear_status_table():
    global status_table
    print("Clearing status table")
    items = read_status()
    with status_table.batch_writer() as batch:
        for item in items:
            batch.delete_item(Key={
                "username": item.get("username"),
                "prop": item.get("prop")
            })
    sleep(2)


def read_alarms():
    global alarms_table
    response = alarms_table.scan(ConsistentRead=True)
    return response.get("Items")


def read_status():
    global status_table
    response = status_table.scan(ConsistentRead=True)
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


def run_test(test, stream, env):
    print(f"\n\n{test.get('title')}")
    if test.get("clear", "") == "alarms":
        clear_alarms_table()
    send(stream, test, env)
    sleep(2)
    db = read_alarms()
    if test.get("expected"):
        print(f"Expected passed? {test_pass(test, db)}")
    else:
        print("No tests set")


def send(stream, test, env):
    print(f"Sending test: {json.dumps(test)}")
    if test.get("event"):
        client.put_record(
            StreamName=stream,
            Data=json.dumps(test.get("event")),
            PartitionKey='capita-ccm-rta-producer'
        )

    elif test.get("hb"):
        fn = f"lmbRtaApp-ccm-{env.upper()}"
        event = {
            "EventType": "SP_HEART_BEAT"
        }
        ts = test.get("hb", {}).get("ts")

        if ts:
            event['ts'] = ts

        print(f"\nInvoking with event: {event}\n")

        lambda_client.invoke(FunctionName=fn,
                             Payload=json.dumps(event))


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
        "SIU": [
            # SHIFT START=2019-02-20T08:15 END=2019-02-20T17:15
            {
                "title": "SIU Pending Before SHIFT",
                "event": create(typ="LOGIN",
                                username="P21207381",
                                ts="2019-02-20T07:30:00.012Z")
            },
            {
                "title": "SIU Incr TS Pending Before SHIFT",
                "hb": {"ts": "2019-02-20T07:31:00.012Z"}
            },
            {
                "title": "SIU Incr TS Active Before SHIFT",
                "hb": {"ts": "2019-02-20T07:36:00.012Z"}
            },
            {
                "title": "SIU Pending After SHIFT",
                "event": create(typ="LOGIN",
                                username="P21207381",
                                ts="2019-02-20T17:55:00.012Z"),
                "clear": "alarms"
            },
            {
                "title": "SIU Pending WITH NO SCHEDULE",
                "event": create(typ="LOGIN",
                                username="P123",
                                ts="2019-02-20T17:55:00.012Z"),
                "clear": "alarms"
            },
            {
                "title": "SIU Pending WITH NO SCHEDULE, Increment time",
                "hb": {"ts": "2019-02-20T17:56:00.012Z"}
            },
            {
                "title": "SIU Activated WITH NO SCHEDULE, Increment time",
                "hb": {"ts": "2019-02-20T18:02:00.012Z"}
            }
        ],
        "BSL": [
            # SHIFT START=2019-02-20T08:15 END=2019-02-20T17:15
            # T1=2019-02-20T08:20 T2=2019-02-20T17:15
            {
                "title": "BSL Activated with SHB",
                "hb": {"ts": "2019-02-20T08:21:00.012Z"}
            },
            {
                "title": "BSL TS Update with SHB",
                "hb": {"ts": "2019-02-20T08:22:00.012Z"}
            },
            {
                "title": "BSL Login detected",
                "event": create(typ="LOGIN",
                                username="P21207381",
                                ts="2019-02-20T08:22:00.012Z")
            }
        ],
        "WOB": [
            # BREAK START=2019-02-20T12:30 END=2019-02-20T13:00
            # T1=2019-02-20T12:35 T2=2019-02-20T12:55
            {
                "title": "WOB Set up: setting LOGIN with a work status",
                "event": create(typ="LOGIN",
                                username="P21207381",
                                ts="2019-02-20T08:15:00.012Z")
            },
            {
                "title": "WOB Activated with SHB",
                "hb": {"ts": "2019-02-20T12:36:00.012Z"}
            },
            {
                "title": "WOB TS Updated with SHB",
                "hb": {"ts": "2019-02-20T12:37:00.012Z"}
            },
            {
                "title": "WOB Cleared with State Change to non-work status",
                "event": create(typ="STATE_CHANGE",
                                username="P21207381",
                                ts="2019-02-20T12:38:00.012Z",
                                status="Break")
            },
            {
                "title": ("WOB Activated during scheduled exception with "
                          "State Change to a work status - PENDING status"),
                "event": create(typ="STATE_CHANGE",
                                username="P21207381",
                                ts="2019-02-20T12:36:00.012Z",
                                status="Available")
            },
            {
                "title": ("WOB Activated during scheduled exception with "
                          "State Change to a work status - ACTIVE status"),
                "hb": {"ts": "2019-02-20T12:42:00.012Z"}
            },
            {
                "title": "WOE ts updated",
                "hb": {"ts": "2019-02-20T12:43:00.012Z"}
            }
        ],
        "WOE": [
            # EXC START=2019-02-20T13:00 END=2019-02-20T17:15
            # T1=2019-02-20T13:05 T2=2019-02-20T17:10, status=Available
            {
                "title": "WOE Set up: setting LOGIN with a work status",
                "event": create(typ="LOGIN",
                                username="P21207381",
                                ts="2019-02-20T08:15:00.012Z")
            },
            {
                "title": "WOE Activated with SHB",
                "hb": {"ts": "2019-02-20T13:06:00.012Z"}
            },
            {
                "title": "WOE TS Updated with SHB",
                "hb": {"ts": "2019-02-20T13:07:00.012Z"}
            },
            {
                "title": "WOE Cleared with State Change to non-work status",
                "event": create(typ="STATE_CHANGE",
                                username="P21207381",
                                ts="2019-02-20T13:08:00.012Z",
                                status="Break")
            },
            {
                "title": ("WOE Activated during scheduled exception with "
                          "State Change to a work status - PENDING status"),
                "event": create(typ="STATE_CHANGE",
                                username="P21207381",
                                ts="2019-02-20T13:01:00.012Z",
                                status="Available")
            },
            {
                "title": ("WOE Activated during scheduled exception with "
                          "State Change to a work status - ACTIVE status"),
                "hb": {"ts": "2019-02-20T13:07:00.012Z"}
            },
            {
                "title": "WOE ts updated",
                "hb": {"ts": "2019-02-20T13:08:00.012Z"}
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

    global alarms_table
    global status_table
    alarms_table = dynamodb.Table(f'rta-alarmsdb-ccm-{env}')
    status_table = dynamodb.Table(f'rta-eventhistory-ccm-{env}')
    if args.test and not tests.get(args.test):
        raise Exception(f"Test '{args.test}' not found")

    if args.test:
        print(f"""

+-----------------------------------+
Running test set for {args.test}

""")
        clear_alarms_table()
        clear_status_table()
        for test in tests.get(args.test):
            run_test(test, stream, env)
            slp(10)
    else:
        for test_set, test_items in tests.items():
            print(f"""

+-----------------------------------+
Running test set for {test_set}

""")
            clear_alarms_table()
            clear_status_table()
            for test in test_items:
                run_test(test, stream, env)
                slp(10)

    print("Completed")


if __name__ == '__main__':
    main()
