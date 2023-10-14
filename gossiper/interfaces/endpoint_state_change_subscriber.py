from abc import abstractmethod

from network.endpoint import Endpoint
from network.endpoint_state import EndpointState


class EndPointStateChangeSubscriber:

    @abstractmethod
    def on_change(self, endpoint: Endpoint, ep_state: EndpointState):
        pass
