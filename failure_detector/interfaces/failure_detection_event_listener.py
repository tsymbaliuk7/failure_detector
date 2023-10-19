from abc import abstractmethod

from failure_detector.detector_report import DetectorReport
from network.enpoints.endpoint import Endpoint


class IFailureDetectionEventListener:
    """
    Interface for Failure Detection Event Listeners.
    """

    @abstractmethod
    def convict(self, ep: Endpoint, detector_report: DetectorReport):
        """
        Convict the specified endpoint.

        Args:
            :param ep: The endpoint to be convicted.
            :param detector_report: Failure detector output summary
        """
        pass

    @abstractmethod
    def suspect(self, ep: Endpoint, detector_report: DetectorReport):
        """
        Suspect the specified endpoint.

        Args:
            :param ep: The endpoint to be suspected.
            :param detector_report: Failure detector output summary
        """
        pass

    @abstractmethod
    def reanimate(self, ep: Endpoint, detector_report: DetectorReport):
        """
        Reanimate the specified endpoint.

        Args:
            :param ep: The endpoint to be reanimated.
            :param detector_report: Failure detector output summary
        """
        pass
