import boto3
import os
import logging
from datetime import datetime


logger = logging.getLogger()
# ERROR = 40, WARNING = 30, INFO = 20, DEBUG = 10
LOGGING_LEVEL = int(os.environ.get("LOGGING_LEVEL", "20"))
logger.setLevel(LOGGING_LEVEL)


def handler(event, _context):
    logger.info(f"@lambda_handler|handler|received event: {str(event)}")

    db = os.environ.get("DB")
    tables = os.environ.get("TABLES")
    bucket = os.environ.get("BUCKET")
    clients = os.environ.get("CLIENTS")

    if not db:
        logger.error("@lambda_handler|handler|No database specified in env variable DB")

    if not tables:
        logger.error("@lambda_handler|handler|No tables specified in env variable TABLES")

    if not bucket:
        logger.error("@lambda_handler|handler|No bucket specified in env variable BUCKET")

    if not clients:
        logger.error("@lambda_handler|handler|No client specified in env variable CLIENT")

    if db and tables and bucket and clients:
        update(db, bucket, tables, clients)


def update(db, bucket, tables, clients):
    table_list = tables.split(",")
    for tablename in table_list:
        create_folder_partition(bucket, tablename, clients)
        update_partitions(db, tablename, bucket)


def create_folder_partition(bucket, tablename, clients):
    s3 = boto3.resource('s3')
    rowdate = datetime.now().strftime('%Y-%m-%d')

    for client in clients.split(","):
        key = f"{tablename}/clientname={client}/rowdate={rowdate}/"
        dummy_obj = s3.Object(bucket, key)
        response = dummy_obj.put(Body='')
        logger.info(f"@lambda_handler|create_folder_partition|Created new folder: {key}")
        logger.info(f"@lambda_handler|create_folder_partition|New folder response: {response}")


def update_partitions(db, tablename, query_results_bucket):
    client = boto3.client('athena')
    query_string = f'MSCK REPAIR TABLE {tablename};'

    response = client.start_query_execution(
        QueryExecutionContext={
            'Database': db
        },
        QueryString=query_string,
        ResultConfiguration={
            'OutputLocation': f"s3://{query_results_bucket}/query-results/mi-analyst"
        }
    )

    logger.info(f"@lambda_handler|update_partitions|Run query: {query_string}")
    logger.info(f"@lambda_handler|update_partitions|Run query response: {response}")
