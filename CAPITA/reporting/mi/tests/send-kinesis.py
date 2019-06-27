import argparse
import sys
import boto3

'''
Sends a specific file to a a given kinesis stream

Usage:

    python send-kinesis.py -r REGION STREAM FILE
'''


def main():
    parser = argparse.ArgumentParser(description="""
Usage:
    python send-kinesis.py -r REGION STREAM FILE
    """)
    parser.add_argument('--region', '-r', action="store", default=boto3.session.Session().region_name)
    parser.add_argument('stream', action="store")
    parser.add_argument('file', action="store")
    args = parser.parse_args()
    print(f"Sending to stream '{args.stream}' [{args.region}]: {args.file}")

    client = boto3.client('kinesis', region_name=args.region)

    with open(args.file, 'r') as f:
        d = f.read()
        response = client.put_record(StreamName=args.stream, Data=d, PartitionKey='test')
        print(response)


if __name__ == '__main__':
    sys.exit(main())
