from network.enpoints.endpoint import Endpoint
from network.messages.entities.message import Message
from abc import abstractmethod


class MessageSender:
    @abstractmethod
    def send_message(self, target_ep: Endpoint, message: Message):
        pass
