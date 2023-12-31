from network.messages.message_codes import MessageCodes
from network.messages.message_handlers.handler import Handler
from network.messages.entities.message import Message
from util.singletone import Singleton


class MessageHandlerService(metaclass=Singleton):

    def __init__(self, default_handler: Handler = None):
        self.default_handler = default_handler
        self.handlers_dict: dict[MessageCodes, Handler] = {}

    def handle_message(self, message: Message):
        if message.message_code in list(self.handlers_dict.keys()):
            self.handlers_dict[message.message_code].handle_message(message)
        else:
            self.default_handler.handle_message(message)

    def register_message_handler(self, code: MessageCodes, handler: Handler):
        self.handlers_dict[code] = handler

    def remove_message_handler(self, code):
        if code in list(self.handlers_dict.keys()):
            self.handlers_dict.pop(code)
