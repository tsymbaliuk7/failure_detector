import math


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

    def sum_of_deviations(self):
        """
        Calculate the sum of squared deviations from the mean.

        Returns:
            float: The sum of squared deviations.
        """
        mean_value = self.mean()
        return sum((x - mean_value) ** 2 for x in self.arrival_intervals)

    def mean(self):
        """
        Calculate the mean of arrival intervals in the window.

        Returns:
            float: The mean of arrival intervals.
        """
        return self.sum() / len(self.arrival_intervals)

    def variance(self):
        """
        Calculate the variance of arrival intervals in the window.

        Returns:
            float: The variance of arrival intervals.
        """
        return self.sum_of_deviations() / len(self.arrival_intervals)

    def deviation(self):
        """
        Calculate the standard deviation of arrival intervals in the window.

        Returns:
            float: The standard deviation of arrival intervals.
        """
        return math.sqrt(self.variance())

    def clear(self):
        """
        Clear all arrival intervals from the window.
        """
        self.arrival_intervals.clear()

    def p(self, t):
        """
        Calculate the probability using the Exponential Cumulative Distribution Function (CDF).

        Args:
            t (float): The value for which to calculate the probability.

        Returns:
            float: The calculated probability.
        """
        mean_value = self.mean()
        exponent = (-t) / mean_value
        return 1 - (1 - math.exp(exponent))

    def phi(self, t_now):
        """
        Calculate the log likelihood ratio (phi) for a given time.

        Args:
            t_now (float): The current time.

        Returns:
            float: The calculated log likelihood ratio (phi).
        """
        if len(self.arrival_intervals) > 0:
            t = t_now - self.t_last
            probability = self.p(t)
            log_value = (-1) * math.log10(probability)
            return log_value
        return 0.0

    def __str__(self):
        """
        Return a string representation of the Arrival Window.

        Returns:
            str: A string containing the arrival intervals.
        """
        return ' '.join(map(str, self.arrival_intervals))
