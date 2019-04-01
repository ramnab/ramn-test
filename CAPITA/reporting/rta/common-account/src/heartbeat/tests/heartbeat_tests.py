import unittest
from unittest.mock import MagicMock, patch, Mock
import os
import sys

script_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, script_path + '/../code')
from lambda_handler import *


class ScheduleTests(unittest.TestCase):

    @patch('boto3.client')
    def test_Start_Schedule(self, client_mock):
        os.environ['HB'] = '123'
        client_mock.return_value.enable_rule.return_value = "asdf"
        client_mock.return_value.disable_rule.return_value = "asdf"
        handler({"schedule": "start"}, None)
        self.assertTrue(client_mock.return_value.enable_rule.called)
        self.assertFalse(client_mock.return_value.disable.called)

    @patch('boto3.client')
    def test_Stop_Schedule(self, client_mock):
        os.environ['HB'] = '123'
        client_mock.return_value.disable_rule.return_value = "asdf"
        handler({"schedule": "stop"}, None)
        self.assertTrue(client_mock.return_value.disable_rule.called)
        self.assertFalse(client_mock.return_value.enable_rule.called)

if __name__ == '__main__':
    unittest.main()
