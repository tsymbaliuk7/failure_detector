import json

from gossiper.gossip_digest import GossipDigest
from network.enpoints.endpoint import Endpoint
from network.messages.message_codes import MessageCodes
from network.messages.entities.message import Message


class GossipSyncMessage(Message):

    def __init__(self, sender: Endpoint, gossip_digests: list[GossipDigest], cluster_id: str):
        super().__init__(sender, message_code=MessageCodes.GOSSIP_SYNC_CODE)
        self.gossip_digests: list[GossipDigest] = gossip_digests
        self.cluster_id = cluster_id

    def to_json(self):
        data_dict = {
            "sender": self.sender.to_json(),
            "message_code": self.message_code.value,
            "cluster_id": self.cluster_id,
            "gossip_digests": list(map(lambda a: a.to_json(), self.gossip_digests))
        }
        return json.dumps(data_dict)

    @classmethod
    def from_json(cls, json_data):
        if isinstance(json_data, str):
            data = json.loads(json_data)
        else:
            data = json_data
        return cls(Endpoint.from_json(data["sender"]), [GossipDigest.from_json(data) for data in data["gossip_digests"]], cluster_id=data["cluster_id"])
