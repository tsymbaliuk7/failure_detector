from network.message_handlers.handler import Handler
from network.messages.gossip_sync_message import GossipSyncMessage


class GossipSyncMessageHandler(Handler):
    def handle_message(self, message: GossipSyncMessage):
        print(f"Incoming message {message.message_code} from {message.sender}")
        print(message.data)
