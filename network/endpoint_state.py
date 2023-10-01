import json
from datetime import datetime
from enum import Enum

from network.application_state import ApplicationState
from network.heartbeat_state import HeartBeatState


class State(Enum):
    LIVE = "live"
    SUSPICIOUS = "suspicious"
    UNREACHABLE = "unreachable"


class EndpointState:
    def __init__(self, heartbeat_state: HeartBeatState, state=State.LIVE, last_update_date=datetime.now()):
        self.state = state
        self.last_update_date = last_update_date
        self.heartbeat_state: HeartBeatState = heartbeat_state
        self.application_states: dict[str, ApplicationState] = dict()

    def is_live(self) -> bool:
        return self.state == State.LIVE

    def is_sus(self) -> bool:
        return self.state == State.SUSPICIOUS

    def is_unreachable(self) -> bool:
        return self.state == State.UNREACHABLE

    def update_state(self, new_state: State):
        """
        Update the state and last update date.
        """
        self.state = new_state

    def update_heartbeat_state(self, hb_state: HeartBeatState):
        self.heartbeat_state = hb_state
        self.last_update_date = datetime.now().isoformat()

    def add_app_state(self, key: str, app_state: ApplicationState):
        self.application_states[key] = app_state

    def to_json(self):
        """
        Convert the object to a JSON-formatted string.
        """
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    @classmethod
    def from_json(cls, json_data):
        """
        Create an object from a JSON-formatted string.
        """
        data = json.loads(json_data)
        return cls(**data)
