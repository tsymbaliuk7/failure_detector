from network.message_handlers.handler import Handler
from gossiper.messages.gossip_sync_message import GossipSyncMessage


class GossipSyncMessageHandler(Handler):
    def handle_message(self, message: GossipSyncMessage):
        print(f"Incoming GossipSyncMessage {message.message_code} from {message.sender}")
        print(message.data)

        print(f"Sending a GossipAckMessage to {message.sender}")
