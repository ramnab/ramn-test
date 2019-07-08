import datetime
import json
import argparse
import os
import logging.config
import re
from abc import ABC, abstractmethod


import boto3

ROLE_ARN_TEMPLATE = "arn:aws:iam::{account_id}:role/CA_CONNECT_METRICS_{environment}"
AWS_REGION = 'eu-central-1'
METRIC_MAPPING = {
    "CONTACTS_QUEUED": "Call",
    "CONTACTS_ABANDONED": "Abandoned",
    "QUEUE_ANSWER_TIME": "ASA",
    "AGENTS_ONLINE": "Agents",
    "OLDEST_CONTACT_AGE": "MaxOCW",
    "CONTACTS_IN_QUEUE": "InQueue",
    "AGENTS_AFTER_CONTACT_WORK": "ACW",
    "AGENTS_AVAILABLE": "Available"
}

script_path = os.path.dirname(__file__)
logging.config.fileConfig(f'{script_path}/logging.ini', disable_existing_loggers=False)
logger = logging.getLogger("connectMetrics")
configuration_directory = f'{script_path}/../../../config'
output_directory = f'{script_path}/../../../output'
VERSION_RE = re.compile(r'''__version__ = ['"]([0-9.]+)['"]''')


class ConnectMetricRequest(ABC):
    queue_arn_template = "arn:aws:connect:{region}:{account_id}:instance/{instance_id}/queue/{queue_id}"

    def __init__(self, connect_client, region):
        self.connect_client = connect_client
        self.region = region

    def create_request(self, metadata):
        request = {
            "InstanceId":  metadata['instanceId'],
            "Filters": {
                'Channels': [
                    'VOICE'
                ],
                'Queues': self.construct_queue_arns(metadata)
            },
            "Groupings": [
                'QUEUE'
            ]
        }
        return request

    def construct_queue_arns(self, metadata):
        return list(
            map(
                lambda queue: self.create_queue_arn(metadata['accountId'], metadata['instanceId'], queue),
                list(metadata['queues'].keys())
            )
        )

    @abstractmethod
    def get_web_request(self):
        pass

    @staticmethod
    def create_queue_arn(account_id, instance_id, queue_id):
        return ConnectMetricRequest.queue_arn_template.format(
            account_id=account_id,
            region=AWS_REGION,
            instance_id=instance_id,
            queue_id=queue_id
        )

    def execute(self, metadata):
        request = self.create_request(metadata)
        web_request = self.get_web_request()
        response = web_request(**request)
        return response['MetricResults']


class CurrentMetricRequest(ConnectMetricRequest):
    def __init__(self, connect_client, region):
        super().__init__(connect_client, region)

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
    def __init__(self, connect_client, region):
        super().__init__(connect_client, region)

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


def get_metric_data(profile, client, environment):
    lower_client = client.lower()
    lower_environment = environment.lower()

    logger.info(
        "Retrieving metrics for profile %s, client %s and environment %s",
        profile,
        lower_client,
        lower_environment
    )
    queue_metadata = read_configuration(lower_client, lower_environment)

    connect_client = create_connect_client(profile, queue_metadata)

    metrics = make_requests(connect_client, queue_metadata)
    output_metrics(metrics, lower_client, lower_environment)


def create_connect_client(profile, queue_metadata):
    session = create_session(profile)
    credentials = assume_role(queue_metadata, session)
    logger.debug("Creating Amazon Connect client for region %s", AWS_REGION)
    connect_client = session.client(
        'connect',
        region_name=AWS_REGION,
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"]
    )
    return connect_client


def assume_role(queue_metadata, session):
    role_arn = create_role_arn(queue_metadata)
    logger.debug("Assuming role %s...", role_arn)
    sts_client = session.client("sts", region_name=AWS_REGION)
    assumed_role = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName="dashboard_connect_metrics"
    )
    credentials = assumed_role["Credentials"]
    return credentials


def create_session(profile):
    logger.debug("Creating AWS session...")
    session = boto3.Session(profile_name=profile)
    return session


def read_configuration(client, environment):
    config_file = f'{configuration_directory}/{client}-{environment}.json'
    logger.debug("Reading configuration from %s", config_file)
    with open(config_file) as f:
        queue_metadata = json.load(f)
    return queue_metadata


def make_requests(connect_client, metadata):

    current_metrics_request = CurrentMetricRequest(connect_client, AWS_REGION)
    historic_metrics_request = HistoricMetricRequest(connect_client, AWS_REGION)

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
        return METRIC_MAPPING[name]
    except KeyError:
        return name


def store_metrics(call_metrics, metrics, metadata):
    for metric in metrics:
        queue_name = lookup_queue_name(metric, metadata)
        queue = call_metrics.setdefault(queue_name, {})
        for collection in metric['Collections']:
            metric_name = lookup_metric_name(collection['Metric']['Name'])
            queue[metric_name] = int(collection['Value'])


def output_metrics(call_metrics, client, environment):
    output = []
    current_date = datetime.datetime.now()
    for queue_name, metrics in call_metrics.items():
        queue_metrics = {
            'Date': current_date.date().isoformat(),
            'Time': current_date.time().isoformat(),
            'Client': client,
            'QueueName': queue_name
        }
        for key, value in metrics.items():
            queue_metrics[key] = value
        output.append(queue_metrics)

    metric_output_file = f'{output_directory}/{client}-{environment}-metric-data.json'
    logger.debug("Saving metrics to %s", metric_output_file)

    with open(metric_output_file, 'w') as f:
        json.dump(output, f)


def lookup_queue_name(metric, metadata):
    arn = metric['Dimensions']['Queue']['Arn']
    last_slash_index = arn.rfind('/')
    queue_id = arn[last_slash_index + 1:]

    try:
        return metadata['queues'][queue_id]
    except KeyError:
        return arn


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--profile", help="The name of the AWS profile to use to authenticate the API call")
    parser.add_argument("-c", "--client", help="The name of the client to retrieve metrics for")
    parser.add_argument("-e", "--environment",
                        help="The environment to use, either dev, test, or prod",
                        choices=["dev", "test", "prod"]
                        )
    parser.add_argument("-v", "--version", help="Displays the script version", action="store_true")
    return parser.parse_args()


def create_role_arn(queue_metadata):
    return ROLE_ARN_TEMPLATE.format(
        account_id=queue_metadata["accountId"],
        environment=queue_metadata["environment"].upper()
    )


def get_version():
    init = open(os.path.join(script_path, '__init__.py')).read()
    return VERSION_RE.search(init).group(1)


if __name__ == '__main__':
    args = parse_arguments()
    if args.version:
        print(get_version())
        exit(0)

    get_metric_data(args.profile, args.client, args.environment)
    logger.info("Successfully retrieved metrics")
