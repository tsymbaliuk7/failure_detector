from util.serializable import Serializable
from util.version_generator import VersionGenerator


class ApplicationState(Serializable):
    def __init__(self, value, version=None):
        self.value = value
        self.version: int = version if version else VersionGenerator().next_version

    def to_json(self):
        return {"value": self.value, "version": self.version}

    @classmethod
    def from_json(cls, data):
        return cls(value=data["value"], version=data["version"])
