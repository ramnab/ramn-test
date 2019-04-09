import unittest
import os
import sys

script_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, script_path + '/../code')
import verify.code.lambda_handler as la  # noqa


class VerifyTests(unittest.TestCase):

    def test_row_missing_start_moment(self):
        row = {}
        errors = la.verify_schedule_contents(row)
        self.assertEqual(len(errors), 3)


if __name__ == '__main__':
    unittest.main()
