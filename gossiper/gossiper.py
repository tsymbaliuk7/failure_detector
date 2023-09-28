import random

from failure_detector.interfaces.failure_detection_event_listener import IFailureDetectionEventListener
from network.endpoint_state import EndpointState
from network.messages.message import Message
from util.singletone import Singleton
from util.endpoints_loader import load_endpoints
import threading


class Gossiper(IFailureDetectionEventListener, metaclass=Singleton):
    interval = 1

    def __init__(self):
        self.send_message = None
        self.local_endpoint = None
        self.end_point_state_map = {}  # Map<EndPoint, EndPointState>
        self.subscribers = []
        self.gossip_timer = None
        self.seeds = []

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
        # Implement your gossiping logic here
        # This method will be called periodically based on the interval
        print("Running gossip...")
        if self.local_endpoint:
            random_endpoint = random.choice(list(self.end_point_state_map.keys()))
            print(f"Selected random endpoint: {random_endpoint}")

            # Call the send_message method with the random endpoint
            if callable(self.send_message):
                self.send_message(tuple(random_endpoint), Message(self.local_endpoint, {'message': "hello"}))
            else:
                print("send_message method not set.")

        # Schedule the next gossiping
        self.schedule_gossip()

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
