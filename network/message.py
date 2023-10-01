import json

from network.endpoint import Endpoint
from network.message_codes import MessageCodes
from util.serializable import Serializable


class Message(Serializable):
    def __init__(self, sender: Endpoint, data, message_code=MessageCodes.UNKNOWN):
        self.sender = sender
        self.data = data
        self.message_code = message_code

    def to_json(self):
        data_dict = {"sender": self.sender.to_json(), "data": self.data, "message_code": self.message_code.value}
        return json.dumps(data_dict)

    @classmethod
    def from_json(cls, json_data):
        if json_data is str:
            data = json.loads(json_data)
        else:
            data = json_data
        return cls(Endpoint.from_json(data["sender"]), data["data"], message_code=MessageCodes.from_str(data["message_code"]))
