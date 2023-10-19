import json

from network.enpoints.endpoint import Endpoint
from network.enpoints.endpoint_state import EndpointState
from network.messages.message_codes import MessageCodes
from network.messages.entities.message import Message


class GossipAckConfirmMessage(Message):
    def __init__(self, sender: Endpoint, ep_state_map: dict[Endpoint, EndpointState]):
        super().__init__(sender, message_code=MessageCodes.GOSSIP_ACK_CONFIRM_CODE),
        self.ep_state_map: dict[Endpoint, EndpointState] = ep_state_map

    def to_json(self):

        ep_state_items = list(self.ep_state_map.items())

        data_dict = {
            "sender": self.sender.to_json(),
            "message_code": self.message_code.value,
            "ep_state_map": [[i.to_json() for i in item] for item in ep_state_items]
        }

        return json.dumps(data_dict)

    @classmethod
    def from_json(cls, json_data):
        if isinstance(json_data, str):
            data = json.loads(json_data)
        else:
            data = json_data

        temp_ep_state_map = {Endpoint.from_json(ep_item[0]): EndpointState.from_json(ep_item[1]) for ep_item in
                             data["ep_state_map"]}

        return cls(Endpoint.from_json(data["sender"]), temp_ep_state_map)
