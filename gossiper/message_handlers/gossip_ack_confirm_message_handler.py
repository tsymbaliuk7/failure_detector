from network.message_handlers.handler import Handler
from gossiper.messages.gossip_ack_confirm_message import GossipAckConfirmMessage


class GossipAckConfirmMessageHandler(Handler):
    def handle_message(self, message: GossipAckConfirmMessage):
        print(f"Incoming message {message.message_code} from {message.sender}")
        print(message.data)
