from network.endpoint import Endpoint
from network.message_codes import MessageCodes
from network.messages.message import Message


class GossipAckMessage(Message):
    def __init__(self, sender: Endpoint, data):
        super().__init__(sender, data, message_code=MessageCodes.GOSSIP_ACK_CODE)
