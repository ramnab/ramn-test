import boto3
from botocore.exceptions import ClientError
import logging
import csv
import json
import os


logger = logging.getLogger()
# INFO = 20
# DEBUG = 10
LOGGING_LEVEL = int(os.environ.get("LOGGING_LEVEL", "20"))
logger.setLevel(LOGGING_LEVEL)

max_number_firehose_batch = 500

'''
Republish
Loads a csv file from S3 and converts to JSON
Each entry/line is then published to the
specified firehose

Config is a list of normalised fields that should be 
kept as a string
'''


def process(bucket: str, key: str, firehose: str, config: list):
    """
    Reads in a csv report from S3, converts to JSON and republishes
    to the specified firehose

    :param bucket: S3 bucket
    :param key: key to csv file
    :param firehose: name of firehose
    :param config: list of normalised fields that should remain as strings
                   (default is to convert to either int or null)
    :return:
    """
    logger.info(f"@republish|process|invoked with bucket={bucket}, key={key}, firehose={firehose}")
    report = read_s3(bucket, key)
    report_json = str_to_json(report, config)
    republish(report_json, firehose)


def read_s3(bucket: str, key: str):
    """
    Reads a file from S3 and returns a string
    :param bucket: S3 bucket
    :param key: S3 key to file
    :return: file as a string
    """

    s3 = boto3.resource('s3')
    # return
    try:
        obj = s3.Object(bucket, key)
        response = obj.get()
        return response.get('Body').read().decode('utf-8')
    except ClientError as e:
        raise Exception(f"Cannot read file s3://{bucket}/{key}: {str(e)}")


def str_to_json(report: str, config: list):
    """
    Convert a string containing CSV data into a dict

    :param report: csv as a string
    :param config: list of normalised fields that should remain as strings
    :return: list of dictionary items
    """
    reader = csv.DictReader(report.split('\n'), delimiter=',')
    entries = []
    for row in reader:
        entry = {}
        for fld, val in row.items():
            fld_normalised = normalise_field(fld)
            value_typed = convert_value(config, fld_normalised, val)
            entry[fld_normalised] = value_typed
        entries.append(entry)
    return entries


def normalise_field(fld: str):
    return fld.lower().replace(" ", "")


def convert_value(config: list, fld: str, val: str):
    """
    Convert value to integer if the normalised field
    not in config list; an empty string is returned as
    'None'
    """

    if fld in config:
        return val
    try:
        return int(val)
    except ValueError:
        pass
    return None


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def republish(report_json: dict, firehose: str):
    fh = boto3.client('firehose')

    record_chunks = chunks(report_json, max_number_firehose_batch)
    for records in record_chunks:
        logger.info(f"@republish|republish|sending records: {str(records)}")
        fh.put_record_batch(
            DeliveryStreamName=firehose,
            Records=[{'Data': json.dumps(record)} for record in records]
        )


