import unittest
from unittest.mock import MagicMock, patch
import os
import sys

script_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, script_path + '/../code')
from republish import *


config = ['queue', 'startinterval', 'endinterval']


class RepublishTests(unittest.TestCase):

    @patch('boto3.resource')
    def test_Republish_ReadS3(self, mock_boto3_s3):
        mock_boto3_s3.return_value.Object.return_value \
                     .get.return_value.get.return_value \
                      .read.return_value.decode.return_value = ""

        read_s3("bucket", "key")
        self.assertTrue(mock_boto3_s3.called)
        self.assertTrue(mock_boto3_s3.return_value.Object.return_value
                                     .get.return_value.get.return_value
                                     .read.return_value.decode.called)

    def test_csv_conversion(self):
        with open("queue_interval_test.csv", "r") as f:
            csv_file = f.read()
            number_records = len(csv_file.strip().split("\n")) - 1
            report = str_to_json(csv_file, config)

            self.assertEqual(len(report), number_records)
            # with open("queue_interval_test.json", 'w') as t:
            #     t.write(json.dumps(report))

            first_entry = report[0]
            self.assertEqual(first_entry.get('queue'), 'Fraud Internal')
            self.assertEqual(first_entry.get('startinterval'), '2019-02-08T06:30:00.000Z')
            self.assertEqual(first_entry.get('aftercontactworktime'), None)
            self.assertEqual(first_entry.get('agentidletime'), 16)

    def test_normalise_field(self):
        normalised_field_1 = normalise_field("Agent on contact time")
        self.assertEqual(normalised_field_1, "agentoncontacttime")

    def test_convert_values(self):
        converted_value_1 = convert_value(config, "agentoncontacttime", "10")
        self.assertEqual(converted_value_1, 10)
        converted_value_2 = convert_value(config, "queue", "Fraud Internal")
        self.assertEqual(converted_value_2, "Fraud Internal")
        converted_value_3 = convert_value(config, "agentoncontacttime", "")
        self.assertEqual(converted_value_3, None)

    @patch('boto3.client')
    def test_republish(self, mock_boto3_fh):
        firehose = "kfh-dummy"
        with open("queue_interval_test.json", 'r') as f:
            report = json.loads(f.read())

            expected_data = report[0]
            mock_boto3_fh.return_value.put_record_batch.return_value = ""

            republish(report, firehose)
            self.assertEqual(mock_boto3_fh.return_value.put_record_batch.call_count, 1)
            call_args = tuple(mock_boto3_fh.return_value.put_record_batch._mock_call_args_list[0])[1]

            self.assertEqual(call_args.get("DeliveryStreamName"), firehose)
            actual_data = call_args.get("Records")[0].get("Data")
            self.assertTrue(isinstance(actual_data, str))
            self.assertEqual(json.loads(actual_data), expected_data)


if __name__ == '__main__':
    unittest.main()
