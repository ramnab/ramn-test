import unittest
import api.code.lambda_handler as api
import json


class APITestCases(unittest.TestCase):
    def test_filter_no_client_wildcard(self):
        """
        API request specifies:
            no client;
            user has wildcard permissions
        """
        with open('event_all_clients_wildcard.json', 'r') as f:
            event = json.loads(f.read())
            filtered = api.get_requested_filtered(event)['filtered']
            self.assertEqual(len(filtered), 1)
            self.assertIn("*", filtered)

    def test_filter_client_wildcard(self):
        """
        API request specifies:
            client;
            user has wildcard permissions
        """
        with open('event_client_wildcard.json', 'r') as f:
            event = json.loads(f.read())
            filtered = api.get_requested_filtered(event)['filtered']
            self.assertEqual(len(filtered), 1)
            self.assertIn("tradeuk", filtered)

    def test_filter_client_matched_permission(self):
        """
        API request specifies:
            client;
            user has permissions for client
        """
        with open('event_client_matched_permission.json', 'r') as f:
            event = json.loads(f.read())
            filtered = api.get_requested_filtered(event)['filtered']
            self.assertEqual(len(filtered), 1)
            self.assertIn("tradeuk", filtered)

    def test_filter_client_no_permission(self):
        """
        API request specifies:
            client;
            user does not have permissions for client
        """
        with open('event_client_no_matched_permission.json', 'r') as f:
            event = json.loads(f.read())
            self.assertRaises(Exception, api.get_requested_filtered, event)

    def test_filter_no_client_permission(self):
        """
        API request specifies:
            no client;
            user has permissions for client 'tradeuk'
        """
        with open('event_no_client_permission.json', 'r') as f:
            event = json.loads(f.read())
            filtered = api.get_requested_filtered(event)['filtered']
            self.assertEqual(len(filtered), 1)
            self.assertIn("tradeuk", filtered)


if __name__ == '__main__':
    unittest.main()
