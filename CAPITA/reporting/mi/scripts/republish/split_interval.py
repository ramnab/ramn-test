import sys
import boto3
from botocore.exceptions import ClientError
import re
import argparse


def read_s3(bucket: str, key: str):
    """
    Reads a file from S3 and returns a string
    :param bucket: S3 bucket
    :param key: S3 key to file
    :return: file as a string
    """
    s3 = boto3.resource('s3')
    try:
        obj = s3.Object(bucket, key)
        response = obj.get()
        return response.get('Body').read().decode('utf-8')
    except ClientError as e:
        raise Exception(f"Cannot read file s3://{bucket}/{key}: {str(e)}")


def write_s3(bucket: str, key: str, header: str, lines: list, dryrun):

    if dryrun:
        print("(DRYRUN) ", end="")
    print(f"Writing {len(lines)} lines to s3://{bucket}/{key}")
    s3 = boto3.resource('s3')
    contents = header + "\n"
    for i, line in enumerate(lines):
        contents += line
        if i != len(lines) - 1:
            contents += "\n"
    try:
        if not dryrun:
            obj = s3.Object(bucket, key)
            obj.put(Body=contents)
    except ClientError as e:
        raise Exception(f"Cannot write file s3://{bucket}/{key}: {str(e)}")


def get_file_name(destination: str, date: str):
    return destination.replace("{DATE}", date)


def get_date(line: str):
    m = re.match(r'^.+?,(\d\d\d\d-\d\d-\d\d)T', line)
    if m:
        return m.group(1)
    raise Exception(f"No date found in line: '{line}'")


def load_files(bucket: str, keys: list, days: dict):
    header = None
    for key in keys:
        print(f"Processing file 's3://{bucket}/{key}'")
        file = read_s3(bucket, key)
        lines = file.split('\n')
        header = lines[0]
        for line in lines[1:]:
            if line:
                date = get_date(line)
                if not days.get(date):
                    days[date] = []
                days[date].append(line)
    return header


def write_files(destination: str, header: str, days: dict, dryrun):
    for date, lines in days.items():
        (target_bucket, target_key) = from_path(destination)
        target_key = get_file_name(target_key, date)
        write_s3(target_bucket, target_key, header, lines, dryrun)


def get_files(bucket: str, prefix: str):
    s3 = boto3.client("s3")
    response = s3.list_objects_v2(
        Bucket=bucket,
        Prefix=prefix
    )
    return [item.get("Key") for item in response.get("Contents", [])]


def from_path(path: str):
    return re.match('s3://(.+?)/(.+)', path).groups()


def main():
    parser = argparse.ArgumentParser(description='''
       Usage:
           python split_interval.py [--dryrun] -s SOURCE_PATH -t TARGET_PATH
       ''')
    parser.add_argument('-s', '--source',
                        help='Source path in the form s3://bucket/folder/prefix',
                        required=True)

    parser.add_argument('-t', '--target',
                        help='Target path in the form s3://bucket/folder/AgentInterval-{DATE}.csv',
                        required=True)

    parser.add_argument('--dryrun',
                        help='Dry run - will not write to S3',
                        action="store_true")

    args = parser.parse_args()
    (source_bucket, source_prefix) = from_path(args.source)
    print(f"Reading files from s3://{source_bucket}/{source_prefix}")
    files = get_files(source_bucket, source_prefix)
    days = {}
    header = load_files(source_bucket, files, days)
    print(f"Days = {days.keys()}")
    write_files(args.target, header, days, args.dryrun)


if __name__ == '__main__':
    sys.exit(main())
