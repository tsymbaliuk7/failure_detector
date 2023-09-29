from failure_detector.interfaces.failure_detection_event_listener import IFailureDetectionEventListener
from gossiper.gossip_digest import GossipDigest
from network.endpoint import Endpoint
from network.endpoint_state import EndpointState
from gossiper.messages.gossip_sync_message import GossipSyncMessage
from network.message import Message
from util.singletone import Singleton
from util.endpoints_loader import load_endpoints
import threading
import random


class Gossiper(IFailureDetectionEventListener, metaclass=Singleton):
    interval = 1

    def __init__(self):
        self.send_message = None
        self.local_endpoint = None
        self.end_point_state_map = {}  # Map<EndPoint, EndPointState>
        self.subscribers = []
        self.gossip_timer = None
        self.live_endpoints = []
        self.unreachable_endpoints = []
        self.seeds = []

    @property
    def local_endpoint_state(self) -> EndpointState:
        return self.end_point_state_map[self.local_endpoint]

    def start(self, local_endpoint):
        # Set the local endpoint
        self.local_endpoint = local_endpoint
        self.seeds = load_endpoints()

        # Check if the local endpoint is not in the endpoint_states map
        if local_endpoint not in self.end_point_state_map:
            # Initialize its state with the default value
            self.end_point_state_map[local_endpoint] = EndpointState()

        # Start periodic gossiping
        self.schedule_gossip()

    def schedule_gossip(self):
        # Schedule the run_gossip method to run every 'interval' seconds
        self.gossip_timer = threading.Timer(self.interval, self.run_gossip)
        self.gossip_timer.start()

    def run_gossip(self):
        print("Running gossip...")
        if self.local_endpoint:
            self.local_endpoint_state.update_heartbeat()
            message = GossipSyncMessage(self.local_endpoint, {'message': "hello"})

            result = self.do_gossip_to_live_member(message)

            self.do_gossip_to_unreachable_member(message)

            if not result:
                self.do_gossip_to_seed(message)

        # Schedule the next gossiping
        self.schedule_gossip()

    def do_gossip_to_seed(self, message: Message):
        seed_size = len(self.seeds)
        if seed_size > 0:
            if seed_size == 1 and self.seeds[0] == self.local_endpoint:
                return

            if len(self.live_endpoints) == 0:
                self.send_gossip(message, self.seeds)
            else:
                probability = len(self.seeds) / (len(self.live_endpoints) + len(self.unreachable_endpoints))
                random_double = random.uniform(0, 1)
                if random_double <= probability:
                    self.send_gossip(message, self.seeds)

    def do_gossip_to_live_member(self, message: Message) -> bool:
        size = len(self.live_endpoints)
        if size == 0:
            return False
        return self.send_gossip(message, self.live_endpoints)

    def do_gossip_to_unreachable_member(self, message: Message):
        live_endp_len = len(self.live_endpoints)
        unreachable_endp_len = len(self.unreachable_endpoints)
        if unreachable_endp_len > 0:
            probability = unreachable_endp_len / (live_endp_len + 1)
            random_double = random.uniform(0, 1)
            if random_double < probability:
                self.send_gossip(message, list(self.unreachable_endpoints))

    def send_gossip(self, message: Message, endpoints: list[Endpoint]) -> bool:
        random_endpoint = random.choice(list(endpoints))
        print(f"Selected random endpoint: {random_endpoint}")

        # Call the send_message method with the random endpoint
        if callable(self.send_message):
            self.send_message(tuple(random_endpoint), message)
            return random_endpoint in self.seeds
        else:
            print("send_message method not set.")
            return False

    def generate_random_gossip_digest(self) -> list[GossipDigest]:
        gossip_digest_list = []

        ep_state = self.local_endpoint_state
        local_version = ep_state.version

        gossip_digest_list.append(GossipDigest(self.local_endpoint, local_version))

        return gossip_digest_list

    def stop(self):
        # Stop the gossiping timer when you're done
        if self.gossip_timer:
            self.gossip_timer.cancel()

    def convict(self, ep):
        pass

    def suspect(self, ep):
        pass

    def set_local_endpoint(self, endpoint):
        self.local_endpoint = endpoint

    def set_send_message(self, send_message_method):
        self.send_message = send_message_method

    def add_subscriber(self, subscriber):
        self.subscribers.append(subscriber)

    def remove_subscriber(self, subscriber):
        self.subscribers.remove(subscriber)

    def select_random_endpoint(self):
        # Simulate selecting a random endpoint for gossip
        # In your implementation, you should choose a random endpoint from the available endpoints
        available_endpoints = list(self.end_point_state_map.keys())
        return random.choice(available_endpoints)

    def notify_subscribers(self, addr, ep_state):
        # Notify subscribers of state changes for a specific endpoint and state
        for subscriber in self.subscribers:
            subscriber.on_change(addr, ep_state)
