import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from datetime import timedelta
import os
import sys

script_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, script_path + '/../code')
from alarms import *


class AlarmTests(unittest.TestCase):

    SCHEDULE = {
        "P0001": {
            "SCHEDULE": {
                "SHIFT": {
                    # shift 08:00 - 16:30
                    "T1": "2019-01-21T08:00",
                    "T2": "2019-01-21T16:30"
                }
            },
            "ALARMS": {
                "BSE": [{
                    # 07:30 - 07:55
                    "T1": "2019-01-21T07:30",
                    "T2": "2019-01-21T07:55"
                }],
                "BSL": [{
                    # > 08:05
                    "T1": "2019-01-21T08:05",
                    "T2": "2019-01-21T16:30"
                }],
                "ESE": [{
                    # < 16:25
                    "T1": "2019-01-21T16:25",
                    "T2": "2019-01-21T16:30"
                }],
                "ESL": [{
                    # 16:35 < ts < 17:00
                    "T1": "2019-01-21T16:35",
                    "T2": "2019-01-21T17:00"
                }],
                "BBE": [
                    {
                        # break is 13:00 - 14:00
                        # 12:30 < ts < 12:55
                        "start": "2019-01-21T13:00",
                        "T1": "2019-01-21T12:30",
                        "T2": "2019-01-21T12:55"
                    }
                ],
                "EBL": [
                    {
                        # break is 13:00 - 14:00
                        # 14:05 < ts < 14:30
                        "start": "2019-01-21T13:00",
                        "T1": "2019-01-21T14:05",
                        "T2": "2019-01-21T14:30"
                    }
                ],
                "SIU": [{
                    # > 17:00
                    "T1": "2019-01-21T17:00",
                    "T2": "2019-01-21T17:05"
                }],
                "SOU": [{
                    # < 16:25 (shift end is 16:30)
                    "T1": "2019-01-21T16:25"
                }],
                "WOB": [
                    {
                        # break is 13:00 - 14:00
                        # 13:05 < ts < 13:55
                        "start": "2019-01-21T13:00",
                        "T1": "2019-01-21T13:05",
                        "T2": "2019-01-21T13:55"
                    }
                ],
                "BXE": [
                    {
                        # exception work is 13:00 - 14:00
                        # 13:05 < ts < 13:55
                        "start": "2019-01-21T13:00",
                        "T1": "2019-01-21T13:05",
                        "T2": "2019-01-21T13:55"
                    }
                ],
                "EXL": [
                    {
                        # excption work is 13:00 - 14:00
                        # 14:05 < ts < 14:30
                        "T1": "2019-01-21T14:05",
                        "T2": "2019-01-21T14:30"
                    }
                ],
                "WOX": [
                    {
                        # exception work is 13:00 - 14:00
                        # 13:05 < ts < 13:55
                        "start": "2019-01-21T13:00",
                        "T1": "2019-01-21T13:05",
                        "T2": "2019-01-21T13:55"
                    }
                ]
            }
        }  
    }          

    def create_event(self, typ, username, ts, status='Available'):
        return [
            {
                "EventType": typ,
                "CurrentAgentSnapshot": {
                    "Configuration": {
                        "Username": username
                    },
                    "AgentStatus": {
                        "Name": status
                    }
                },
                "EventTimestamp": ts
            }
        ]

    @patch('alarms.BSE.set_alarm')
    def test_BSE_Activated(self, set_alarm_mock):
        bse = BSE(self.SCHEDULE)
        events1 = self.create_event("LOGIN", "P0001", 
                                    "2019-01-21T07:33:00.012Z")

        bse.process(events1, "P0001", False)
        self.assertTrue(set_alarm_mock.called)

    @patch('alarms.BSE.clear_alarm')
    def test_BSE_Cleared(self, clear_alarm_mock):
        bse = BSE(self.SCHEDULE)
        events2 = self.create_event("HEART_BEAT", "P0001",
                                    "2019-01-21T07:55:00.012Z")
        bse.process(events2, "P0001", True)
        self.assertTrue(clear_alarm_mock.called)

    @patch('alarms.BSL.set_alarm')
    def test_BSL_Activated(self, set_alarm_mock):
        bsl = BSL(self.SCHEDULE)
        events1 = self.create_event("HEART_BEAT", "P0001",
                                    "2019-01-21T08:06:00.012Z", "Offline")

        bsl.process(events1, "P0001", False)
        self.assertTrue(set_alarm_mock.called)

    @patch('alarms.BSL.clear_alarm')
    def test_BSL_Cleared(self, clear_alarm_mock):
        bsl = BSL(self.SCHEDULE)
        events2 = self.create_event("LOGIN", "P0001",
                                    "2019-01-21T16:32:00.012Z")
        bsl.process(events2, "P0001", True)
        self.assertTrue(clear_alarm_mock.called)

    @patch('alarms.ESE.set_alarm')
    def test_ESE_Activated(self, set_alarm_mock):
        ese = ESE(self.SCHEDULE)
        events1 = self.create_event("LOGOUT", "P0001",
                                    "2019-01-21T16:26:00.012Z")

        ese.process(events1, "P0001", False)
        self.assertTrue(set_alarm_mock.called)

    @patch('alarms.ESL.set_alarm')
    def test_ESL_Activated(self, set_alarm_mock):
        esl = ESL(self.SCHEDULE)
        events1 = self.create_event("HEART_BEAT", "P0001", 
                                    "2019-01-21T16:36:00.012Z", "Available")

        esl.process(events1, "P0001", False)
        self.assertTrue(set_alarm_mock.called)

    @patch('alarms.BBE.set_alarm')
    def test_BBE_Activated(self, set_alarm_mock):
        bbe = BBE(self.SCHEDULE)
        events1 = self.create_event("HEART_BEAT", "P0001",
                                    "2019-01-21T12:40:00.012Z", "Lunch")

        bbe.process(events1, "P0001", False)
        self.assertTrue(set_alarm_mock.called)

    @patch('alarms.EBL.set_alarm')
    def test_EBL_Activated(self, set_alarm_mock):
        ebl = EBL(self.SCHEDULE)
        events1 = self.create_event("HEART_BEAT", "P0001",
                                    "2019-01-21T14:25:00.012Z", "Break")

        ebl.process(events1, "P0001", False)
        self.assertTrue(set_alarm_mock.called)

    @patch('alarms.SIU.set_alarm')
    def test_SIU_Activated(self, set_alarm_mock):
        siu = SIU(self.SCHEDULE)
        events1 = self.create_event("LOGIN", "P0001",
                                    "2019-01-21T17:05:00.012Z")

        siu.process(events1, "P0001", False)
        self.assertTrue(set_alarm_mock.called)

    @patch('alarms.SOU.set_alarm')
    def test_SOU_Activated(self, set_alarm_mock):
        sou = SOU(self.SCHEDULE)
        events1 = self.create_event("LOGOUT", "P0001",
                                    "2019-01-21T16:20:00.012Z", "Offline")

        sou.process(events1, "P0001", False)
        self.assertTrue(set_alarm_mock.called)

    @patch('alarms.SOU.clear_alarm')
    def test_SOU_Clear_Login(self, clear_alarm_mock):
        sou = SOU(self.SCHEDULE)
        events1 = self.create_event("LOGIN", "P0001",
                                    "2019-01-21T16:20:20.012Z", "Offline")

        sou.process(events1, "P0001", True)
        self.assertTrue(clear_alarm_mock.called)

    @patch('alarms.SOU.clear_alarm')
    def test_SOU_Clear_HB(self, clear_alarm_mock):
        sou = SOU(self.SCHEDULE)
        events1 = self.create_event("HEART_BEAT", "P0001",
                                    "2019-01-21T16:31:00.012Z", "Offline")

        sou.process(events1, "P0001", True)
        self.assertTrue(clear_alarm_mock.called)

    @patch('alarms.WOB.set_alarm')
    def test_WOB_Activate(self, set_alarm_mock):
        wob = WOB(self.SCHEDULE)
        events1 = self.create_event("HEART_BEAT", "P0001",
                                    "2019-01-21T13:16:00.012Z", "Available")

        wob.process(events1, "P0001", False)
        self.assertTrue(set_alarm_mock.called)


if __name__ == '__main__':
    unittest.main()
