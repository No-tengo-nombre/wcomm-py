from wcomm.modulation.modulation import Modulator
from wcomm.utils.log import log
import sounddevice as sd
import numpy as np


FSK256_BASE_FREQUENCY = 300
FSK256_DELTA_FREQUENCY = 50
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
        for char in message:
            yield ord(char)

    def send_through_channel(self, channel, message, time):
        for key in self.split(message):
            log(f"SEND CHAR '{chr(key)}' = {key}")
            channel.play(self.calculate_frequency(key), time)

    def get_base_functions(self, num):
        """Returns a matrix with 256 rows, each corresponding to a base
        function, and `num` columns, each corresponding to a data point.
        """
        return np.array([
            np.cos(2 * np.pi * self.calculate_frequency(k) *
                   self._sampling_frequency * np.arange(0, num))
            for k in range(256)
        ])

    def calculate_frequency(self, key):
        return self._base_frequency + key * self._delta_frequency

    def detect(self, data):
        """Returns the index, starting from zero, of the detected symbol."""
        return np.argmax(self.get_base_functions(len(data)) @ data)
        # return self.get_base_functions(len(data)) @ data

    def listen(frequency): pass
