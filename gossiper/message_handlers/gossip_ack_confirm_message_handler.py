from gossiper.gossiper import Gossiper
from network.messages.message_handlers.handler import Handler
from gossiper.messages.gossip_ack_confirm_message import GossipAckConfirmMessage


class GossipAckConfirmMessageHandler(Handler):
    def handle_message(self, message: GossipAckConfirmMessage):
        print(f"Received a GossipDigestAckMessage from {message.sender}")

        remote_ep_state = message.ep_state_map

        Gossiper().notify_failure_detector(message.sender)
        Gossiper().apply_state_locally(remote_ep_state)

        print(f"Gossip cycle between {Gossiper().local_endpoint} and {message.sender} finished!")