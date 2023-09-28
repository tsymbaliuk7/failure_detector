from util.serializable import Serializable


class Endpoint(Serializable):

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def __eq__(self, other):
        return self.host == other.host and self.port == other.port

    def to_json(self):
        return {"host": self.host, "port": self.port}

    def __iter__(self):
        yield self.host
        yield self.port

    @classmethod
    def from_json(cls, json_data):
        return cls(json_data["host"], json_data["port"])

    def __str__(self):
        return f"{self.host}:{self.port}"
