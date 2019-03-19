from unittest import mock
import os
import sys
from datetime import datetime


script_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, script_path + '/../code')
from lambda_handler import *


@mock.patch("boto3.resource")
def test_create_folder(boto_mock):

    bucket = "bucket"
    tablename = "tablename"
    client = "client"
    rowdate = datetime.now().strftime('%Y-%m-%d')

    boto_mock.return_value.Object.return_value.put.return_value = "response"
    create_folder_partition(bucket, tablename, client)
    assert boto_mock.called
    assert boto_mock.return_value.Object.return_value.put.called
    mock_args, _mock_kwargs = boto_mock.return_value.Object.call_args

    key = f"{tablename}/clientname={client}/rowdate={rowdate}/"
    assert mock_args[0] == bucket
    assert mock_args[1] == key


@mock.patch("boto3.client")
def test_update_partition(boto_mock):

    db = "db"
    tablename = "tablename"

    boto_mock.return_value.start_query_execution.return_value = "response"
    update_partitions(db, tablename)
    assert boto_mock.called
    assert boto_mock.return_value.start_query_execution.called

    _mock_args, mock_kwargs = boto_mock.return_value.start_query_execution.call_args
    assert mock_kwargs.get('QueryExecutionContext') == {'Database': db}
    assert mock_kwargs.get('QueryString') == f'MSCK REPAIR TABLE {tablename};'


@mock.patch("lambda_handler.create_folder_partition")
@mock.patch("lambda_handler.update_partitions")
@mock.patch("lambda_handler.os.environ.get")
def test_lambda_handler(mock_os, mock_paritions, mock_create_folder):

    mock_os.side_effect = ["DB", "TABLE", "BUCKET", "CLIENT"]
    handler({}, None)
    assert mock_paritions.called
    assert mock_create_folder.called

    mock_args, _mock_kwargs = mock_paritions.call_args
    assert mock_args[0] == "DB"
    assert mock_args[1] == "TABLE"

    mock_args, _mock_kwargs = mock_create_folder.call_args
    assert mock_args[0] == "BUCKET"
    assert mock_args[1] == "TABLE"
    assert mock_args[2] == "CLIENT"
