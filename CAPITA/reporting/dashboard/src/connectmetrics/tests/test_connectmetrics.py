import datetime
import json
import os
from unittest.mock import patch, mock_open
from src.connectmetrics import connectmetrics

script_path = f'{os.path.dirname(connectmetrics.__file__)}/../../..'

test_config = """{
  "clientName": "client1",
  "environment": "DEV",
  "accountId": "1111111",
  "instanceId": "instance1",
  "queues": {
      "333": "BasicQueue",
      "555": "AnotherQueue"
    }
}"""

end_time = datetime.datetime.utcnow()
end_time -= datetime.timedelta(minutes=end_time.minute % 5,
                               seconds=end_time.second,
                               microseconds=end_time.microsecond)

expected_historic_metric_request = {
    "InstanceId": "instance1",
    "Filters": {
        'Channels': ['VOICE'],
        'Queues': [
            "arn:aws:connect:eu-central-1:1111111:instance/instance1/queue/333",
            "arn:aws:connect:eu-central-1:1111111:instance/instance1/queue/555"
        ]
    },
    "Groupings": ['QUEUE'],
    "StartTime": datetime.datetime.combine(datetime.datetime.today(), datetime.time.min),
    "EndTime": end_time,
    "HistoricalMetrics": [
        {'Name': 'CONTACTS_HANDLED', 'Unit': 'COUNT', 'Statistic': 'SUM'},
        {'Name': 'CONTACTS_QUEUED', 'Unit': 'COUNT', 'Statistic': 'SUM'},
        {'Name': 'ABANDON_TIME', 'Unit': 'SECONDS', 'Statistic': 'AVG'},
        {'Name': 'CONTACTS_ABANDONED', 'Unit': 'COUNT', 'Statistic': 'SUM'},
        {'Name': 'QUEUE_ANSWER_TIME', 'Unit': 'SECONDS', 'Statistic': 'AVG'}

    ]
}

expected_current_metric_request = {
    "InstanceId": "instance1",
    "Filters": {
        'Channels': ['VOICE'],
        'Queues': [
            "arn:aws:connect:eu-central-1:1111111:instance/instance1/queue/333",
            "arn:aws:connect:eu-central-1:1111111:instance/instance1/queue/555"
        ]
    },
    "Groupings": ['QUEUE'],
    "CurrentMetrics": [
        {'Name': 'AGENTS_ONLINE', 'Unit': 'COUNT'},
        {'Name': 'AGENTS_ON_CALL', 'Unit': 'COUNT'},
        {'Name': 'OLDEST_CONTACT_AGE', 'Unit': 'SECONDS'},
        {'Name': 'CONTACTS_IN_QUEUE', 'Unit': 'COUNT'},
        {'Name': 'AGENTS_AFTER_CONTACT_WORK', 'Unit': 'COUNT'},
        {'Name': 'AGENTS_AVAILABLE', 'Unit': 'COUNT'}
    ]
}

historic_metric_response = {
    "MetricResults": [
        {
            "Dimensions": {"Queue": {'Arn': "arn:aws:connect:eu-central-1:1111111:instance/instance1/queue/333"}},
            "Collections": [
                {'Metric': {'Name': 'CONTACTS_HANDLED'}, 'Value': 1},
                {'Metric': {'Name': 'CONTACTS_QUEUED'}, 'Value': 1},
                {'Metric': {'Name': 'ABANDON_TIME'}, 'Value': 1},
                {'Metric': {'Name': 'CONTACTS_ABANDONED'}, 'Value': 1},
                {'Metric': {'Name': 'QUEUE_ANSWER_TIME'}, 'Value': 1}
            ]
        },
        {
            "Dimensions": {"Queue": {'Arn': "arn:aws:connect:eu-central-1:1111111:instance/instance1/queue/555"}},
            "Collections": [
                {'Metric': {'Name': 'CONTACTS_HANDLED'}, 'Value': 1},
                {'Metric': {'Name': 'CONTACTS_QUEUED'}, 'Value': 1},
                {'Metric': {'Name': 'ABANDON_TIME'}, 'Value': 1},
                {'Metric': {'Name': 'CONTACTS_ABANDONED'}, 'Value': 1},
                {'Metric': {'Name': 'QUEUE_ANSWER_TIME'}, 'Value': 1}
            ]
        }
    ]
}

