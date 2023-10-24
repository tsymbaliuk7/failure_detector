from network.messages.message_handlers.handler import Handler
from network.messages.entities.message import Message
from util.logger import Logger


class DefaultMessageHandler(Handler):
    def handle_message(self, message: Message):
        Logger.info(f"Incoming message {message.message_code} from {message.sender}")
