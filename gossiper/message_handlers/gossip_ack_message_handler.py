from network.message_handlers.handler import Handler
from gossiper.messages.gossip_ack_message import GossipAckMessage


class GossipAckMessageHandler(Handler):
    def handle_message(self, message: GossipAckMessage):
        print(f"Incoming message {message.message_code} from {message.sender}")
        print(message.data)
