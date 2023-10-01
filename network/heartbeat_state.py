from util.serializable import Serializable
from util.version_generator import VersionGenerator


class HeartBeatState(Serializable):

    def __init__(self, heartbeat=0, version=0):
        self.version: int = version,
        self.heartbeat: int = heartbeat

    def update_heartbeat(self):
        self.version = VersionGenerator().next_version
        self.heartbeat += 1

    def to_json(self):
        return {"version": self.version, "heartbeat": self.heartbeat}

    @classmethod
    def from_json(cls, data):
        return cls(version=data["version"], heartbeat=data["heartbeat"])
