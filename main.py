import sys

from failure_detector.failure_detector import FailureDetector
from gossiper.gossiper import Gossiper
from network.message_sender_service import MessageSenderService
from network.messages.message_codes import MessageCodes
from gossiper.message_handlers.gossip_ack_confirm_message_handler import GossipAckConfirmMessageHandler
from gossiper.message_handlers.gossip_ack_message_handler import GossipAckMessageHandler
from gossiper.message_handlers.gossip_sync_message_handler import GossipSyncMessageHandler
from network.messages.message_handlers.info_request_message_handler import InfoRequestMessageHandler
from util.endpoints_loader import EndpointsLoader
from network.enpoints.endpoint import Endpoint
from network.messages.message_handler_service import MessageHandlerService
from network.messages.message_handlers.default_message_handler import DefaultMessageHandler
from network.server import Server


def start_server(server: Server):
    FailureDetector().register_failure_detection_event_listener(Gossiper())

    Gossiper().add_subscriber(server)

    message_handler_service = MessageHandlerService(default_handler=DefaultMessageHandler())
    message_handler_service.register_message_handler(MessageCodes.GOSSIP_SYNC_CODE, GossipSyncMessageHandler())
    message_handler_service.register_message_handler(MessageCodes.GOSSIP_ACK_CODE, GossipAckMessageHandler())
    message_handler_service.register_message_handler(MessageCodes.GOSSIP_ACK_CONFIRM_CODE,
                                                     GossipAckConfirmMessageHandler())

    message_handler_service.register_message_handler(MessageCodes.INFO_REQUEST, InfoRequestMessageHandler())

    message_sender_service = MessageSenderService()
    message_sender_service.set_message_sender(server)

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

        server = Server(Endpoint(host, port))
        start_server(server)
    except KeyboardInterrupt:
        if server:
            server.stop()
