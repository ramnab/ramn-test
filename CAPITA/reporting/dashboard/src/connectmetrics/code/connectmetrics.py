import datetime
import json
import argparse
import os
import logging.config
from abc import ABC, abstractmethod


import boto3

script_path = os.path.dirname(__file__)
logging.config.fileConfig(f'{script_path}/logging.ini', disable_existing_loggers=False)
logger = logging.getLogger("connectMetrics")

aws_region = 'eu-central-1'
metric_mapping = {
    "CONTACTS_QUEUED": "Call",
    "CONTACTS_ABANDONED": "Abandoned",
    "QUEUE_ANSWER_TIME": "ASA",
    "AGENTS_ONLINE": "Agents",
    "OLDEST_CONTACT_AGE": "MaxOCW",
    "CONTACTS_IN_QUEUE": "InQueue",
    "AGENTS_AFTER_CONTACT_WORK": "ACW",
    "AGENTS_AVAILABLE": "Available"
}


configuration_directory = f'{script_path}/../../../config'
output_directory = f'{script_path}/../../../output'


class ConnectMetricRequest(ABC):
    def __init__(self, connect_client):
        self.connect_client = connect_client

    def create_request(self, metadata):
        request = {
            "InstanceId":  metadata['instanceId'],
            "Filters": {
                'Channels': [
                    'VOICE'
                ],
                'Queues': list(metadata['queues'].keys())
            },
            "Groupings": [
                'QUEUE'
            ]
        }
        return request

    @abstractmethod
    def get_web_request(self):
        pass

    def execute(self, metadata):
        request = self.create_request(metadata)
        web_request = self.get_web_request()
        response = web_request(**request)
        return response['MetricResults']


class CurrentMetricRequest(ConnectMetricRequest):
    def __init__(self, connect_client):
        super().__init__(connect_client)

    def create_request(self, metadata):
        request = super().create_request(metadata)
        request['CurrentMetrics'] = [
            {
                'Name': 'AGENTS_ONLINE',
                'Unit': 'COUNT'
            },
            {
                'Name': 'AGENTS_ON_CALL',
                'Unit': 'COUNT'
            },
            {
                'Name': 'OLDEST_CONTACT_AGE',
                'Unit': 'SECONDS'
            },
            {
                'Name': 'CONTACTS_IN_QUEUE',
                'Unit': 'COUNT'
            },
            {
                'Name': 'AGENTS_AFTER_CONTACT_WORK',
                'Unit': 'COUNT'
            },
            {
                'Name': 'AGENTS_AVAILABLE',
                'Unit': 'COUNT'
            }
        ]
        return request

    def get_web_request(self):
        return self.connect_client.get_current_metric_data


class HistoricMetricRequest(ConnectMetricRequest):
    def __init__(self, connect_client):
        super().__init__(connect_client)

    def create_request(self, metadata):
        request = super().create_request(metadata)
        request['HistoricalMetrics'] = [
            {
                'Name': 'CONTACTS_HANDLED',
                'Unit': 'COUNT',
                'Statistic': 'SUM'
            },
            {
                'Name': 'CONTACTS_QUEUED',
                'Unit': 'COUNT',
                'Statistic': 'SUM'
            },
            {
                'Name': 'ABANDON_TIME',
                'Unit': 'SECONDS',
                'Statistic': 'AVG'
            },
            {
                'Name': 'CONTACTS_ABANDONED',
                'Unit': 'COUNT',
                'Statistic': 'SUM'
            },
            {
                'Name': 'QUEUE_ANSWER_TIME',
                'Unit': 'SECONDS',
                'Statistic': 'AVG'
            }

        ]

        start_time = self.get_midnight()

        end_time = self.get_five_minute_interval_timestamp(datetime.datetime.utcnow())

        request["StartTime"] = start_time
        request["EndTime"] = end_time
        return request

    def get_web_request(self):
        return self.connect_client.get_metric_data

    @staticmethod
    def get_five_minute_interval_timestamp(date):
        date -= datetime.timedelta(minutes=date.minute % 5,
                                   seconds=date.second,
                                   microseconds=date.microsecond)
        return date

    @staticmethod
    def get_midnight():
        midnight = datetime.datetime.combine(datetime.datetime.today(), datetime.time.min)
        return midnight


