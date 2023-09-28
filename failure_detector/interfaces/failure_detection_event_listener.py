from abc import abstractmethod


class IFailureDetectionEventListener:
    """
    Interface for Failure Detection Event Listeners.
    """

    @abstractmethod
    def convict(self, ep):
        """
        Convict the specified endpoint.

        Args:
            ep: The endpoint to be convicted.
        """
        pass

    @abstractmethod
    def suspect(self, ep):
        """
        Suspect the specified endpoint.

        Args:
            ep: The endpoint to be suspected.
        """
        pass
