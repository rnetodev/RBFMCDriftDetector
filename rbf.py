"""
Radial Basis Function Network implementation
Ruivaldo Neto - rneto at rneto.net
"""

import numpy as np
from markov import MarkovChain


class RBFMCDriftDetector:
    """Radial Basis Function with Markov Chain detector."""

    def __init__(self, sigma=0.1, threshold=0.9):
        self.sigma = sigma
        self.threshold = threshold

        self.centers = []
        self.actual_center = None

    def handle(self, input_data):
        print("\n" * 2)
        print(f"input_data: {input_data}")
        print(f"centers: {self.centers}")
        print(self.actual_center)

        activation_threshold = self.threshold
        activated_center = None
        activation = 0.0

        for center in self.centers:
            distance = np.sqrt(np.float_power(input_data - center, 2))
            activation = np.exp(
                # ϕ(r) = exp(- r²/2σ²)
                -(np.float_power(distance, 2.0))
                / (2.0 * np.float_power(self.sigma, 2.0))
            )

            print(
                f"input_data: {input_data} - center: {center} - activation: {activation}"
            )

            if activation >= activation_threshold:
                activated_center = center
                activation_threshold = activation

        # no center activates, so we have a new center
        if activated_center is None:
            self.centers.append(input_data)
            activated_center = input_data

        # if no center had been activated before
        if self.actual_center is None:
            self.actual_center = input_data

        # if actual_center is not the activated_center, drift, drift!
        if self.actual_center != activated_center:
            self.actual_center = activated_center

            return True

        return False

    def is_center(self, value):
        return value in self.centers
