from abc import ABC, abstractmethod


class Modulator(ABC):
    """Base class for a modulator."""

    @abstractmethod
    def get_name(self): pass

    @abstractmethod
    def split(self, message): pass

    @abstractmethod
    def send_through_channel(self, channel, message, time): pass

    @abstractmethod
    def calculate_frequency(self, key): pass

    @abstractmethod
    def detect(self, data, samp_freq): pass

    @abstractmethod
    def listen(self, frequency): pass
