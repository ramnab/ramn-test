import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from datetime import timedelta
import os
import sys

script_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, script_path + '/../code')
from alarms import *
from db import *


class AlarmTests(unittest.TestCase):

    def setUp(self):
        with open(f'{script_path}/agent-schedule.json', 'r') as f:
            self.SCHEDULE = json.loads(f.read())

    def create_event(self, **kwargs):
        return [{
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
        }]

    @patch('alarms.BSE.set_alarm')
    def test_BSE_Activated(self, set_alarm_mock):
        bse = BSE(self.SCHEDULE)
        # shift starts 08:00
        # BSE if login between 07:30 and 07:55
        events1 = self.create_event(typ="LOGIN", username="P12125105",
                                    ts="2019-02-07T07:31:11.012Z")

        bse.process(events1, "P12125105", {})
        self.assertTrue(set_alarm_mock.called)

    @patch('alarms.BSE.clear_alarm')
    def test_BSE_Cleared(self, clear_alarm_mock):
        bse = BSE(self.SCHEDULE)
        events2 = self.create_event(typ="SP_HEART_BEAT", username="P12125105",
                                    ts="2019-02-07T07:56:0.000Z")
        bse.process(events2,
                    "P12125105",
                    {
                        "extra": {
                            "end": "2019-02-07T07:55"
                        }
                    })
        self.assertTrue(clear_alarm_mock.called)

    @patch('alarms.ESE.set_alarm')
    def test_ESE_Activated(self, set_alarm_mock):
        ese = ESE(self.SCHEDULE)
        events1 = self.create_event(typ="LOGOUT", username="P12125105",
                                    ts="2019-02-07T16:57:00.012Z")
        ese.process(events1, "P12125105", {})
        self.assertTrue(set_alarm_mock.called)

    @patch('alarms.ESL.set_alarm')
    def test_ESL_Activated(self, set_alarm_mock):
        esl = ESL(self.SCHEDULE)
        events1 = self.create_event(typ="SP_HEART_BEAT", username="P12125105",
                                    ts="2019-02-07T17:10:00.012Z")
        esl.process(events1, "P12125105", {})
        self.assertTrue(set_alarm_mock.called)

    @patch('alarms.BBE.set_alarm')
    def test_BBE_Activated(self, set_alarm_mock):
        bbe = BBE(self.SCHEDULE)
        events1 = self.create_event(typ="SP_HEART_BEAT", username="P12125105",
                                    ts="2019-02-07T14:47:00.012Z",
                                    status="Break")
        bbe.process(events1, "P12125105", {})
        self.assertTrue(set_alarm_mock.called)

    @patch('alarms.EBL.set_alarm')
    def test_EBL_Activated(self, set_alarm_mock):
        ebl = EBL(self.SCHEDULE)
        events1 = self.create_event(typ="SP_HEART_BEAT", username="P12125105",
                                    ts="2019-02-07T15:27:00.012Z",
                                    status="Break")
        ebl.process(events1, "P12125105", {})
        self.assertTrue(set_alarm_mock.called)

    @patch('alarms.SIU.set_alarm')
    def test_SIU_Activated_Early(self, set_alarm_mock):
        siu = SIU(self.SCHEDULE)
        events1 = self.create_event(typ="LOGIN", username="P12125105",
                                    ts="2019-02-07T07:24:00.012Z")
        siu.process(events1, "P12125105", {})
        self.assertTrue(set_alarm_mock.called)

    @patch('alarms.SIU.set_alarm')
    def test_SIU_Activated_Late(self, set_alarm_mock):
        siu = SIU(self.SCHEDULE)
        events1 = self.create_event(typ="LOGIN", username="P12125105",
                                    ts="2019-02-07T17:37:00.012Z")
        siu.process(events1, "P12125105", {})
        self.assertTrue(set_alarm_mock.called)

    @patch('alarms.SOU.set_alarm')
    def test_SOU_Activated(self, set_alarm_mock):
        sou = SOU(self.SCHEDULE)
        events1 = self.create_event(typ="LOGOUT", username="P12125105",
                                    ts="2019-02-07T15:56:00.012Z",
                                    status="Offline")
        sou.process(events1, "P12125105", {})
        self.assertTrue(set_alarm_mock.called)

    @patch('alarms.SOU.clear_alarm')
    def test_SOU_Clear_Login(self, clear_alarm_mock):
        sou = SOU(self.SCHEDULE)
        events1 = self.create_event(typ="LOGIN", username="P12125105",
                                    ts="2019-02-07T16:56:00.012Z",
                                    status="Offline")
        sou.process(events1, "P12125105", {"end": "2019-02-07T17:00"})
        self.assertTrue(clear_alarm_mock.called)

    @patch('alarms.SOU.clear_alarm')
    def test_SOU_Clear_HB(self, clear_alarm_mock):
        sou = SOU(self.SCHEDULE)
        events1 = self.create_event(typ="SP_HEART_BEAT", username="P12125105",
                                    ts="2019-02-07T17:01:00.012Z",
                                    status="Offline")
        sou.process(events1,
                    "P12125105",
                    {
                        "extra": {
                            "end": "2019-02-07T17:00"
                        }
                    })
        self.assertTrue(clear_alarm_mock.called)

    @patch('alarms.WOB.set_alarm')
    def test_WOB_Activate(self, set_alarm_mock):
        wob = WOB(self.SCHEDULE)
        events1 = self.create_event(typ="SP_HEART_BEAT", username="P12125105",
                                    ts="2019-02-07T15:07:00.012Z",
                                    status="Available")
        wob.process(events1, "P12125105", {})
        self.assertTrue(set_alarm_mock.called)

    @patch('alarms.BXE.set_alarm')
    def test_BXE_WithNoExceptions(self, set_alarm_mock):
        bxe = BXE(self.SCHEDULE)
        events1 = self.create_event(typ="SP_HEART_BEAT", username="P12125105",
                                    ts="2019-02-07T15:07:00.012Z",
                                    status="Available")
        bxe.process(events1, "P12125105", {})
        self.assertFalse(set_alarm_mock.called)

    @patch('alarms.BSL.set_alarm')
    def test_BSL_ActivateOnSpecialHB(self, set_alarm_mock):
        bsl = BSL(self.SCHEDULE)
        events1 = self.create_event(typ="SP_HEART_BEAT",
                                    username="P12125105",
                                    ts="2019-02-07T15:07:00.012Z",
                                    status="Available")
        bsl.process(events1, "P12125105", {}, [])
        self.assertTrue(set_alarm_mock.called)

    @patch('alarms.BSL.set_alarm')
    def test_BSL_Not_Activate_Previously_LoggedIn(self, set_alarm_mock):
        bsl = BSL(self.SCHEDULE)
        events1 = self.create_event(typ="SP_HEART_BEAT",
                                    username="P12125105",
                                    ts="2019-02-07T15:07:00.012Z",
                                    status="Available")
        history = [
            {
                "username": "P12125105",
                "prop": "LOGIN"
            }
        ]
        bsl.process(events1, "P12125105", {}, history)
        self.assertFalse(set_alarm_mock.called)

    @patch('alarms.BSL.clear_alarm')
    def test_BSL_Cleared(self, clear_alarm_mock):
        bsl = BSL(self.SCHEDULE)
        events1 = self.create_event(typ="LOGIN", username="P12125105",
                                    ts="2019-02-07T08:06:00.012Z")
        bsl.process(events1, "P12125105", {"end": "2019-02-07T17:00"})
        self.assertTrue(clear_alarm_mock.called)

    @patch('alarms.BSL.update_display_ts')
    def test_BSL_UpdateTS(self, update_display_ts):
        bsl = BSL(self.SCHEDULE)
        events1 = self.create_event(typ="SP_HEART_BEAT",
                                    username="P12125105",
                                    ts="2019-02-07T08:06:00.012Z")
        bsl.process(events1,
                    "P12125105",
                    {
                        "extra": {
                            "start": "2019-02-07T08:00",
                            "end": "2019-02-07T17:00"
                        }
                    }
                    )
        self.assertTrue(update_display_ts.called)

if __name__ == '__main__':
    unittest.main()
