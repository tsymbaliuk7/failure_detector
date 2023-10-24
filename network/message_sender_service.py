from typing import Optional

from network.enpoints.endpoint import Endpoint
from network.message_sender_interface import MessageSender
from network.messages.entities.message import Message
from util.logger import Logger
from util.singletone import Singleton


class MessageSenderService(metaclass=Singleton):

    def __init__(self):
        self.message_sender: Optional[MessageSender] = None

    def set_message_sender(self, message_sender: MessageSender):
        self.message_sender = message_sender

    def send_message(self, target_ep: Endpoint, message: Message) -> bool:
        if self.message_sender:
            self.message_sender.send_message(target_ep, message)
            return True
        else:
            Logger.warning("message_sender not set in MessageSenderService.")
            return False
