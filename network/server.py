import socket
import threading
import time

from gossiper.interfaces.endpoint_state_change_subscriber import EndPointStateChangeSubscriber
from network.endpoint import Endpoint
from network.endpoint_state import EndpointState
from network.message import Message
from network.message_factory import message_factory
from network.message_handler_service import MessageHandlerService


class Server(EndPointStateChangeSubscriber):

    def __init__(self, local_endpoint: Endpoint, endpoints: list[Endpoint]):
        self.local_endpoint: Endpoint = local_endpoint
        self.connections: dict[Endpoint, socket] = dict()
        self.endpoints: list[Endpoint] = endpoints
        self.server_socket = None

        self.server_ep_state_info: dict[Endpoint, EndpointState] = {}

    def establish_connections(self):
        while True:
            for target_server in self.endpoints:
                if target_server != self.local_endpoint and target_server not in self.connections:
                    target_address_tuple = tuple(target_server)
                    try:
                        target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        target_socket.connect(target_address_tuple)
                        target_socket.settimeout(15)
                        self.connections[target_server] = target_socket
                        print(f"Connected to {target_server.host}:{target_server.port}")
                    except Exception as e:
                        print(
                            f"Error establishing connection to {target_server.host}:{target_server.port}: {str(e)}")

            time.sleep(5)

    def start(self):
        self.server_socket: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(tuple(self.local_endpoint))
        self.server_socket.listen(5)
        print(f"Server {self.local_endpoint} is listening on {self.local_endpoint.host}:{self.local_endpoint.port}")

        while True:
            client, addr = self.server_socket.accept()
            print(f"Accepted connection from {addr}")
            client_handler = threading.Thread(target=self.handle_client, args=(client,))
            client_handler.start()

    @staticmethod
    def handle_client(client_socket):
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            message = message_factory(data)
            MessageHandlerService().handle_message(message)

    def send_message(self, target_ep, message):
        try:
            ep_state = self.server_ep_state_info.get(target_ep)
            if ep_state:
                if ep_state.is_sus():
                    print("Warning! This endpoint is suspicious and message send might fail!")
                elif ep_state.is_sus():
                    print("Alert! This endpoint is unreachable!")
            target_socket = self.connections.get(target_ep)
            if target_socket:
                target_message = message.to_json()
                target_socket.send(target_message.encode('utf-8'))
        except Exception as e:
            print(f"Error sending message: {str(e)}")

    def stop(self):
        if self.server_socket:
            self.server_socket.close()

    # def message_sender(self):
    #     while True:
    #         for target_address, target_socket in self.connections.items():
    #             message = Message(self.address, "Hello from Server-" + self.address)
    #             self.send_message(target_address, message)
    #         time.sleep(5)

    def on_change(self, endpoint, ep_state):
        self.server_ep_state_info[endpoint] = ep_state
        if ep_state.is_unreachable():
            print(f"Endpoint {endpoint} is now unreachable")
            print("Closing connection socket...")
            try:
                connection = self.connections.pop(endpoint)
                if connection:
                    connection.close()
            except Exception as e:
                print(f"Such connection don't exist: {str(e)}")

        elif ep_state.is_sus():
            print(f"Endpoint {endpoint} is now suspicious")
        elif ep_state.is_live():
            print(f"Endpoint {endpoint} is now live")



