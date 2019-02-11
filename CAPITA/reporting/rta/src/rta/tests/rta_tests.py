import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from datetime import timedelta
import os
import sys
import base64


script_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, script_path + '/../code')
from lambda_handler import *


class RtaLambdaTests(unittest.TestCase):

    def create_kinesis_record(self, event):
        return {
            "kinesis": {
                "data": str(base64.encodebytes(json.dumps(event).encode('utf-8')))
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

    def test_recalc_Pass(self):
        os.environ["SCHEDULE"] = "s3://bucket/key"
        os.environ["ALARMDB"] = "rta-alarmsdb-ccm-dev"
        events1 = self.create_event("LOGIN", "P0001", 
                                    "2019-01-21T07:33:00.012Z")
        event = {
            "Records": [
                self.create_kinesis_record(events1[0])
            ]
        }
        handler(event, None)


if __name__ == '__main__':
    unittest.main()
