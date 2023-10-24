from network.message_sender_service import MessageSenderService
from network.messages.entities.info_response_message import InfoResponseMessage
from network.messages.message_handlers.handler import Handler
from network.messages.entities.message import Message
from network.server import Server
from util.logger import Logger


class InfoRequestMessageHandler(Handler):
    def handle_message(self, message: Message):
        Logger.info(f"Incoming message {message.message_code} from {message.sender}")

        local_endpoint = Server().local_endpoint
        ep_state_map = Server().server_ep_state_info
        detector_reports = Server().server_ep_detector_reports

        Logger.info(f"Sending a InfoResponseMessage to {message.sender}")
        MessageSenderService().send_message(message.sender, InfoResponseMessage(local_endpoint, ep_state_map, detector_reports))
