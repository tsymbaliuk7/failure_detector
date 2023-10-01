from abc import ABC, abstractmethod


class Serializable(ABC):
    @abstractmethod
    def to_json(self):
        pass

    @classmethod
    @abstractmethod
    def from_json(cls, json_data):
        pass
