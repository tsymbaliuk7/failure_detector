from typing import Optional

from failure_detector.detector_report import DetectorReport
from failure_detector.failure_detector import FailureDetector
from failure_detector.interfaces.failure_detection_event_listener import IFailureDetectionEventListener
from failure_detector.interfaces.failure_detector import IFailureDetector
from gossiper.gossip_digest import GossipDigest
from gossiper.interfaces.endpoint_state_change_subscriber import EndPointStateChangeSubscriber
from network.enpoints.endpoint import Endpoint
from network.enpoints.endpoint_state import EndpointState, State
from gossiper.messages.gossip_sync_message import GossipSyncMessage
from network.enpoints.heartbeat_state import HeartBeatState
from network.message_sender_service import MessageSenderService
from network.messages.entities.message import Message
from util.logger import Logger
from util.singletone import Singleton
from util.endpoints_loader import EndpointsLoader
import threading
import random


class Gossiper(IFailureDetectionEventListener, metaclass=Singleton):
    interval = 1

    def __init__(self):
        self.local_endpoint = None
        self.end_point_state_map: dict[Endpoint, EndpointState] = {}
        self.subscribers: list[EndPointStateChangeSubscriber] = []
        self.gossip_timer = None
        self.live_endpoints: set[Endpoint] = set()
        self.unreachable_endpoints: set[Endpoint] = set()
        self.seeds: set[Endpoint] = set()

    @property
    def local_endpoint_state(self) -> EndpointState:
        return self.end_point_state_map[self.local_endpoint]

    def get_suspicious_ep_list(self) -> list[Endpoint]:
        sus_list = []
        for ep in self.live_endpoints:
            ep_state = self.end_point_state_map.get(ep)
            if ep_state:
                if ep_state.is_sus():
                    sus_list.append(ep)
        return sus_list

    def start(self, local_endpoint: Endpoint):
        # Set the local endpoint
        self.local_endpoint = local_endpoint
        self.seeds = EndpointsLoader().endpoints

        # Check if the local endpoint is not in the endpoint_states map
        if local_endpoint not in self.end_point_state_map.keys():
            # Initialize its state with the default value
            self.end_point_state_map[local_endpoint] = EndpointState(heartbeat_state=HeartBeatState())

        # Start periodic gossiping
        self.schedule_gossip()

    def schedule_gossip(self):
        # Schedule the run_gossip method to run every 'interval' seconds
        self.gossip_timer = threading.Timer(self.interval, self.run_gossip)
        self.gossip_timer.start()

    def run_gossip(self):
        Logger.info("Running gossip...")
        if self.local_endpoint:
            self.local_endpoint_state.heartbeat_state.update_heartbeat()

            gossip_digest = self.generate_random_gossip_digest()

            if len(gossip_digest) > 0:

                message = GossipSyncMessage(self.local_endpoint, gossip_digest, cluster_id=EndpointsLoader().cluster_id)

                result = self.do_gossip_to_live_member(message)

                self.do_gossip_to_unreachable_member(message)

                if not result:
                    self.do_gossip_to_seed(message)

                Logger.info("Performing status check...")

                self.status_check()

        # Schedule the next gossiping
        self.schedule_gossip()

    def create_gossip_sync_message(self):
        pass

    def do_gossip_to_seed(self, message: Message):
        seed_size = len(self.seeds)
        if seed_size > 0:
            if seed_size == 1 and list(self.seeds)[0] == self.local_endpoint:
                return

            if len(self.live_endpoints) == 0:
                self.send_gossip(message, list(self.seeds))
            else:
                probability = len(self.seeds) / (len(self.live_endpoints) + len(self.unreachable_endpoints))
                random_double = random.uniform(0, 1)
                if random_double <= probability:
                    self.send_gossip(message, list(self.seeds))

    def do_gossip_to_live_member(self, message: Message) -> bool:
        size = len(self.live_endpoints)
        if size == 0:
            return False

        suspicious_ep_list = self.get_suspicious_ep_list()

        if len(suspicious_ep_list) > 0:
            return self.send_gossip(message, suspicious_ep_list)
        else:
            return self.send_gossip(message, list(self.live_endpoints))

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
        if random_endpoint == self.local_endpoint:
            return False
        Logger.info(f"Selected random endpoint: {random_endpoint}")
        return MessageSenderService().send_message(random_endpoint, message)

    def generate_random_gossip_digest(self) -> list[GossipDigest]:
        gossip_digest_list = []

        ep_state = self.local_endpoint_state
        max_version = self.get_max_endpoint_state_version(ep_state)

        gossip_digest_list.append(GossipDigest(self.local_endpoint, max_version))

        endpoints = list(self.live_endpoints)

        random.shuffle(endpoints)

        for ep in endpoints:
            state = self.end_point_state_map[ep]
            if state:
                version = self.get_max_endpoint_state_version(ep_state)
                gossip_digest_list.append(GossipDigest(ep, version))
            else:
                gossip_digest_list.append(GossipDigest(ep, 0))

        return gossip_digest_list

    @staticmethod
    def get_max_endpoint_state_version(ep_state: EndpointState) -> int:
        versions: list[int] = [ep_state.heartbeat_state.version]
        for key, app_state in ep_state.application_states.items():
            versions.append(app_state.version)

        return max(versions)

    @staticmethod
    def notify_failure_detector(ep: Endpoint):
        fd: IFailureDetector = FailureDetector()
        fd.report(ep)

    def apply_state_locally(self, ep_state_map: dict[Endpoint, EndpointState]):
        endpoints = ep_state_map.keys()
        for ep in endpoints:
            if ep == self.local_endpoint:
                continue

            local_ep_state_ptr = self.end_point_state_map.get(ep)
            remote_state = ep_state_map.get(ep)

            if local_ep_state_ptr:
                remote_version = self.get_max_endpoint_state_version(remote_state)
                local_version = self.get_max_endpoint_state_version(local_ep_state_ptr)
                if remote_version > local_version:
                    # self.reanimate(ep, local_ep_state_ptr)
                    self.apply_heart_beat_state_locally(ep, local_ep_state_ptr, remote_state)
                    self.apply_application_state_locally(ep, local_ep_state_ptr, remote_state)

            else:
                self.handle_new_join(ep, remote_state)

    @staticmethod
    def apply_heart_beat_state_locally(ep: Endpoint, local_state: EndpointState, remote_state: EndpointState):
        local_hb_state = local_state.heartbeat_state
        remote_hb_state = remote_state.heartbeat_state

        if remote_hb_state.version > local_hb_state.version:
            old_version = local_hb_state.version
            local_state.update_heartbeat_state(remote_hb_state)
            Logger.info(
                f"Updating heartbeat state version to {local_state.heartbeat_state.version} from {old_version} for {ep}...")

    def apply_application_state_locally(self, ep: Endpoint, local_state: EndpointState, remote_state: EndpointState):
        local_app_state_map = local_state.application_states
        remote_app_state_map = remote_state.application_states

        for key in remote_app_state_map.keys():
            remote_app_state = remote_app_state_map.get(key)
            local_app_state = local_app_state_map.get(key)

            if not local_app_state:
                local_state.add_app_state(key, remote_app_state)
                delta_state = EndpointState(local_state.heartbeat_state)
                delta_state.add_app_state(key, remote_app_state)

                self.notify_subscribers(ep, delta_state)
                continue

            remote_version = remote_app_state.version
            local_version = local_app_state.version

            if remote_version > local_version:
                local_state.add_app_state(key, remote_app_state)
                delta_state = EndpointState(local_state.heartbeat_state)
                delta_state.add_app_state(key, remote_app_state)

                self.notify_subscribers(ep, delta_state)

    def handle_new_join(self, ep: Endpoint, ep_state: EndpointState):
        Logger.success(f"Node {ep} has now joined.")
        self.end_point_state_map[ep] = ep_state
        self.change_local_state(ep, ep_state, State.LIVE)
        self.notify_subscribers(ep, ep_state)

    def stop(self):
        # Stop the gossiping timer when you're done
        if self.gossip_timer:
            self.gossip_timer.cancel()

    def status_check(self):
        eps = list(self.end_point_state_map.keys())

        for endpoint in eps:
            if endpoint == self.local_endpoint:
                continue
            FailureDetector().interpret(endpoint)

    def convict(self, ep: Endpoint, detector_report: DetectorReport):
        ep_state: EndpointState = self.end_point_state_map[ep]

        if ep_state:
            if not ep_state.is_unreachable():
                Logger.error(f"Endpoint {ep} is dead")
                self.change_local_state(ep, ep_state, State.UNREACHABLE)
            self.notify_subscribers(ep, ep_state, detector_report)

    def suspect(self, ep: Endpoint, detector_report: DetectorReport):
        ep_state: EndpointState = self.end_point_state_map[ep]

        if ep_state:
            if not ep_state.is_sus():
                Logger.warning(f"Endpoint {ep} is suspicious")
                self.change_local_state(ep, ep_state, State.SUSPICIOUS)
            self.notify_subscribers(ep, ep_state, detector_report)

    def reanimate(self, ep: Endpoint, detector_report: DetectorReport):
        ep_state: EndpointState = self.end_point_state_map[ep]

        if ep_state:
            if not ep_state.is_live():
                Logger.success(f"Endpoint {ep} is live")
                self.change_local_state(ep, ep_state, State.LIVE)
            self.notify_subscribers(ep, ep_state, detector_report)

    def change_local_state(self, endpoint: Endpoint, ep_state: EndpointState, new_value: State):
        ep_state.update_state(new_value)

        if new_value == State.LIVE or new_value == State.SUSPICIOUS:
            self.live_endpoints.add(endpoint)
            try:
                self.unreachable_endpoints.remove(endpoint)
            except Exception as e:
                Logger.error(str(e))
        else:
            self.unreachable_endpoints.add(endpoint)
            try:
                self.live_endpoints.remove(endpoint)
            except Exception as e:
                Logger.error(str(e))

    '''
    This method is used to figure the state that the Gossiper has but Gossipee doesn't. The delta digests
    and the delta state are built up.
    '''

    def examine_gossiper(self, g_digest_list: list[GossipDigest], delta_gossip_digest_list: list[GossipDigest],
                         delta_ep_state_map: dict[Endpoint, EndpointState]):
        for g_digest in g_digest_list:
            max_remote_version = g_digest.max_version
            ep_state_ptr = self.end_point_state_map.get(g_digest.endpoint)
            if ep_state_ptr:
                max_local_version = self.get_max_endpoint_state_version(ep_state_ptr)
                if max_remote_version == max_local_version:
                    continue
                elif max_remote_version > max_local_version:
                    delta_gossip_digest_list.append(GossipDigest(g_digest.endpoint, max_version=max_local_version))
                else:
                    self.add_ep_state_for_sending(g_digest, delta_ep_state_map, max_remote_version=max_remote_version)

            else:
                self.add_digest_to_request(g_digest, delta_gossip_digest_list)

    @staticmethod
    def add_digest_to_request(g_digest: GossipDigest, delta_gossip_digest_list: list[GossipDigest]):
        delta_gossip_digest_list.append(GossipDigest(g_digest.endpoint, max_version=0))

    def add_ep_state_for_sending(self, g_digest: GossipDigest, delta_ep_state_map: dict[Endpoint, EndpointState],
                                 max_remote_version: int):
        local_ep_state = self.get_state_for_version_bigger_than(g_digest.endpoint, max_remote_version)
        if local_ep_state:
            delta_ep_state_map[g_digest.endpoint] = local_ep_state

    def get_state_for_version_bigger_than(self, for_ep: Endpoint, version: int) -> Optional[EndpointState]:
        ep_state = self.end_point_state_map[for_ep]
        req_ep_state: Optional[EndpointState] = None

        if ep_state:
            local_hb_version = ep_state.heartbeat_state.version
            if local_hb_version > version:
                req_ep_state = EndpointState(ep_state.heartbeat_state)

            app_state_map = ep_state.application_states

            for key, app_state in app_state_map.items():
                if app_state.version > version:
                    if req_ep_state is None:
                        req_ep_state = EndpointState(ep_state.heartbeat_state)
                    req_ep_state.add_app_state(key, app_state)

        return req_ep_state

    def set_local_endpoint(self, endpoint):
        self.local_endpoint = endpoint

    def add_subscriber(self, subscriber: EndPointStateChangeSubscriber):
        self.subscribers.append(subscriber)

    def remove_subscriber(self, subscriber: EndPointStateChangeSubscriber):
        self.subscribers.remove(subscriber)

    def select_random_endpoint(self):
        # Simulate selecting a random endpoint for gossip
        # In your implementation, you should choose a random endpoint from the available endpoints
        available_endpoints = list(self.end_point_state_map.keys())
        return random.choice(available_endpoints)

    def notify_subscribers(self, ep: Endpoint, ep_state: EndpointState,
                           detector_report: Optional[DetectorReport] = None):
        # Notify subscribers of state changes for a specific endpoint and state
        for subscriber in self.subscribers:
            subscriber.on_change(ep, ep_state, detector_report)
