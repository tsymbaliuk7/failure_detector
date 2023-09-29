from abc import abstractmethod

from network.message import Message


class Handler:

    @abstractmethod
    def handle_message(self, message: Message):
        pass