current_metric_response = {
    "MetricResults": [
        {
            "Dimensions": {"Queue": {'Arn': "arn:aws:connect:eu-central-1:1111111:instance/instance1/queue/333"}},
            "Collections": [
                {'Metric': {'Name': 'AGENTS_ONLINE'}, 'Value': 1},
                {'Metric': {'Name': 'AGENTS_ON_CALL'}, 'Value': 1},
                {'Metric': {'Name': 'OLDEST_CONTACT_AGE'}, 'Value': 1},
                {'Metric': {'Name': 'CONTACTS_IN_QUEUE'}, 'Value': 1},
                {'Metric': {'Name': 'AGENTS_AFTER_CONTACT_WORK'}, 'Value': 1},
                {'Metric': {'Name': 'AGENTS_AVAILABLE'}, 'Value': 1}
            ]
        },
        {
            "Dimensions": {"Queue": {'Arn': "arn:aws:connect:eu-central-1:1111111:instance/instance1/queue/555"}},
            "Collections": [
                {'Metric': {'Name': 'AGENTS_ONLINE'}, 'Value': 1},
                {'Metric': {'Name': 'AGENTS_ON_CALL'}, 'Value': 1},
                {'Metric': {'Name': 'OLDEST_CONTACT_AGE'}, 'Value': 1},
                {'Metric': {'Name': 'CONTACTS_IN_QUEUE'}, 'Value': 1},
                {'Metric': {'Name': 'AGENTS_AFTER_CONTACT_WORK'}, 'Value': 1},
                {'Metric': {'Name': 'AGENTS_AVAILABLE'}, 'Value': 1}
            ]
        }
    ]
}

test_date = datetime.datetime.now()

expected_mapped_metrics = [
  {
    "Date": test_date.isoformat(),
    "Client": "client1",
    "QueueName": "BasicQueue",
    "Call": 1,
    "Abandoned": 1,
    "ABANDON_TIME": 1,
    "CONTACTS_HANDLED": 1,
    "Agents": 1,
    "AGENTS_ON_CALL": 1,
    "MaxOCW": 1,
    "InQueue": 1,
    "ACW": 1,
    "Available": 1,
    "ASA": 1
  },
  {
    "Date": test_date.isoformat(),
    "Client": "client1",
    "QueueName": "AnotherQueue",
    "Call": 1,
    "Abandoned": 1,
    "ABANDON_TIME": 1,
    "CONTACTS_HANDLED": 1,
    "Agents": 1,
    "AGENTS_ON_CALL": 1,
    "MaxOCW": 1,
    "InQueue": 1,
    "ACW": 1,
    "Available": 1,
    "ASA": 1
  }
]


@patch("src.connectmetrics.connectmetrics.boto3")
@patch('builtins.open', new_callable=mock_open, read_data=test_config)
def test_that_the_config_file_is_used_matching_the_profile(open_mock, boto_mock):
    connectmetrics.get_metric_data("testprofile", "client1", "dev")
    open_mock.assert_any_call(f'{script_path}/config/client1-dev.json')


@patch("src.connectmetrics.connectmetrics.boto3")
@patch('builtins.open', new_callable=mock_open, read_data=test_config)
def test_that_the_environment_is_converted_to_lowercase_when_matching_the_profile(open_mock, boto_mock):
    connectmetrics.get_metric_data("testprofile", "client1", "DEV")
    open_mock.assert_any_call(f'{script_path}/config/client1-dev.json')


@patch("src.connectmetrics.code.connectmetrics.boto3")
@patch('builtins.open', new_callable=mock_open, read_data=test_config)
def test_that_output_is_written_to_the_profile_data_file(open_mock, boto_mock):
    connectmetrics.get_metric_data("testprofile", "client1", "dev")
    open_mock.assert_called_with(f'{script_path}/output/client1-dev-metric-data.json', 'w')


