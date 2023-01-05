import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'home_04'))

from common.constants import *
import server
from datetime import datetime
import unittest



class TestServer(unittest.TestCase):

    def setUp(self):
        self.account_name = 'Guest'
        self.time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.responce_200 = {
            RESPONSE: 200,
            ALERT: 'Connected'
        }
        self.responce_400 = {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        }
        
        self.request_200 = {
            ACTION: PRESENCE,
            TIME: self.time,
            TYPE: STATUS,
            USER: {
                ACCOUNT_NAME: self.account_name,
                STATUS: HERE
            }
        }
        self.request_400_no_action = {
            TIME: self.time,
            TYPE: STATUS,
            USER: {
                ACCOUNT_NAME: self.account_name,
                STATUS: HERE
            }
        }
        self.request_400_unknown_action = {
            ACTION: 'Unknown',
            TIME: self.time,
            TYPE: STATUS,
            USER: {
                ACCOUNT_NAME: self.account_name,
                STATUS: HERE
            }
        }
        self.request_400_no_time = {
            ACTION: PRESENCE,
            TYPE: STATUS,
            USER: {
                ACCOUNT_NAME: self.account_name,
                STATUS: HERE
            }
        }
        self.request_400_no_user = {
            ACTION: PRESENCE,
            TIME: self.time,
            TYPE: STATUS,
        }
        self.request_400_no_account_name = {
            ACTION: PRESENCE,
            TIME: self.time,
            TYPE: STATUS,
            USER: {
                STATUS: HERE
            }
        }
        self.request_400_no_guest_user = {
            ACTION: PRESENCE,
            TIME: self.time,
            TYPE: STATUS,
            USER: {
                ACCOUNT_NAME: 'User',
                STATUS: HERE
            }
        }
        
        return super().setUp()

    def test_process_client_request_200(self):
        response = server.process_client_request(self.request_200)
        self.assertEqual(response, self.responce_200)

    def test_process_client_request_400_no_action(self):
        response = server.process_client_request(self.request_400_no_action)
        self.assertEqual(response, self.responce_400)
        
    def test_process_client_request_400_unknown_action(self):
        response = server.process_client_request(self.request_400_unknown_action)
        self.assertEqual(response, self.responce_400)

    def test_process_client_request_400_no_time(self):
        response = server.process_client_request(self.request_400_no_time)
        self.assertEqual(response, self.responce_400)

    def test_process_client_request_400_no_user(self):
        response = server.process_client_request(self.request_400_no_user)
        self.assertEqual(response, self.responce_400)

    def test_process_client_request_400_no_account_name(self):
        response = server.process_client_request(self.request_400_no_account_name)
        self.assertEqual(response, self.responce_400)
    
    def test_process_client_request_400_no_guest_user(self):
        response = server.process_client_request(self.request_400_no_guest_user)
        self.assertEqual(response, self.responce_400)

if __name__ == '__main__':
    unittest.main()
