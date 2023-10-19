import json

from failure_detector.detector_report import DetectorReport
from network.enpoints.endpoint import Endpoint
from network.enpoints.endpoint_state import EndpointState
from network.messages.message_codes import MessageCodes
from network.messages.entities.message import Message


class InfoResponseMessage(Message):
    def __init__(self, sender: Endpoint, ep_state_map: dict[Endpoint, EndpointState], ep_detector_report_map: dict[Endpoint, DetectorReport]):
        super().__init__(sender, message_code=MessageCodes.INFO_RESPONSE),
        self.ep_state_map: dict[Endpoint, EndpointState] = ep_state_map
        self.ep_detector_report_map: dict[Endpoint, DetectorReport] = ep_detector_report_map

    def to_json(self):

        ep_state_items = list(self.ep_state_map.items())

        ep_state_list = []

        for ep, ep_state in ep_state_items:

            dr = self.ep_detector_report_map.get(ep)

            ep_state_list.append([ep.to_json(), ep_state.to_json(), dr.to_json() if dr else None])

        data_dict = {
            "sender": self.sender.to_json(),
            "message_code": self.message_code.value,
            "ep_state": ep_state_list
        }

        return json.dumps(data_dict)
