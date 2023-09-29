import json
from datetime import datetime
from enum import Enum

from util.version_generator import VersionGenerator


class State(Enum):
    UNKNOWN = "unknown"
    LIVE = "live"
    SUSPICIOUS = "suspicious"
    UNREACHABLE = "unreachable"


class EndpointState:
    def __init__(self, state=State.UNKNOWN, last_update_date=datetime.now(), version=0, heartbeat=0):
        self.state = state
        self.last_update_date = last_update_date
        self.version = version,
        self.heartbeat = heartbeat

    def to_json(self):
        """
        Convert the object to a JSON-formatted string.
        """
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    @classmethod
    def from_json(cls, json_str):
        """
        Create an object from a JSON-formatted string.
        """
        data = json.loads(json_str)
        return cls(**data)

    def update_state(self, new_state):
        """
        Update the state and last update date.
        """
        self.state = new_state
        self.last_update_date = datetime.now().isoformat()

    def update_heartbeat(self):
        self.version = VersionGenerator().next_version
        self.heartbeat += 1
