from network.message_handlers.handler import Handler
from network.message import Message


class DefaultMessageHandler(Handler):
    def handle_message(self, message: Message):
        print(f"Incoming message {message.message_code} from {message.sender}")
        print(message.data)
