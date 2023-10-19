from abc import abstractmethod
from typing import Optional

from failure_detector.detector_report import DetectorReport
from network.enpoints.endpoint import Endpoint
from network.enpoints.endpoint_state import EndpointState


class EndPointStateChangeSubscriber:

    @abstractmethod
    def on_change(self, endpoint: Endpoint, ep_state: EndpointState, detector_report: Optional[DetectorReport] = None):
        pass
