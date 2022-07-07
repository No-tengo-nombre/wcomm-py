from wcomm.modulation.modulation import Modulator
from wcomm.utils.log import log
import numpy as np


PSK256_BASE_FREQUENCY = 2000
DEFAULT_SAMPLING_FREQUENCY = 44100


class PSK256(Modulator):
    def __init__(self, base_frequency=PSK256_BASE_FREQUENCY,
                 samp_freq=DEFAULT_SAMPLING_FREQUENCY):
        self._base_frequency = base_frequency
        self._sampling_frequency = samp_freq

    def get_name(self):
        return "256-PSK"

    def split(self, message):
        for char in message:
            yield ord(char)

    def send_through_channel(self, channel, message, time):
        for key in self.split(message):
            log(f"INFO::SEND CHAR '{chr(key)}' = {key}")
            channel.play(self.calculate_frequency(key), time)

    def get_base_functions(self, num):
        """Returns a matrix with 2 rows, each corresponding to a base
        function, and `num` columns, each corresponding to a data point.
        """
        # This operation basically applies a DFT to the data, and chooses
        # the row with the highest Fourier coefficient
        return np.array([
            np.cos(2 * np.pi * self._base_frequency * np.arange(num) / self._sampling_frequency + self.calculate_phase())
        ])

    def calculate_phase(self, key):
        return 2 * np.pi * key / 256

    def detect(self, data, threshold):
        """Returns the index, starting from zero, of the detected symbol."""
        # For out of phase signals, this method throws good results as long
        # as the number of points is sufficiently large
        candidate = np.argmax(self.get_base_functions(len(data)) @ data)
        return candidate if candidate >= threshold else -1
        # return np.argmax(self.get_base_functions(len(data)) @ data)

    def listen(self, frequency): pass
