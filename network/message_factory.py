import json

from gossiper.messages.gossip_ack_confirm_message import GossipAckConfirmMessage
from gossiper.messages.gossip_ack_message import GossipAckMessage
from gossiper.messages.gossip_sync_message import GossipSyncMessage
from network.message import Message
from network.message_codes import MessageCodes


def message_factory(json_data) -> Message:
    if isinstance(json_data, str):
        data = json.loads(json_data)
    else:
        data = json_data

    message_code = MessageCodes.from_str(data["message_code"])

    print(message_code)

    if message_code == MessageCodes.GOSSIP_SYNC_CODE:
        return GossipSyncMessage.from_json(data)

    elif message_code == MessageCodes.GOSSIP_ACK_CODE:
        return GossipAckMessage.from_json(data)
    elif message_code == MessageCodes.GOSSIP_ACK_CONFIRM_CODE:
        return GossipAckConfirmMessage.from_json(data)
    else:
        return Message.from_json(data)
