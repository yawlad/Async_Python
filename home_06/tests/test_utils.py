import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'home_04')) 

import unittest
from datetime import datetime
import common.utils as utils
from common.constants import *
import json

class TestClientSimpleModel:
    
    def __init__(self, message):
        self.message = message
        self.sended_message = None

    def send(self, message):
        self.sended_message = message

    def recv(self, max_len):   
        return self.message
        


class TestClient(unittest.TestCase):
    def setUp(self):
        self.ok_message = {
            '1': '1',
            '2': '2',
            '3': '3'
        }
        self.bad_message_not_bytes = 'example'
        self.bad_message_not_dict = [1,2,3]
        
        self.ok_message_encoded = json.dumps(self.ok_message).encode(ENCODING)
        self.bad_message_not_dict_encoded = json.dumps(self.bad_message_not_dict).encode(ENCODING)
        
        self.ok_client = TestClientSimpleModel(self.ok_message_encoded)
        self.not_dict_client = TestClientSimpleModel(self.bad_message_not_bytes)
        self.not_bytes_client = TestClientSimpleModel(self.bad_message_not_dict_encoded)
        return super().setUp()

    def test_get_message_ok(self):
        result = utils.get_message(self.ok_client)
        self.assertEqual(result, self.ok_message)
    
    def test_get_message_exception_not_bytes_encoded_response(self):
        self.assertRaises(Exception, utils.get_message, self.not_bytes_client)
    
    def test_get_message_exception_not_dict_decoded_response(self):
        self.assertRaises(Exception, utils.get_message, self.not_dict_client)
    
    
    def test_send_message_ok(self):
        utils.send_message(self.ok_client, self.ok_message)
        self.assertEqual(self.ok_message_encoded, self.ok_client.sended_message)
    
    def test_send_message_not_dict(self):
        self.assertRaises(Exception, utils.send_message, self.ok_client, self.bad_message_not_dict)
    
if __name__ == '__main__':
    unittest.main()
