import unittest
from unittest.mock import patch, Mock
import os
import sys
import csv
import json


script_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, script_path + '/../code')
import verify.code.lambda_handler as la  # noqa


def load_local_file(file):
    with open(file) as f:
        return f.read()


def load_schedule(file):
    data = load_local_file(file)
    schedule = csv.DictReader(data.splitlines())
    return la.convert_schedule_to_json({}, schedule)


class VerifyTests(unittest.TestCase):

    def test_row_missing_start_moment(self):
        row = {}
        errors = la.verify_schedule_contents(row)
        self.assertEqual(len(errors), 3)

    @patch("verify.code.lambda_handler.sns_error")
    def test_valid_schedule_to_json(self, mock_sns):
        (schedule, errors) = load_schedule('TUK-ASPECT-WELL-FORMED.csv')
        self.assertEqual(len(errors), 0)
        self.assertEqual(len(schedule.keys()), 1)
        self.assertIsNotNone(schedule.get("P99999999"))
        self.assertFalse(mock_sns.called)

    def test_alarms_for_found_client_TUK(self):
        (schedule, _errors) = load_schedule('TUK-ASPECT-WELL-FORMED.csv')
        alarm_config = json.loads(load_local_file('test_alarm_config.json'))
        for agent in schedule:
            schedule[agent]["ALARMS"] = la.create_alarms(schedule, agent, alarm_config)
        print(schedule)
        self.assertEqual(len(schedule['P99999999']['ALARMS']), 1)

    def test_alarms_for_unknown_client(self):
        (schedule, _errors) = load_schedule('TUK-ASPECT-WELL-FORMED-UNK_CLIENT.csv')
        alarm_config = json.loads(load_local_file('test_alarm_config.json'))
        for agent in schedule:
            schedule[agent]["ALARMS"] = la.create_alarms(schedule, agent, alarm_config)
        self.assertEqual(len(schedule['P99999999']['ALARMS']), 4)


if __name__ == '__main__':
    unittest.main()