def get_metric_data(profile, configuration):
    queue_metadata = read_configuration(configuration)

    connect_client = create_connect_client(profile, queue_metadata)

    metrics = make_requests(connect_client, queue_metadata)
    output_metrics(metrics, queue_metadata["clientName"], configuration)


def create_connect_client(profile, queue_metadata):
    session = create_session(profile)
    credentials = assume_role(queue_metadata, session)
    logger.debug("Creating Amazon Connect client for region %s", aws_region)
    connect_client = session.client(
        'connect',
        region_name=aws_region,
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"]
    )
    return connect_client


def assume_role(queue_metadata, session):
    logger.debug("Assuming role %s...", queue_metadata["metricsRoleArn"])
    sts_client = session.client("sts", region_name=aws_region)
    assumed_role = sts_client.assume_role(
        RoleArn=queue_metadata["metricsRoleArn"],
        RoleSessionName="dashboard_connect_metrics"
    )
    credentials = assumed_role["Credentials"]
    return credentials


def create_session(profile):
    logger.debug("Creating AWS session...")
    session = boto3.Session(profile_name=profile)
    return session


def read_configuration(configuration):
    config_file = f'{configuration_directory}/{configuration}.json'
    logger.debug("Reading configuration from %s", config_file)
    with open(config_file) as f:
        queue_metadata = json.load(f)
    return queue_metadata


def make_requests(connect_client, metadata):

    current_metrics_request = CurrentMetricRequest(connect_client)
    historic_metrics_request = HistoricMetricRequest(connect_client)

    call_metrics = {}

    logger.info("Requesting historic metrics...")
    metrics = historic_metrics_request.execute(metadata)
    store_metrics(call_metrics, metrics, metadata)

    logger.info("Requesting current metrics...")
    current_metrics = current_metrics_request.execute(metadata)
    store_metrics(call_metrics, current_metrics, metadata)

    return call_metrics


def lookup_metric_name(name):
    try:
        return metric_mapping[name]
    except KeyError:
        return name


def store_metrics(call_metrics, metrics, metadata):
    for metric in metrics:
        queue_name = lookup_queue_name(metric, metadata)
        queue = call_metrics.setdefault(queue_name, {})
        for collection in metric['Collections']:
            metric_name = lookup_metric_name(collection['Metric']['Name'])
            queue[metric_name] = int(collection['Value'])


def output_metrics(call_metrics, client, configuration):
    output = []
    for queue_name, metrics in call_metrics.items():
        queue_metrics = {'Date': datetime.datetime.now().isoformat(), 'Client': client, 'QueueName': queue_name}
        for key, value in metrics.items():
            queue_metrics[key] = value
        output.append(queue_metrics)

    metric_output_file = f'{output_directory}/{configuration}-metric-data.json'
    logger.debug("Saving metrics to %s", metric_output_file)

    with open(metric_output_file, 'w') as f:
        json.dump(output, f)


def lookup_queue_name(metric, metadata):
    arn = metric['Dimensions']['Queue']['Arn']
    try:
        return metadata['queues'][arn]
    except KeyError:
        return arn


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("profile", help="The name of the AWS profile to use to authenticate the API call")
    parser.add_argument("configuration", help="The name of the configuration to use to access the API")
    parser.add_argument(
        "-v",
        "--verbosity",
        help="Adjusts the logging level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="DEBUG"
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    logger.info("Retrieving metrics for profile %s and configuration %s", args.profile, args.configuration)

    get_metric_data(args.profile, args.configuration)
    logger.info("Successfully retrieved metrics")
