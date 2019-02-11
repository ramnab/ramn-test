import unittest
from unittest.mock import Mock, patch
import sys
import os

script_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, script_path + '/../code')
from lambda_handler import *

class BridgeTests(unittest.TestCase):
    #Test currently not useful, framework in place for later completion
    def placeholder_test(self):
          self.assertTrue(build_records_input("PLACEHOLDER"))
          
if __name__ == '__main__':
    unittest.main(buffer=True)
