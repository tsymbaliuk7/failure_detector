from abc import abstractmethod


class IFailureDetector:
    """
    Interface for a Failure Detector.
    """

    @abstractmethod
    def is_alive(self, ep):
        """
        Get the Failure Detector's knowledge of whether a node is up or down.

        Args:
            ep: The endpoint in question.

        Returns:
            bool: True if UP, False if DOWN.
        """
        pass

    @abstractmethod
    def interpret(self, ep):
        """
        Calculate Phi and deem an endpoint as suspicious or alive.

        Args:
            ep: The endpoint for which we interpret the interarrival times.
        """
        pass

    @abstractmethod
    def report(self, ep):
        """
        Report the receipt of a heartbeat and sample the arrival time.

        Args:
            ep: The endpoint being reported.
        """
        pass

    @abstractmethod
    def register_failure_detection_event_listener(self, listener):
        """
        Register interest for Failure Detector events.

        Args:
            listener: Implementation of an application provided IFailureDetectionEventListener.
        """
        pass

    @abstractmethod
    def unregister_failure_detection_event_listener(self, listener):
        """
        Unregister interest for Failure Detector events.

        Args:
            listener: Implementation of an application provided IFailureDetectionEventListener.
        """
        pass
