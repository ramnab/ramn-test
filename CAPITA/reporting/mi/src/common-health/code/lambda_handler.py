import os
import logging
import boto3
from datetime import datetime, timezone


s3_client = boto3.client("s3")
cw_client = boto3.client("cloudwatch")
logger = logging.getLogger()
# INFO = 20, DEBUG = 10
LOGGING_LEVEL = int(os.environ.get("LOGGING_LEVEL", "20"))
logger.setLevel(LOGGING_LEVEL)
namespace = os.environ.get("NAMESPACE", "CAPITA/MI")


def handler(event, _context):
    logger.info(f"@lambda_handler|handler|received event: {str(event)}")

    report_bucket = os.environ.get("REPORTING_BUCKET")
    clients = os.environ.get("CLIENTS", "tradeuk").split(',')

    rowdate = datetime.utcnow().strftime("%Y-%m-%d")
    metrics = []

    agent_intervals(metrics, report_bucket, clients, rowdate)
    queue_intervals(metrics, report_bucket, clients, rowdate)

    print(f"\n\nMetrics: {metrics}")
    logger.info(f"@lambda_handler|handler|metrics={metrics}")
    send_metrics(metrics)


def agent_intervals(metrics, bucket, clients, rowdate):

    for client in clients:

        conf = {
            'dimensions': {
                'ReportCategory': 'AgentIntervalReports',
                'Client': client
            }
        }

        prefix = f"agent_interval/clientname={client}/rowdate={rowdate}"
        conf['prefix'] = prefix
        conf['files'] = list_files(bucket, prefix)
        missing_data_metric(metrics, **conf)
        freshness_metric(metrics, **conf)


def queue_intervals(metrics, bucket, clients, rowdate):

    for client in clients:
        conf = {
            'dimensions': {
                'ReportCategory': 'AgentIntervalReports',
                'Client': client
            }
        }

        prefix = f"queue_interval/clientname={client}/rowdate={rowdate}"
        conf['prefix'] = prefix
        conf['files'] = list_files(bucket, prefix)
        missing_data_metric(metrics, **conf)
        freshness_metric(metrics, **conf)


def missing_data_metric(metrics, **kwargs):
    if not kwargs.get("files"):
        metrics.append({
            "dimensions": kwargs.get("dimensions"),
            "metric": "MissingData",
            "value": 1,
            "message": f"No reports found at {kwargs.get('prefix')}"
        })


def freshness_metric(metrics, **kwargs):
    files = kwargs.get('files')
    if not files:
        return
    last_modified = files[0].get("LastModified")
    freshness = datetime.now(timezone.utc) - last_modified
    (minutes, _seconds) = divmod(freshness.total_seconds(), 60)
    logger.info(f"last file is {minutes} minutes old")
    print(f"last file is {minutes} minutes old")
    metrics.append({
        "dimensions": kwargs.get("dimensions"),
        "metric": "Freshness",
        "value": minutes,
        "message": f"Report {files[0].get('Key')} is {minutes} minutes old"
    })


def list_files(bucket, prefix):
    files = []
    list_files1(bucket=bucket, prefix=prefix, files=files)
    return files


def list_files1(**kwargs):
    args = {
        'Bucket': kwargs.get("bucket"),
        'Prefix': kwargs.get("prefix")
    }
    token = kwargs.get("ContinuationToken")
    if token:
        args['ContinuationToken'] = token

    response = s3_client.list_objects_v2(**args)
    kwargs.get("files").extend(response.get("Contents", []))
    token = response.get('NextContinuationToken')
    if token:
        kwargs['ContinuationToken'] = token
        list_files1(**kwargs)


def send_metrics(metrics):

    metric_data = []

    for metric in metrics:
        entry = {
            'MetricName': metric.get("metric"),
            'Value': metric.get("value")
        }
        dimensions = []
        logger.info(f"Metric: {metric}")
        for key, val in metric.get("dimensions").items():
            dimensions.append({'Name': key, 'Value': val})
        entry['Dimensions'] = dimensions
        metric_data.append(entry)

    logger.info(f"send_metrics metric data: {metric_data}")
    response = cw_client.put_metric_data(
        Namespace=namespace,
        MetricData=metric_data
    )
    logger.info(f"send_metrics response = {response}")