@patch("src.connectmetrics.connectmetrics.boto3")
@patch('builtins.open', new_callable=mock_open, read_data=test_config)
def test_that_the_profile_name_is_used_to_create_the_session(open_mock, boto_mock):
    connectmetrics.get_metric_data("testprofile", "client1", "dev")
    boto_mock.Session.assert_called_with(profile_name="testprofile")


@patch("src.connectmetrics.connectmetrics.boto3")
@patch('builtins.open', new_callable=mock_open, read_data=test_config)
def test_that_the_sts_is_configured_for_the_eu_central_region_with_the_assumed_role(open_mock, boto_mock):
    connectmetrics.get_metric_data("testprofile", "client1", "dev")
    boto_mock.Session.return_value.client.assert_any_call("sts", region_name="eu-central-1")


@patch("src.connectmetrics.connectmetrics.boto3")
@patch('builtins.open', new_callable=mock_open, read_data=test_config)
def test_that_the_connect_metric_role_is_assumed(open_mock, boto_mock):
    connectmetrics.get_metric_data("testprofile", "client1", "dev")
    mock_client = boto_mock.Session.return_value.client.return_value
    mock_client.assume_role.assert_any_call(
        RoleArn="arn:aws:iam::1111111:role/CA_CONNECT_METRICS_DEV",
        RoleSessionName="dashboard_connect_metrics"
    )


@patch("src.connectmetrics.connectmetrics.boto3")
@patch('builtins.open', new_callable=mock_open, read_data=test_config)
def test_that_the_connect_client_is_configured_for_the_eu_central_region_with_the_assumed_role(open_mock, boto_mock):
    mock_client = boto_mock.Session.return_value.client.return_value
    mock_client.assume_role.return_value = {
        "Credentials": {
            'AccessKeyId': 'Key1',
            'SecretAccessKey': 'Secret1',
            'SessionToken': 'Session1',
        }
    }
    connectmetrics.get_metric_data("testprofile", "client1", "dev")

    boto_mock.Session.return_value.client.assert_called_with(
        "connect",
        region_name="eu-central-1",
        aws_access_key_id="Key1",
        aws_secret_access_key="Secret1",
        aws_session_token="Session1"
    )


@patch("src.connectmetrics.connectmetrics.boto3")
@patch('builtins.open', new_callable=mock_open, read_data=test_config)
def test_that_the_current_metric_request_is_correct(open_mock, boto_mock):
    connectmetrics.get_metric_data("testprofile", "client1", "dev")
    mock_client = boto_mock.Session.return_value.client.return_value
    actual_request = mock_client.get_current_metric_data.call_args[1]
    assert expected_current_metric_request == actual_request


@patch("src.connectmetrics.connectmetrics.boto3")
@patch('builtins.open', new_callable=mock_open, read_data=test_config)
def test_that_the_historic_metric_request_is_correct(open_mock, boto_mock):
    connectmetrics.get_metric_data("testprofile", "client1", "dev")
    mock_client = boto_mock.Session.return_value.client.return_value
    actual_request = mock_client.get_metric_data.call_args[1]
    assert expected_historic_metric_request == actual_request


@patch("src.connectmetrics.connectmetrics.datetime")
@patch("src.connectmetrics.connectmetrics.json")
@patch("src.connectmetrics.connectmetrics.boto3")
@patch('builtins.open', new_callable=mock_open, read_data=test_config)
def test_that_metrics_are_mapped_to_a_flattened_structure(open_mock, boto_mock, json_mock, datetime_mock):
    mock_client = boto_mock.Session.return_value.client.return_value
    mock_client.get_metric_data.return_value = historic_metric_response
    mock_client.get_current_metric_data.return_value = current_metric_response
    datetime_mock.datetime.now.return_value = test_date
    json_mock.load.return_value = json.loads(test_config)
    connectmetrics.get_metric_data("testprofile", "client1", "dev")
    actual_mapped_metrics = json_mock.dump.call_args[0][0]
    assert expected_mapped_metrics == actual_mapped_metrics
