import json
from common.constants import MAX_PACKAGE_LENGTH, ENCODING

def get_message(client):

    encoded_response = client.recv(MAX_PACKAGE_LENGTH)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        raise Exception
    raise Exception

def send_message(socket, message):
    if isinstance(message, dict):
        js_message = json.dumps(message)
        encoded_message = js_message.encode(ENCODING)
        socket.send(encoded_message)
        return
    raise Exception