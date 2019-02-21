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


def send(stream, event):
    print(f"Sending event: {json.dumps(event)}")
    response = client.put_record(
        StreamName=stream,
        Data=json.dumps(event),
        PartitionKey='capita-ccm-rta-producer'
    )
    print(f"Response: {response}")


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
    python agent-events-integration-tests.py --stream STREAM --wait DELAY

STREAM: kinesis stream to target, e.g. 
DELAY: seconds between each event (optional, default=10)

''')

    parser.add_argument(
        '-s', '--stream',
        help='''
Target Kinesis Stream,
e.g. str-ccm-dev-tradeuk-connect-dev01-agent-events''',
        required=True
    )

    parser.add_argument(
        '-w', '--wait', help='Seconds to wait between events',
        type=int, required=False, default=10
    )

    args = parser.parse_args()

    events = [
        ["BSE_Activated", create(typ="LOGIN", username="P0001", ts="2019-01-21T07:33:00.012Z")],
        # ["BSE_Cleared", create(typ="HEART_BEAT", username="P0001", ts="2019-01-21T07:55:00.012Z")],
        # ["BSL_Activated", create(typ="HEART_BEAT", username="P0001", ts="2019-01-21T08:06:00.012Z", status="Offline")],
        # ["BSL_UpdateTS", create(typ="HEART_BEAT", username="P0001", ts="2019-01-21T08:08:00.012Z", status="Offline")],
        # ["BSL_Cleared ", create(typ="LOGIN", username="P0001", ts="2019-01-21T16:32:00.012Z")],
        # ["ESE_Activated", create(typ="LOGOUT", username="P0001", ts="2019-01-21T16:26:00.012Z")],
        # ["ESL_Activated", create(typ="HEART_BEAT", username="P0001", ts="2019-01-21T16:36:00.012Z")],
        # ["ESL_UpdateTS", create(typ="HEART_BEAT", username="P0001", ts="2019-01-21T16:38:00.012Z")],
        # ["ESL_Cleared", create(typ="HEART_BEAT", username="P0001", ts="2019-01-21T16:38:00.012Z", status="Offline")],
        # ["BBE_Activated", create(typ="HEART_BEAT", username="P0001", ts="2019-01-21T12:40:00.012Z", status="Lunch")],
        # ["EBL_Activated", create(typ="HEART_BEAT", username="P0001", ts="2019-01-21T14:25:00.012Z", status="Break")],
        # ["EBL_UpdateTS", create(typ="HEART_BEAT", username="P0001", ts="2019-01-21T14:27:00.012Z", status="Break")],
        # ["SIU_Activated", create(typ="LOGIN", username="P0001", ts="2019-01-21T17:06:00.012Z")],
        # ["SOU_Activated", create(typ="LOGOUT", username="P0001", ts="2019-01-21T15:50:00.012Z", status="Offline")],
        # ["SOU_Clear_Login", create(typ="LOGIN", username="P0001", ts="2019-01-21T16:20:20.012Z", status="Offline")],
        # ["SOU_Activated", create(typ="LOGOUT", username="P0001", ts="2019-01-21T15:50:00.012Z", status="Offline")],
        # ["SOU_Clear_HB", create(typ="HEART_BEAT", username="P0001", ts="2019-01-21T16:31:00.012Z", status="Offline")],
        # ["WOB_Activate", create(typ="HEART_BEAT", username="P0001", ts="2019-01-21T13:16:00.012Z")],
        # ["WOB_UpdateTS", create(typ="HEART_BEAT", username="P0001", ts="2019-01-21T13:18:00.012Z")]
    ]
    for event in events:
        print(f"\n\n{event[0]}")
        send(args.stream, event[1])
        print(f"Waiting {args.wait} seconds...")
        sleep(args.wait)

    print("Completed")

if __name__ == '__main__':
    main()
