import math

from failure_detector.detector_report import DetectorReport


class ArrivalWindow:
    """
    Represents an Arrival Window in the context of a Failure Detection system.
    """

    def __init__(self, size):
        """
        Initialize an Arrival Window with a specified size.

        Args:
            size (int): The size of the arrival window.
        """
        self.t_last = 0.0
        self.arrival_intervals = []
        self.size = size

    def add(self, value):
        """
        Add a value to the arrival window.

        Args:
            value (float): The value to add.
        """
        if len(self.arrival_intervals) == self.size:
            self.arrival_intervals.pop(0)

        inter_arrival_time = 0.0
        if self.t_last > 0.0:
            inter_arrival_time = value - self.t_last
        self.t_last = value
        self.arrival_intervals.append(inter_arrival_time)

    def sum(self):
        """
        Calculate the sum of arrival intervals in the window.

        Returns:
            float: The sum of arrival intervals.
        """
        return sum(self.arrival_intervals)

    def mean(self):
        """
        Calculate the mean of arrival intervals in the window.

        Returns:
            float: The mean of arrival intervals.
        """
        return self.sum() / len(self.arrival_intervals)

    def clear(self):
        """
        Clear all arrival intervals from the window.
        """
        self.arrival_intervals.clear()

    def probability(self, t):
        """
        Calculate the probability using the Exponential Cumulative Distribution Function (CDF).

        For CDF: mean = 1/l => l = 1/mean where l(lambda) is rate, or inverse scale

        CDF: F(t) = 1 - e^(-l*t) =>  F(t) = 1 - e^(-t/mean),

        Args:
            t (float): The value for which to calculate the probability.

        Returns:
            float: The calculated probability of whether some event will happen in t time.
        """
        mean_value = self.mean()

        if mean_value == 0:
            return 0

        exp_pow = (-t) / mean_value
        return 1 - (1 - math.exp(exp_pow))

    def phi(self, t_now) -> DetectorReport:
        """
        Calculate the log likelihood ratio (phi) for a given time.

        Args:
            t_now (float): The current time.

        Returns:
            float: The calculated log likelihood ratio (phi).
        """
        if len(self.arrival_intervals) > 0:

            t = t_now - self.t_last
            probability = self.probability(t)

            if probability == 0:
                return DetectorReport(float('inf'), probability)

            log_value = (-1) * math.log10(probability)
            return DetectorReport(log_value, probability)
        return DetectorReport(0.0, 0.0)

    def __str__(self):
        """
        Return a string representation of the Arrival Window.

        Returns:
            str: A string containing the arrival intervals.
        """
        return ' '.join(map(str, self.arrival_intervals))
