import unittest
from unittest.mock import patch, Mock
import os
import sys
import csv


script_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, script_path + '/../code')
import verify.code.lambda_handler as la  # noqa


class VerifyTests(unittest.TestCase):

    def test_row_missing_start_moment(self):
        row = {}
        errors = la.verify_schedule_contents(row)
        self.assertEqual(len(errors), 3)

    @patch("verify.code.lambda_handler.sns_error")
    def test_valid_schedule_to_json(self, mock_sns):
        with open('TUK-ASPECT-WELL-FORMED.csv') as f:
            data = f.read()
            schedule = csv.DictReader(data.splitlines())
            (sched, errors) = la.convert_schedule_to_json({}, schedule)

            self.assertEqual(len(errors), 0)
            self.assertEqual(len(sched.keys()), 1)
            self.assertIsNotNone(sched.get("P99999999"))
            self.assertFalse(mock_sns.called)


if __name__ == '__main__':
    unittest.main()
