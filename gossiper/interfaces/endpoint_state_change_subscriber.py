from abc import abstractmethod


class EndPointStateChangeSubscriber:

    @abstractmethod
    def on_change(self, endpoint, ep_state):
        pass
