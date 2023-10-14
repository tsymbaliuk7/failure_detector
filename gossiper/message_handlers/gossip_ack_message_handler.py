from gossiper.gossiper import Gossiper
from gossiper.messages.gossip_ack_confirm_message import GossipAckConfirmMessage
from network.message_handlers.handler import Handler
from gossiper.messages.gossip_ack_message import GossipAckMessage


class GossipAckMessageHandler(Handler):
    def handle_message(self, message: GossipAckMessage):
        print(f"Received a GossipDigestAckMessage from {message.sender}")

        g_digest_list = message.gossip_digests
        ep_state_map = message.ep_state_map

        if len(ep_state_map.keys()) > 0:
            Gossiper().notify_failure_detector_about_ep_state(ep_state_map)
            Gossiper().apply_state_locally(ep_state_map)

        delta_ep_state_map = dict()

        for g_digest in g_digest_list:
            ep = g_digest.endpoint
            local_ep_state = Gossiper().get_state_for_version_bigger_than(ep, g_digest.max_version)
            if local_ep_state:
                delta_ep_state_map[ep] = local_ep_state

        gossip_ack_confirm_message = GossipAckConfirmMessage(Gossiper().local_endpoint, delta_ep_state_map)

        print(f"Sending a GossipAckConfirmMessage to {message.sender}")

        Gossiper().send_message_from_gossiper(message=gossip_ack_confirm_message, to=message.sender)
