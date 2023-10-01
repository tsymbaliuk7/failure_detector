import json

from network.endpoint import Endpoint
from util.serializable import Serializable


class GossipDigest(Serializable):

    def __init__(self, endpoint: Endpoint, max_version):
        self.endpoint = endpoint
        self.max_version = max_version

    def to_json(self):
        data_dict = {"endpoint": self.endpoint.to_json(), "max_version": self.max_version}
        return json.dumps(data_dict)

    @classmethod
    def from_json(cls, json_data):
        data = json.loads(json_data)
        return cls(Endpoint.from_json(data["endpoint"]), max_version=data["max_version"])
