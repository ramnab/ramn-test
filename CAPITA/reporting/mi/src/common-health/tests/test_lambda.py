import unittest
import os
import sys
from unittest.mock import patch
from datetime import datetime, timedelta, timezone


script_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, script_path + '/../code')
import lambda_handler as lh  # noqa


class LambdaTestCase(unittest.TestCase):

    @patch('lambda_handler.list_files')
    def test_agent_interval_missing_metric(self, mock_list_files):
        metrics = []
        mock_list_files.return_value = []
        lh.agent_intervals(metrics, 'dummy_s3', ['tradeuk'], 'dummy_rowdate')
        self.assertTrue(mock_list_files.called)
        self.assertEqual(len(metrics), 1)
        self.assertEqual(metrics[0].get('metric'), "MissingData")

    @patch('lambda_handler.list_files')
    def test_agent_interval_freshness_metric(self, mock_list_files):
        metrics = []
        file_date = datetime.now(timezone.utc) - timedelta(minutes=10)
        mock_list_files.return_value = [{
            'LastModified': file_date
        }]
        lh.agent_intervals(metrics, 'dummy_s3', ['tradeuk'], 'dummy_rowdate')
        print(metrics)
        self.assertTrue(mock_list_files.called)
        self.assertEqual(len(metrics), 1)
        self.assertEqual(metrics[0].get('metric'), "Freshness")
        self.assertEqual(metrics[0].get('value'), 10.0)


if __name__ == '__main__':
    unittest.main()
