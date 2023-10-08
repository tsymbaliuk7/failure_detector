import sys
import threading

from gossiper.gossiper import Gossiper
from network.message_codes import MessageCodes
from gossiper.message_handlers.gossip_ack_confirm_message_handler import GossipAckConfirmMessageHandler
from gossiper.message_handlers.gossip_ack_message_handler import GossipAckMessageHandler
from gossiper.message_handlers.gossip_sync_message_handler import GossipSyncMessageHandler
from util.endpoints_loader import EndpointsLoader
from network.endpoint import Endpoint
from network.message_handler_service import MessageHandlerService
from network.message_handlers.default_message_handler import DefaultMessageHandler
from network.server import Server


def start_server(server):
    Gossiper().set_send_message(server.send_message)

    message_handler_service = MessageHandlerService(default_handler=DefaultMessageHandler())
    message_handler_service.register_message_handler(MessageCodes.GOSSIP_SYNC_CODE, GossipSyncMessageHandler())
    message_handler_service.register_message_handler(MessageCodes.GOSSIP_ACK_CODE, GossipAckMessageHandler())
    message_handler_service.register_message_handler(MessageCodes.GOSSIP_ACK_CONFIRM_CODE,
                                                     GossipAckConfirmMessageHandler())

    connection_thread = threading.Thread(target=server.establish_connections)
    connection_thread.start()

    Gossiper().start(server.local_endpoint)

    server.start()


if __name__ == "__main__":
    server = None
    try:
        if len(sys.argv) != 3:
            print("Usage: python main.py <host> <port>")
            sys.exit(1)

        host = sys.argv[1]
        port = int(sys.argv[2])

        endpoints = EndpointsLoader().endpoints

        server = Server(Endpoint(host, port), endpoints)
        start_server(server)
    except KeyboardInterrupt:
        print("AAAAA")
        if server:
            server.stop()
