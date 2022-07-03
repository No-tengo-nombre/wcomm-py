from wcomm.modulation.modulation import Modulator
from wcomm.utils.log import log


FSK256_BASE_FREQUENCY = 300
FSK256_DELTA_FREQUENCY = 50


class FSK256(Modulator):
    def __init__(self, base_frequency=FSK256_BASE_FREQUENCY, delta_frequency=FSK256_DELTA_FREQUENCY):
        self._base_frequency = base_frequency
        self._delta_frequency = delta_frequency

    def get_name(self):
        return "256-FSK"

    def split(self, message):
        for char in message:
            yield ord(char)

    def send_through_channel(self, channel, message, time):
        for key in self.split(message):
            log(f"SEND CHAR '{chr(key)}' = {key}")
            channel.play(self.calculate_frequency(key), time)

    def calculate_frequency(self, key):
        return self._base_frequency + key * self._delta_frequency
