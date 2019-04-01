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
                    "start": "2019-01-21T08:00",
                    "end": "2019-01-21T16:30",
                    "T1": "2019-01-21T07:30",
                    "T2": "2019-01-21T07:55"
                }],
                "BSL": [{
                    # > 08:05
                    "start": "2019-01-21T08:00",
                    "end": "2019-01-21T16:30",
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
                        "end": "2019-01-21T14:00",
                        "T1": "2019-01-21T14:05",
                        "T2": "2019-01-21T14:30"
                    }
                ],
                "SIU": [{
                    # > 17:00
                    "start": "2019-01-21T08:00",
                    "end": "2019-01-21T16:30",
                    "T1": "2019-01-21T07:25",
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
                        "end": "2019-01-21T14:00",
                        "T1": "2019-01-21T13:05",
                        "T2": "2019-01-21T13:55"
                    }
                ],
                "WOE": [
                    {
                        # exception is 14:00 - 15:00
                        # 14:05 < ts < 14:55
                        "start": "2019-01-21T14:00",
                        "end": "2019-01-21T15:00",
                        "T1": "2019-01-21T14:05",
                        "T2": "2019-01-21T14:55"
                    }
                ],
                "BXE": [
                    {
                        # exception work is 13:00 - 14:00
                        # 12:45 < ts < 12:55
                        "start": "2019-01-21T13:00",
                        "T1": "2019-01-21T12:45",
                        "T2": "2019-01-21T12:55"
                    }
                ],
                "EXL": [
                    {
                        # excption work is 13:00 - 14:00
                        # 14:05 < ts < 14:15
                        "start": "2019-01-21T13:00",
                        "end": "2019-01-21T14:00",
                        "T1": "2019-01-21T14:05",
                        "T2": "2019-01-21T14:15"
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

    # ------------------------------------------------
    # WOE tests
    # 14:05 < ts < 14:55
    def test_WOE_Activate_WorkStatus_During_Exc(self):
        """
        Trigger alarm when agent has a work status
        during an scheduled exception
        Display time is from the start of the exception
        to the heart beat
        """
        woe = WOE(self.SCHEDULE)
        events1 = self.create_event("SP_HEART_BEAT", "P0001",
                                    "2019-01-21T14:16:00.012Z",
                                    "Available")

        alarms = woe.process(events1, "P0001", {})
        self.assertEqual(len(alarms), 1)
        self.assertEqual(alarms[0].get("type"), "put")
        self.assertTrue(alarms[0].get("item"))
        self.assertEqual(alarms[0].get("item").get("alarmcode"), "WOE")
        self.assertEqual(alarms[0].get("item").get("display_ts"), "00:16:00")

    def test_WOE_Activate_StatusChange_To_Working_Pending(self):
        """
        Trigger alarm when agent sets a work status
        during an scheduled exception
        Display time is reset to 0
        """
        woe = WOE(self.SCHEDULE)
        events1 = self.create_event("STATE_CHANGE", "P0001",
                                    "2019-01-21T14:01:00.012Z",
                                    "Available")

        alarms = woe.process(events1, "P0001", {})
        self.assertEqual(len(alarms), 1)
        self.assertEqual(alarms[0].get("type"), "put")
        self.assertTrue(alarms[0].get("item"))
        self.assertEqual(alarms[0].get("item").get("alarmcode"), "WOE")
        self.assertEqual(alarms[0].get("item")
                                  .get("extra")
                                  .get("status"), "pending")
        self.assertEqual(alarms[0].get("item").get("display_ts"), "00:00:00")

    def test_WOE_Clear_StatusChange(self):
        """
        Clear alarm when agent has a non work status
        during an scheduled exception
        """
        woe = WOE(self.SCHEDULE)
        events1 = self.create_event("STATE_CHANGE", "P0001",
                                    "2019-01-21T14:16:00.012Z",
                                    "Lunch")

        extra = {
            "start": "2019-01-21T13:00"
        }
        alarms = woe.process(events1, "P0001", {"extra": extra})
        self.assertEqual(len(alarms), 1)
        self.assertEqual(alarms[0].get("type"), "delete")
        self.assertTrue(alarms[0].get("key"))
        self.assertEqual(alarms[0].get("key").get("alarmcode"), "WOE")

    def test_WOE_Activate_Pending(self):
        """
        Clear alarm when agent has a non work status
        during an scheduled exception
        """
        woe = WOE(self.SCHEDULE)
        events1 = self.create_event("SP_HEART_BEAT", "P0001",
                                    "2019-01-21T14:16:00.012Z",
                                    "Available")

        state = {
            "extra": {
                "start": "2019-01-21T13:10",
                "status": "pending"
            },
            "alarmcode": "WOE"
        }
        alarms = woe.process(events1, "P0001", state)
        self.assertEqual(len(alarms), 1)
        self.assertEqual(alarms[0].get("type"), "put")
        self.assertTrue(alarms[0].get("item"))
        self.assertEqual(alarms[0].get("item").get("alarmcode"), "WOE")
        self.assertEqual(alarms[0].get("item").get("extra").get("status"), "active")

    def test_WOE_NoActivate_Pending(self):
        """
        Clear alarm when agent has a non work status
        during an scheduled exception
        """
        woe = WOE(self.SCHEDULE)
        events1 = self.create_event("SP_HEART_BEAT", "P0001",
                                    "2019-01-21T14:16:00.012Z",
                                    "Available")

        extra = {
            "start": "2019-01-21T14:12",
            "status": "pending"
        }
        alarms = woe.process(events1, "P0001", {"extra": extra})
        self.assertEqual(len(alarms), 1)

    # ------------------------------------------------
    # WOB tests
    # # 13:05 < ts < 13:55
    def test_WOB_Activate_WorkStatus_During_Break(self):
        """
        Trigger alarm when agent has a work status
        during an scheduled break
        Display time is from the start of the break
        to the heart beat
        """
        wob = WOB(self.SCHEDULE)
        events1 = self.create_event("SP_HEART_BEAT", "P0001",
                                    "2019-01-21T13:06:00.012Z",
                                    "Available")

        alarms = wob.process(events1, "P0001", {})
        self.assertEqual(len(alarms), 1)
        self.assertEqual(alarms[0].get("type"), "put")
        self.assertTrue(alarms[0].get("item"))
        self.assertEqual(alarms[0].get("item").get("alarmcode"), "WOB")
        self.assertEqual(alarms[0].get("item").get("display_ts"), "00:06:00")

    def test_WOB_Activate_StatusChange_To_Working_Pending(self):
        """
        Trigger alarm when agent sets a work status
        during an scheduled exception
        Display time is reset to 0
        """
        wob = WOB(self.SCHEDULE)
        events1 = self.create_event("STATE_CHANGE", "P0001",
                                    "2019-01-21T13:01:00.012Z",
                                    "Available")

        alarms = wob.process(events1, "P0001", {})
        self.assertEqual(len(alarms), 1)
        self.assertEqual(alarms[0].get("type"), "put")
        self.assertTrue(alarms[0].get("item"))
        self.assertEqual(alarms[0].get("item").get("alarmcode"), "WOB")
        self.assertEqual(alarms[0].get("item")
                                  .get("extra")
                                  .get("status"), "pending")
        self.assertEqual(alarms[0].get("item").get("display_ts"), "00:00:00")

    def test_WOB_Clear_StatusChange(self):
        """
        Clear alarm when agent has a non work status
        during an scheduled exception
        """
        wob = WOB(self.SCHEDULE)
        events1 = self.create_event("STATE_CHANGE", "P0001",
                                    "2019-01-21T13:16:00.012Z",
                                    "Lunch")

        extra = {
            "start": "2019-01-21T13:00"
        }
        alarms = wob.process(events1, "P0001", {"extra": extra})
        self.assertEqual(len(alarms), 1)
        self.assertEqual(alarms[0].get("type"), "delete")
        self.assertTrue(alarms[0].get("key"))
        self.assertEqual(alarms[0].get("key").get("alarmcode"), "WOB")

    def test_WOB_Activate_Pending(self):
        """
        Clear alarm when agent has a non work status
        during an scheduled exception
        """
        wob = WOB(self.SCHEDULE)
        events1 = self.create_event("SP_HEART_BEAT", "P0001",
                                    "2019-01-21T13:16:00.012Z",
                                    "Available")

        state = {
            "extra": {
                "start": "2019-01-21T13:10",
                "status": "pending"
            },
            "alarmcode": "WOB"
        }
        alarms = wob.process(events1, "P0001", state)
        self.assertEqual(len(alarms), 1)
        self.assertEqual(alarms[0].get("type"), "put")
        self.assertEqual(alarms[0].get("item").get("alarmcode"), "WOB")
        self.assertEqual(alarms[0].get("item").get("extra").get("status"), "active")

    def test_WOB_NoActivate_Pending(self):
        """
        Clear alarm when agent has a non work status
        during an scheduled exception
        """
        wob = WOB(self.SCHEDULE)
        events1 = self.create_event("SP_HEART_BEAT", "P0001",
                                    "2019-01-21T13:16:00.012Z",
                                    "Available")

        extra = {
            "start": "2019-01-21T13:12",
            "status": "pending"
        }
        alarms = wob.process(events1, "P0001", {"extra": extra})
        self.assertEqual(len(alarms), 1)

    # ------------------------------------------------
    # BBE tests
    # 12:30 < ts < 12:55

    def test_BBE_Activated(self):
        bbe = BBE(self.SCHEDULE)
        # 12:30 < ts < 12:55
        events1 = self.create_event("STATE_CHANGE", "P0001",
                                    "2019-01-21T12:40:00.012Z",
                                    "Lunch")

        alarms = bbe.process(events1, "P0001", {})
        self.assertEqual(len(alarms), 1)
        self.assertEqual(alarms[0].get("type"), "put")
        self.assertTrue(alarms[0].get("item"))
        self.assertEqual(alarms[0].get("item").get("alarmcode"), "BBE")

    # ------------------------------------------------
    # SIU tests

    def test_SIU_Activated_BeforeShift(self):
        # Shift start: 2019-01-21T08:00
        # Shift end: 2019-01-21T16:30
        # SIU < 2019-01-21T07:25
        siu = SIU(self.SCHEDULE)
        events1 = self.create_event("LOGIN", "P0001",
                                    "2019-01-21T07:00:00.012Z")

        alarms = siu.process(events1, "P0001", {})
        self.assertEqual(len(alarms), 1)
        self.assertEqual(alarms[0].get("type"), "put")
        self.assertTrue(alarms[0].get("item"))
        self.assertEqual(alarms[0].get("item").get("alarmcode"), "SIU")

    def test_SIU_Activated_AfterShift(self):
        # Shift start: 2019-01-21T08:00
        # Shift end: 2019-01-21T16:30
        # SIU > 2019-01-21T17:05
        siu = SIU(self.SCHEDULE)
        events1 = self.create_event("LOGIN", "P0001",
                                    "2019-01-21T17:06:00.012Z")

        alarms = siu.process(events1, "P0001", {})
        self.assertEqual(len(alarms), 1)
        self.assertEqual(alarms[0].get("type"), "put")
        self.assertTrue(alarms[0].get("item"))
        self.assertEqual(alarms[0].get("item").get("alarmcode"), "SIU")

    def test_SIU_Activated_IncrementTS(self):
        # Shift start: 2019-01-21T08:00
        # Shift end: 2019-01-21T16:30
        # SIU > 2019-01-21T17:05
        siu = SIU(self.SCHEDULE)
        events1 = self.create_event("SP_HEART_BEAT", "P0001",
                                    "2019-01-21T17:07:00.012Z")

        state = {
            "extra": {
                "login": "2019-01-21T17:06:00.012Z"
            },
            "alarmcode": "SIU"
        }
        alarms = siu.process(events1, "P0001", state)
        self.assertEqual(len(alarms), 1)
        self.assertEqual(alarms[0].get("type"), "put")
        self.assertEqual(alarms[0].get("item").get("alarmcode"), "SIU")
        self.assertEqual(alarms[0].get("item").get("display_ts"), "00:01:00")

    def test_SIU_Activated_NoSchedule(self):
        # username = P0002
        siu = SIU(self.SCHEDULE)
        events1 = self.create_event("LOGIN", "P0002",
                                    "2019-01-21T17:06:00.012Z")

        alarms = siu.process(events1, "P0002", {})
        self.assertEqual(len(alarms), 1)
        self.assertEqual(alarms[0].get("type"), "put")
        self.assertTrue(alarms[0].get("item"))
        self.assertEqual(alarms[0].get("item").get("alarmcode"), "SIU")

    # ------------------------------------------------
    # BXE tests
    # 12:45 < ts < 12:55

    def test_BXE_Activated(self):
        bbe = BXE(self.SCHEDULE)
        # 12:45 < ts < 12:55
        events1 = self.create_event("STATE_CHANGE", "P0001",
                                    "2019-01-21T12:48:00.012Z",
                                    "121")

        alarms = bbe.process(events1, "P0001", {})
        self.assertEqual(len(alarms), 1)
        self.assertEqual(alarms[0].get("type"), "put")
        self.assertTrue(alarms[0].get("item"))
        self.assertEqual(alarms[0].get("item").get("alarmcode"), "BXE")

    # ------------------------------------------------
    # EXL tests
    # 14:05 < ts < 14:15

    def test_EXL_Activated(self):
        exl = EXL(self.SCHEDULE)
        # 14:05 < ts < 14:15
        events1 = self.create_event("SP_HEART_BEAT", "P0001",
                                    "2019-01-21T14:10:00.012Z",
                                    "121")

        alarms = exl.process(events1, "P0001", {})
        self.assertEqual(len(alarms), 1)
        self.assertEqual(alarms[0].get("type"), "put")
        self.assertTrue(alarms[0].get("item"))
        self.assertEqual(alarms[0].get("item").get("alarmcode"), "EXL")

    def test_EXL_UpdateTS(self):
        exl = EXL(self.SCHEDULE)
        # 14:05 < ts < 14:15
        events1 = self.create_event("SP_HEART_BEAT", "P0001",
                                    "2019-01-21T14:12:00.012Z",
                                    "121")

        state = {
            "extra": {"end": "2019-01-21T14:00"},
            "alarmcode": "EXL"
        }
        alarms = exl.process(events1, "P0001", state)
        self.assertEqual(len(alarms), 1)
        self.assertEqual(alarms[0].get("type"), "put")
        self.assertTrue(alarms[0].get("item").get("display_ts"), "00:12:00")
        self.assertEqual(alarms[0].get("item").get("alarmcode"), "EXL")

    def test_EXL_UpdateTS2(self):
        exl = EXL(self.SCHEDULE)
        # 14:05 < ts < 14:15
        events1 = self.create_event("SP_HEART_BEAT", "P0001",
                                    "2019-01-21T14:13:00.012Z",
                                    "121")

        state = {
            "extra": {"end": "2019-01-21T14:00"},
            "alarmcode": "EXL"
        }
        alarms = exl.process(events1, "P0001", state)
        self.assertEqual(len(alarms), 1)
        self.assertEqual(alarms[0].get("type"), "put")
        self.assertTrue(alarms[0].get("item").get("display_ts"), "00:13:00")
        self.assertEqual(alarms[0].get("item").get("alarmcode"), "EXL")

    def test_BSE_Activated(self):
        bse = BSE(self.SCHEDULE)
        events1 = self.create_event("LOGIN", "P0001", 
                                    "2019-01-21T07:33:00.012Z")

        alarms = bse.process(events1, "P0001", {})
        self.assertEqual(len(alarms), 1)
        self.assertEqual(alarms[0].get("type"), "put")
        self.assertTrue(alarms[0].get("item"))
        self.assertEqual(alarms[0].get("item").get("alarmcode"), "BSE")

    def test_BSL_Activated(self):
        bsl = BSL(self.SCHEDULE)
        events1 = self.create_event("SP_HEART_BEAT", "P0001",
                                    "2019-01-21T08:06:00.012Z",
                                    "Offline")

        alarms = bsl.process(events1, "P0001", {}, {})
        self.assertEqual(len(alarms), 1)
        self.assertEqual(alarms[0].get("type"), "put")
        self.assertTrue(alarms[0].get("item"))
        self.assertEqual(alarms[0].get("item").get("alarmcode"), "BSL")

    def test_BSL_LateLogin(self):
        bsl = BSL(self.SCHEDULE)
        events1 = self.create_event("LOGIN", "P0001",
                                    "2019-01-21T08:07:00.012Z",
                                    "Offline")

        state = {
            "extra": {
                "start": "2019-01-21T08:00"
            },
            "alarmcode": "BSL"
        }
        alarms = bsl.process(events1, "P0001", state, {})
        self.assertEqual(len(alarms), 1)
        self.assertEqual(alarms[0].get("type"), "put")
        self.assertTrue(alarms[0].get("item"))
        self.assertEqual(alarms[0].get("item").get("alarmcode"), "BSL")

    def test_BSL_UpdateTS(self):
        bsl = BSL(self.SCHEDULE)
        events1 = self.create_event("SP_HEART_BEAT", "P0001",
                                    "2019-01-21T08:07:00.012Z",
                                    "Offline")

        state = {
            "extra": {
                "start": "2019-01-21T08:00"
            },
            "alarmcode": "BSL"
        }
        alarms = bsl.process(events1, "P0001", state, {})

        self.assertEqual(len(alarms), 1)
        self.assertEqual(alarms[0].get("type"), "put")
        self.assertTrue(alarms[0].get("item"))
        self.assertEqual(alarms[0].get("item").get("alarmcode"), "BSL")

    # ------------------------------------------------
    # EBL tests
    # break is 13:00 - 14:00
    # 14:05 < ts < 14:30

    def test_EBL_Activated(self):
        ebl = EBL(self.SCHEDULE)
        events1 = self.create_event("SP_HEART_BEAT", "P0001",
                                    "2019-01-21T14:06:00.012Z",
                                    "Lunch")

        alarms = ebl.process(events1, "P0001", {}, {})
        self.assertEqual(len(alarms), 1)
        self.assertEqual(alarms[0].get("type"), "put")
        self.assertTrue(alarms[0].get("item"))
        self.assertEqual(alarms[0].get("item").get("alarmcode"), "EBL")

    def test_EBL_UpdateTS(self):
        ebl = EBL(self.SCHEDULE)
        events1 = self.create_event("SP_HEART_BEAT", "P0001",
                                    "2019-01-21T14:07:00.012Z",
                                    "Lunch")

        state = {
            "extra": {
                "start": "2019-01-21T13:00",
                "end": "2019-01-21T14:00"
            },
            "alarmcode": "EBL"
        }
        alarms = ebl.process(events1, "P0001", state, {})

        self.assertEqual(len(alarms), 1)
        self.assertEqual(alarms[0].get("type"), "put")
        self.assertEqual(alarms[0].get("item").get("display_ts"), "00:07:00")
        self.assertEqual(alarms[0].get("item").get("alarmcode"), "EBL")

    def test_EBL_Clear(self):
        ebl = EBL(self.SCHEDULE)
        events1 = self.create_event("STATE_CHANGE", "P0001",
                                    "2019-01-21T14:08:00.012Z",
                                    "Available")

        state = {
            "extra": {
                "start": "2019-01-21T13:00",
                "end": "2019-01-21T14:00"
            }
        }
        alarms = ebl.process(events1, "P0001", state, {})
        self.assertEqual(len(alarms), 1)
        self.assertEqual(alarms[0].get("type"), "delete")
        self.assertTrue(alarms[0].get("key"))
        self.assertEqual(alarms[0].get("key").get("alarmcode"), "EBL")


if __name__ == '__main__':
    unittest.main()
