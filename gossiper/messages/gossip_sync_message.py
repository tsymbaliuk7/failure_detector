import json

from gossiper.gossip_digest import GossipDigest
from network.endpoint import Endpoint
from network.message_codes import MessageCodes
from network.message import Message


class GossipSyncMessage(Message):

    def __init__(self, sender: Endpoint, data, gossip_digests: list[GossipDigest]):
        super().__init__(sender, data, message_code=MessageCodes.GOSSIP_SYNC_CODE)
        self.gossip_digests = gossip_digests

    def to_json(self):
        data_dict = {
            "sender": self.sender.to_json(),
            "data": self.data,
            "message_code": self.message_code.value,
            "gossip_digests": list(map(lambda a: a.to_json(), self.gossip_digests))
        }
        return json.dumps(data_dict)

    @classmethod
    def from_json(cls, json_data):
        if json_data is str:
            data = json.loads(json_data)
        else:
            data = json_data
        return cls(Endpoint.from_json(data["sender"]), data["data"],
                   [GossipDigest.from_json(data) for data in data["gossip_digests"]])
