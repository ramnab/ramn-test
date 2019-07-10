import sys
import boto3
import json
import argparse
from datetime import timedelta, datetime
import re
from time import sleep


firehose = boto3.client('firehose')
s3 = boto3.client('s3')


def from_path(path: str):
    """Returns tuple of bucket and path from pattern s3://bucket/path """
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


def update_firehose(fh: str, day: str):
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
            'Prefix': "historic/ctrs/transformed/!{timestamp:yyyy-MM-dd}/clientname=tradeuk/rowdate=" + day + "/",
            'ErrorOutputPrefix': f"historic/errors/ctrs/",
        }
    )


def get_files(bucket: str, prefix: str):
    print(f"\n\nget_files('{bucket}', '{prefix})'")
    response = s3.list_objects_v2(
        Bucket=bucket,
        Prefix=prefix
    )
    files = [x.get("Key") for x in response.get("Contents", [])]
    print(f"Found {len(files)} matching files")
    return files


def republish_day(fh: str, day: str, bucket: str, prefix: str):
    update_firehose(fh, day)
    keys = get_files(bucket, prefix + day)
    for key in keys:
        republish_file(bucket, key, fh)
    return len(keys)


def republish_file(bucket: str, key: str, fh: str):
    records = to_json(bucket, key)
    record_batches = chunks(records, 450)
    for record_set in record_batches:
        batch = [{'Data': json.dumps(r)} for r in record_set]
        print(f"sending {len(batch)} records in a batch")
        firehose.put_record_batch(
            DeliveryStreamName=fh,
            Records=batch
        )


def to_json(bucket: str, key: str):
    response = s3.get_object(
        Bucket=bucket,
        Key=key
    )
    if response.get('Body'):
        records = response.get('Body').read().decode('utf-8')
        records = '[' + re.sub(r'}\s+{', '},\n{', records) + ']'
        json_list = json.loads(records)
        print(f"Source file has {len(json_list)} entries,", end=" ")
        return json_list
    return None


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def main():
    parser = argparse.ArgumentParser(description='''
    Usage:
        python republish_ctrs.py -f FIREHOSE -p PATH -s START -e END

        for dates START to END *inclusive*, in the format YYYY-MM-DD
        if no END given then only the start date is used, i.e. one day only

        PATH is the s3 path to the files, up to the date stamp
        FIREHOSE is the name of the firehose to send republish to

        This script updates the firehose output to go to the following prefix:
            /historic/ctrs/transformed/!{timestamp:yyyy-MM-dd}/clientname=tradeuk/rowdate=DAY/

        where the timestamp is the current date - this allows us to keep subsequent runs separate
        and also prevents the default YYYY/MM/DD/HH/ prefix being used

    ''')

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
        print(f"\n\n---------------------\n D A Y : {day}   {len(dates) - i - 1} remaining\n")

        total = republish_day(args.firehose, day, bucket, prefix)
        if total and i != len(dates) - 1:
            print(f"\nSleeping until buffer expires...")
            sleep(90)
    print("Completed")


if __name__ == '__main__':
    sys.exit(main())
