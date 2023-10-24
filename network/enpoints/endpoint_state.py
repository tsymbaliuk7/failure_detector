import json
from datetime import datetime
from enum import Enum

from network.enpoints.application_state import ApplicationState
from network.enpoints.heartbeat_state import HeartBeatState


class State(Enum):
    LIVE = "live"
    SUSPICIOUS = "suspicious"
    UNREACHABLE = "unreachable"

    @staticmethod
    def from_str(label: str):
        if label in ('LIVE', 'live'):
            return State.LIVE
        elif label in ('SUSPICIOUS', 'suspicious'):
            return State.SUSPICIOUS
        elif label in ('UNREACHABLE', 'unreachable'):
            return State.UNREACHABLE

        return State.LIVE


class EndpointState:
    def __init__(self, heartbeat_state: HeartBeatState, state=State.LIVE, last_update_date=datetime.now(),
                 application_states=None):
        if application_states is None:
            application_states = dict()
        self.state = state
        self.last_update_date: datetime = last_update_date
        self.heartbeat_state: HeartBeatState = heartbeat_state
        self.application_states: dict[str, ApplicationState] = application_states

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
        self.last_update_date = datetime.now()

    def add_app_state(self, key: str, app_state: ApplicationState):
        self.application_states[key] = app_state

    def to_json(self):
        return {
            "state": self.state.value,
            "last_update_date": self.last_update_date.timestamp(),
            "heartbeat_state": self.heartbeat_state.to_json(),
            "application_states": [[item[0], item[1].to_json()] for item in self.application_states.items()]
        }

    @classmethod
    def from_json(cls, json_data):
        if isinstance(json_data, str):
            data = json.loads(json_data)
        else:
            data = json_data

        temp_application_states = {item[0]: ApplicationState.from_json(item[1]) for item in data["application_states"]}

        return cls(
            heartbeat_state=HeartBeatState.from_json(data["heartbeat_state"]),
            state=State.from_str(data["state"]),
            last_update_date=datetime.fromtimestamp(data["last_update_date"]),
            application_states=temp_application_states
        )
