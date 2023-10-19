import socket
from typing import Optional

from failure_detector.detector_report import DetectorReport
from gossiper.interfaces.endpoint_state_change_subscriber import EndPointStateChangeSubscriber
from network.enpoints.endpoint import Endpoint
from network.enpoints.endpoint_state import EndpointState
from network.message_sender_interface import MessageSender
from network.messages.message_factory import message_factory
from network.messages.message_handler_service import MessageHandlerService
from network.messages.entities.message import Message
from util.singletone import Singleton


class Server(EndPointStateChangeSubscriber, MessageSender, metaclass=Singleton):

    def __init__(self, local_endpoint: Optional[Endpoint] = None):
        self.local_endpoint: Optional[Endpoint] = local_endpoint
        self.server_socket = None

        self.server_ep_state_info: dict[Endpoint, EndpointState] = {}
        self.server_ep_detector_reports: dict[Endpoint, DetectorReport] = {}

    def start(self):
        self.server_socket: socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        if self.local_endpoint:
            self.server_socket.bind(tuple(self.local_endpoint))

            while True:
                data, addr = self.server_socket.recvfrom(1024)
                print(f"Message from {addr}")

                if not data:
                    continue

                data = data.decode('utf-8')

                message = message_factory(data)
                MessageHandlerService().handle_message(message)

    def send_message(self, target_ep: Endpoint, message: Message):
        try:
            ep_state = self.server_ep_state_info.get(target_ep)
            if ep_state:
                if ep_state.is_sus():
                    print("Warning! This endpoint is suspicious and message send might fail!")
                elif ep_state.is_sus():
                    print("Alert! This endpoint is unreachable!")
            if self.server_socket:
                target_message = message.to_json()
                self.server_socket.sendto(target_message.encode('utf-8'), tuple(target_ep))
        except Exception as e:
            print(f"Error sending message: {str(e)}")

    def stop(self):
        if self.server_socket:
            self.server_socket.close()

    def on_change(self, endpoint, ep_state, detector_report: Optional[DetectorReport] = None):
        if detector_report:
            self.server_ep_detector_reports[endpoint] = detector_report
        self.server_ep_state_info[endpoint] = ep_state
        if ep_state.is_unreachable():
            print(f"Endpoint {endpoint} is now unreachable")

        elif ep_state.is_sus():
            print(f"Endpoint {endpoint} is now suspicious")
        elif ep_state.is_live():
            print(f"Endpoint {endpoint} is now live")
