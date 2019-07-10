import sys
import boto3
import json
import argparse
from datetime import timedelta, datetime
import re
from time import sleep
from urllib.parse import quote


firehose = boto3.client('firehose')
s3 = boto3.client('s3')
lambda_client = boto3.client('lambda')


def from_path(path: str):
    return re.match('s3://(.+?)/(.+)', path).groups()


def generate_date_range(start_date, end_date):
    dates = []
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    delta = end - start

    for i in range(delta.days + 1):
        d = start + timedelta(i)
        dates.append(d.strftime('%Y-%m-%d'))
    return dates


def republish_day(typ: str, fh: str, day: str, bucket: str, prefix: str):
    update_firehose(typ, fh, day)
    files = get_files(bucket, prefix + day)
    for file in files:
        invoke_lambda(typ, fh, bucket, file)
    return len(files)


def update_firehose(typ: str, fh: str, day: str):
    response = firehose.describe_delivery_stream(DeliveryStreamName=fh)
    version_id = response.get("DeliveryStreamDescription", {}).get("VersionId")
    destination_id = response.get("DeliveryStreamDescription", {}) \
        .get("Destinations")[0] \
        .get("DestinationId")

    firehose.update_destination(
        DeliveryStreamName=fh,
        CurrentDeliveryStreamVersionId=version_id,
        DestinationId=destination_id,
        S3DestinationUpdate={
            'Prefix': "historic/" + typ +
                      "_interval/transformed/!{timestamp:yyyy-MM-dd}/clientname=tradeuk/rowdate=" + day + "/",
            'ErrorOutputPrefix': f"historic/errors/{typ}_interval/",
        }
    )


def get_files(bucket: str, prefix: str):
    response = s3.list_objects_v2(
        Bucket=bucket,
        Prefix=prefix
    )
    files = [x.get("Key") for x in response.get("Contents", [])]
    return files


def invoke_lambda(typ: str, fh: str, bucket: str, key: str):

    print(f"Sending s3://{bucket}/{key}")
    payload = {
        'Firehose': fh,
        'Records': [{
            's3': {
                'bucket': {
                    'name': bucket
                },
                'object': {
                    'key': quote(key)
                }
            }
        }]
    }

    target = typ[0:1].upper() + typ[1:]
    lambda_client.invoke(
        FunctionName=f"lmbMI{target}Interval-ccm-PROD",
        Payload=json.dumps(payload)
    )


def main():
    parser = argparse.ArgumentParser(description='''
    Usage:
        python republish_intervals.py -t TYPE -f FIREHOSE -p PATH -s START -e END
        
        for dates START to END *inclusive*, in the format YYYY-MM-DD
        if no END given then only the start date is used, i.e. one day only
        
        TYPE can be either 'agent' or 'queue'
        PATH is the s3 path to the files, up to the date stamp
        FIREHOSE is the name of the firehose to send republish to
        
        This script updates the firehose output to go to the following prefix:
            /historic/TYPE_interval/transformed/!{timestamp:yyyy-MM-dd}/clientname=tradeuk/rowdate=DAY/
        
        where the timestamp is the current date - this allows us to keep subsequent runs separate
        and also prevents the default YYYY/MM/DD/HH/ prefix being used
        
    ''')

    parser.add_argument('-t', '--type',
                        help='Type, either queue or agent',
                        required=False)

    parser.add_argument('-f', '--firehose',
                        help='The name of the firehose, e.g. kfh-ccm-agent-events-dev',
                        required=True)

    parser.add_argument('-p', '--path',
                        help=('Path to files, for example: '
                              's3://bucket/folder1/folder2/AgentInterval-'),
                        required=True)

    parser.add_argument('-s', '--start',
                        help='Start date, for example: 2019-01-01',
                        required=True)

    parser.add_argument('-e', '--end',
                        help='End date, for example: 2019-03-01',
                        required=False)

    args = parser.parse_args()
    print(f"args.path = {args.path}")
    (bucket, prefix) = from_path(args.path)
    print(f"bucket: {bucket}")
    print(f"prefix: {prefix}")

    if not args.end:
        args.end = args.start
    dates = generate_date_range(args.start, args.end)
    print(f"Republishing reports from the following days: {dates}")
    for i, day in enumerate(dates):
        print(f"\n\n---------------------\n D A Y : {day}\n")
        number_of_files = republish_day(args.type, args.firehose, day, bucket, prefix)
        if i != len(dates) - 1 and number_of_files:
            print(f"Sleeping until buffer expires...")
            sleep(90)
    print("Completed")


if __name__ == '__main__':
    sys.exit(main())
