import socket
import threading
import time

from gossiper.interfaces.endpoint_state_change_subscriber import EndPointStateChangeSubscriber
from network.message import Message


class Server(EndPointStateChangeSubscriber):
    def on_change(self, endpoint, ep_state):
        pass

    def __init__(self, local_endpoint, endpoints):
        self.local_endpoint = local_endpoint
        self.address = f"{local_endpoint.host}:{local_endpoint.port}"
        self.connections = {}
        self.endpoints = endpoints
        self.server_socket = None

    def establish_connections(self):
        while True:
            for target_server in self.endpoints:
                if target_server != self.local_endpoint:
                    target_address = tuple(target_server)
                    if target_address not in self.connections:
                        try:
                            target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            target_socket.connect(target_address)
                            target_socket.settimeout(15)
                            self.connections[target_address] = target_socket
                            print(f"Connected to {target_server.host}:{target_server.port}")
                        except Exception as e:
                            print(
                                f"Error establishing connection to {target_server.host}:{target_server.port}: {str(e)}")

            time.sleep(5)

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(tuple(self.local_endpoint))
        self.server_socket.listen(5)
        print(f"Server {self.address} is listening on {self.local_endpoint.host}:{self.local_endpoint.port}")

        while True:
            client, addr = self.server_socket.accept()
            print(f"Accepted connection from {addr}")
            client_handler = threading.Thread(target=self.handle_client, args=(client,))
            client_handler.start()

    def handle_client(self, client_socket):
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            message = Message.from_json(data)
            print(f"Server {self.address} received message: {message.sender}: {message.data}")

    def send_message(self, target_address, message):
        try:
            target_socket = self.connections.get(target_address)
            if target_socket:
                target_message = message.to_json()
                target_socket.send(target_message.encode('utf-8'))
        except Exception as e:
            print(f"Error sending message: {str(e)}")

    # def message_sender(self):
    #     while True:
    #         for target_address, target_socket in self.connections.items():
    #             message = Message(self.address, "Hello from Server-" + self.address)
    #             self.send_message(target_address, message)
    #         time.sleep(5)

