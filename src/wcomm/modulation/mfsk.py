from wcomm.modulation.modulation import Modulator
from wcomm.utils.log import log
import numpy as np


FSK256_BASE_FREQUENCY = 300
FSK256_DELTA_FREQUENCY = 50

FSK16_BASE_FREQUENCY = 1000
FSK16_DELTA_FREQUENCY = 100

DEFAULT_SAMPLING_FREQUENCY = 44100


class FSK256(Modulator):
    def __init__(self, base_frequency=FSK256_BASE_FREQUENCY,
                 delta_frequency=FSK256_DELTA_FREQUENCY,
                 samp_freq=DEFAULT_SAMPLING_FREQUENCY):
        self._base_frequency = base_frequency
        self._delta_frequency = delta_frequency
        self._sampling_frequency = samp_freq

    def get_name(self):
        return "256-FSK"

    def split(self, message):
        for char in message.as_string():
            yield ord(char)

    def send_through_channel(self, channel, message, time):
        for key in self.split(message):
            log(f"INFO::SEND CHAR '{chr(key)}' = {key}")
            channel.play(self.calculate_frequency(key), time)

    def get_base_functions(self, num):
        """Returns a matrix with 256 rows, each corresponding to a base
        function, and `num` columns, each corresponding to a data point.
        """
        # This operation basically applies a DFT to the data, and chooses
        # the row with the highest Fourier coefficient
        return np.array([
            np.cos(2 * np.pi * self.calculate_frequency(k) *
                   np.arange(num) / self._sampling_frequency)
            for k in range(256)
        ])

    def calculate_frequency(self, key):
        return self._base_frequency + key * self._delta_frequency

    def detect(self, data, threshold):
        """Returns the index, starting from zero, of the detected symbol."""
        # For out of phase signals, this method throws good results as long
        # as the number of points is sufficiently large
        candidate = np.argmax(self.get_base_functions(len(data)) @ data)
        return candidate if candidate >= threshold else -1
        # return np.argmax(self.get_base_functions(len(data)) @ data)

    def listen(self, frequency): pass


class FSK16(Modulator):
    def __init__(self, base_frequency=FSK16_BASE_FREQUENCY,
                 delta_frequency=FSK16_DELTA_FREQUENCY,
                 samp_freq=DEFAULT_SAMPLING_FREQUENCY):
        self._base_frequency = base_frequency
        self._delta_frequency = delta_frequency
        self._sampling_frequency = samp_freq

    def get_name(self):
        return "16-FSK"

    def split(self, message):
        for b in message.group(4):
            yield int(b, 2)

    def send_through_channel(self, channel, message, time):
        for key in self.split(message):
            log(f"INFO::SEND CHAR '{chr(key)}' = {key}")
            channel.play(self.calculate_frequency(key), time)

    def get_base_functions(self, num):
        """Returns a matrix with 16 rows, each corresponding to a base
        function, and `num` columns, each corresponding to a data point.
        """
        # This operation basically applies a DFT to the data, and chooses
        # the row with the highest Fourier coefficient
        return np.array([
            np.cos(2 * np.pi * self.calculate_frequency(k) *
                   np.arange(num) / self._sampling_frequency)
            for k in range(16)
        ])

    def calculate_frequency(self, key):
        return self._base_frequency + key * self._delta_frequency

    def detect(self, data, threshold):
        """Returns the index, starting from zero, of the detected symbol."""
        # For out of phase signals, this method throws good results as long
        # as the number of points is sufficiently large
        candidate = np.argmax(self.get_base_functions(len(data)) @ data)
        return candidate if candidate >= threshold else -1
        # return np.argmax(self.get_base_functions(len(data)) @ data)

    def listen(self, frequency): pass
