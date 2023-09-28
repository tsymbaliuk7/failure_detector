from abc import abstractmethod

from network.messages.message import Message


class Handler:

    @abstractmethod
    def handle_message(self, message: Message):
        pass