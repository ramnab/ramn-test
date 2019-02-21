import unittest
from unittest.mock import MagicMock, patch, Mock
from datetime import datetime
from datetime import timedelta
import os
import sys

script_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, script_path + '/../code')
from lambda_handler import *
from db import *


class FirstLoginTests(unittest.TestCase):

    def setUp(self):
        with open(f'{script_path}/agent-schedule.json', 'r') as f:
            self.SCHEDULE = json.loads(f.read())

    def create_event(self, **kwargs):
        return {
            "EventType": kwargs.get("typ"),
            "CurrentAgentSnapshot": {
                "Configuration": {
                    "Username": kwargs.get("username"),
                    "FirstName": kwargs.get("firstname", "Fred"),
                    "LastName": kwargs.get("lastname", "Blogs")
                },
                "AgentStatus": {
                    "Name": kwargs.get("status", "Available")
                }
            },
            "EventTimestamp": kwargs.get("ts")
        }

    @patch('db.DbTable')
    def test_First_Login_Recorded(self, db_mock):

        # determine whether history updated
        events1 = self.create_event(typ="LOGIN", username="P12125105",
                                    ts="2019-02-07T07:30:00.000Z")

        db_mock.write.return_value = ""
        user_events = {"P12125105": [events1]}
        result = capture_history(self.SCHEDULE,
                                 user_events,
                                 db_mock)
        db_entry = [{
            'username': 'P12125105',
            'event': 'LOGIN',
            'ts': '2019-02-07T07:30:00.000Z',
            'ttl': 1549558800
        }]
        self.assertTrue(db_mock.write.called)

    @patch('db.DbTable')
    def test_First_Login_Recorded_Only(self, db_mock):

        # determine whether history updated
        events1 = self.create_event(typ="LOGIN", username="P12125105",
                                    ts="2019-02-07T07:30:00.000Z")
        events2 = self.create_event(typ="LOGIN", username="P12125105",
                                    ts="2019-02-07T07:35:00.000Z")

        user_events = {"P12125105": [events1, events2]}
        
        db_entry = [{
            'username': 'P12125105',
            'event': 'LOGIN',
            'ts': '2019-02-07T07:30:00.000Z',
            'ttl': 1549558800
        }]
        db_mock.write.return_value = ""
        db_mock.write.return_value = db_entry
        result = capture_history(self.SCHEDULE,
                                 user_events,
                                 db_mock)
        self.assertTrue(db_mock.write.called)

    @patch('db.DbTable')
    def test_First_Login_Recorded_Twice(self, db_mock):

        # determine whether history updated
        events1 = self.create_event(typ="LOGIN", username="P12125105",
                                    ts="2019-02-07T07:30:00.000Z")
        events2 = self.create_event(typ="LOGIN", username="P12127256",
                                    ts="2019-02-07T07:35:00.000Z")

        user_events = {
            "P12125105": [events1],
            "P12127256": [events2]
        }
        db_mock.write.return_value = ""
        result = capture_history(self.SCHEDULE,
                                 user_events,
                                 db_mock)
        db_entry = [
            {
                'username': 'P12125105',
                'event': 'LOGIN',
                'ts': '2019-02-07T07:30:00.000Z',
                'ttl': 1549558800
            },
            {
                'username': 'P12127256',
                'event': 'LOGIN',
                'ts': '2019-02-07T07:35:00.000Z',
                'ttl': 1549571400
            }
        ]
        self.assertTrue(db_mock.write.called)


if __name__ == '__main__':
    unittest.main()
