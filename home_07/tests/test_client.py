import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'home_04')) 

import unittest
from datetime import datetime
import client
from common.constants import *




class TestClient(unittest.TestCase):
    
    def setUp(self):
        self.account_name = 'ExampleName'
        self.time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        self.response_200 = {
                    RESPONSE: 200,
                    ALERT: 'Connected'
                    }
        self.response_400 = {
                    RESPONSE: 400,
                    ERROR: 'Bad Request'
                    }
        self.response_exception = {}
        
        self.processed_response_200 = f'Response code: {self.response_200[RESPONSE]}\nAlert: {self.response_200[ALERT]}'
        self.processed_response_400 = f'Response code: {self.response_400[RESPONSE]}\nError: {self.response_400[ERROR]}'
        
        
        return super().setUp()
    
    def test_make_presense_without_name(self):
        request = client.make_presense()
        request[TIME] = self.time
        self.assertEqual(request, {ACTION: PRESENCE,
                                    TIME: self.time,
                                    TYPE: STATUS,
                                    USER: {
                                        ACCOUNT_NAME: 'Guest',
                                        STATUS: HERE
                                    }})
    
    def test_make_presense_with_name(self):
        request = client.make_presense(self.account_name)
        request[TIME] = self.time
        self.assertEqual(request, {ACTION: PRESENCE,
                                    TIME: self.time,
                                    TYPE: STATUS,
                                    USER: {
                                        ACCOUNT_NAME: self.account_name,
                                        STATUS: HERE
                                    }})
    
    def test_process_ans_200(self):
        responce_200 = client.process_ans(self.response_200)
        self.assertEqual(responce_200, self.processed_response_200)
    
    def test_process_ans_400(self):
        responce_400 = client.process_ans(self.response_400)
        self.assertEqual(responce_400, self.processed_response_400)
        
    def test_process_ans_exception(self):
        self.assertRaises(Exception, client.process_ans, (self.response_exception,) )
        
if __name__ == '__main__':
    unittest.main()