import datetime

from failure_detector.arrival_window import ArrivalWindow
from failure_detector.interfaces.failure_detection_event_listener import IFailureDetectionEventListener
from failure_detector.interfaces.failure_detector import IFailureDetector

from network.enpoints.endpoint import Endpoint
from util.logger import Logger
from util.singletone import Singleton


class FailureDetector(IFailureDetector, metaclass=Singleton):
    sample_size = 100
    phi_suspect_threshold = 5
    phi_convict_threshold = 8

    def __init__(self):
        self.arrival_samples: dict[Endpoint, ArrivalWindow] = {}
        self.fd_evnt_listeners: list[IFailureDetectionEventListener] = []

    def is_alive(self, ep: Endpoint):
        pass

    def interpret(self, ep: Endpoint):
        hb_window = self.arrival_samples.get(ep)

        if hb_window is None:
            return

        now = datetime.datetime.now().timestamp() * 1000
        is_convicted = False
        is_suspected = False

        detector_report = hb_window.phi(now)

        phi = detector_report.phi

        Logger.info(f"Failure Detector ({ep}) calculated phi = {phi}, probability = {detector_report.probability}")

        if phi > self.phi_convict_threshold:
            is_convicted = True
            for listener in self.fd_evnt_listeners:
                listener.convict(ep, detector_report)
        if not is_convicted and phi > self.phi_suspect_threshold:
            is_suspected = True
            for listener in self.fd_evnt_listeners:
                listener.suspect(ep, detector_report)

        if not is_suspected and phi <= self.phi_suspect_threshold:
            for listener in self.fd_evnt_listeners:
                listener.reanimate(ep, detector_report)

    def report(self, ep: Endpoint):
        now = datetime.datetime.now().timestamp() * 1000
        arrival_window = self.arrival_samples.get(ep)

        if arrival_window is None:
            arrival_window = ArrivalWindow(self.sample_size)
            self.arrival_samples[ep] = arrival_window

        arrival_window.add(now)

    def register_failure_detection_event_listener(self, listener: IFailureDetectionEventListener):
        self.fd_evnt_listeners.append(listener)  # Add the listener to the list

    def unregister_failure_detection_event_listener(self, listener: IFailureDetectionEventListener):
        self.fd_evnt_listeners.remove(listener)  # Remove the listener from the list

    def __str__(self):
        sb = []
        eps = self.arrival_samples.keys()

        sb.append("-----------------------------------------------------------------------")
        for ep in eps:
            hb_window = self.arrival_samples[ep]
            sb.append(str(ep) + " : ")
            sb.append(str(hb_window))
            sb.append('\n')
        sb.append("-----------------------------------------------------------------------")
        return ''.join(sb)
