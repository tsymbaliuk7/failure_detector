from gossiper.gossip_digest import GossipDigest
from gossiper.gossiper import Gossiper
from gossiper.messages.gossip_ack_message import GossipAckMessage
from network.endpoint import Endpoint
from network.endpoint_state import EndpointState
from network.message_handlers.handler import Handler
from gossiper.messages.gossip_sync_message import GossipSyncMessage
from util.endpoints_loader import EndpointsLoader


class GossipSyncMessageHandler(Handler):
    def handle_message(self, message: GossipSyncMessage):
        print(f"Incoming GossipSyncMessage {message.message_code} from {message.sender}")

        if not EndpointsLoader().cluster_id == message.cluster_id:
            return

        gossip_digest_list = message.gossip_digests

        Gossiper().notify_failure_detector(gossip_digest_list)

        self.do_sort(gossip_digest_list)

        delta_gossip_digest: list[GossipDigest] = []
        delta_ep_states_map: dict[Endpoint, EndpointState] = {}

        Gossiper().examine_gossiper(gossip_digest_list, delta_gossip_digest, delta_ep_states_map)

        Gossiper().send_message_from_gossiper(
            GossipAckMessage(Gossiper().local_endpoint, delta_gossip_digest, delta_ep_states_map), message.sender)

        print(f"Sending a GossipAckMessage to {message.sender}")

    @staticmethod
    def do_sort(g_digest_list):
        # Construct a map of endpoint to GossipDigest.
        ep_to_digest_map = {g_digest.endpoint: g_digest for g_digest in g_digest_list}

        # These digests have their max_version set to the difference of the version
        # of the local EndpointState and the version found in the GossipDigest.
        diff_digests = []
        for g_digest in g_digest_list:
            ep = g_digest.endpoint
            ep_state = Gossiper().end_point_state_map.get(ep)

            version = Gossiper.get_max_endpoint_state_version(ep_state) if ep_state else 0
            diff_version = abs(version - g_digest.max_version)
            diff_digests.append(GossipDigest(ep, diff_version))

        g_digest_list.clear()
        diff_digests.sort(key=lambda x: x.max_version)
        size = len(diff_digests)

        # Report the digests in descending order. This takes care of the endpoints
        # that are far behind w.r.t this local endpoint.
        for i in range(size - 1, -1, -1):
            g_digest_list.append(ep_to_digest_map[diff_digests[i].endpoint])
