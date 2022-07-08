from wcomm.utils.log import log
from wcomm.message import Message
from abc import ABC, abstractmethod


class Modulator(ABC):
    """Base class for a modulator."""

    @abstractmethod
    def get_name(self): pass

    def get_name_message(self):
        return Message(self.get_name())

    @abstractmethod
    def split(self, message): pass

    def send_name(self, channel, time):
        log(f"INFO::SEND MODULATION HEADER")
        for key in self.split(self.get_name_message()):
            log(f"INFO::SEND CHAR '{chr(key)}' = {key}")
            channel.play(self.calculate_frequency(key), time)

    @abstractmethod
    def send_through_channel(self, channel, message, time, send_header=True): pass

    @abstractmethod
    def detect(self, data, samp_freq): pass

    @abstractmethod
    def listen(self, frequency): pass
