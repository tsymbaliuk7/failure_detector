import json

from util.serializable import Serializable


class Endpoint(Serializable):

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def __eq__(self, other):
        return self.host == other.host and self.port == other.port

    def __hash__(self):
        return hash((self.port, self.host))

    def __dict__(self):
        return {"host": self.host, "port": self.port}

    def to_json(self):
        return self.__dict__()

    def __iter__(self):
        yield self.host
        yield self.port

    @classmethod
    def from_json(cls, json_data):
        if isinstance(json_data, str):
            data = json.loads(json_data)
        else:
            data = json_data
        return cls(data["host"], data["port"])

    def __str__(self):
        return f"{self.host}:{self.port}"
