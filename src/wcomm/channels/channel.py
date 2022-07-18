from abc import ABC, abstractmethod


class Channel(ABC):
    """Interface for a channel."""

    @abstractmethod
    def send(self, message, time, send_header=True): pass

    @abstractmethod
    def play(self, frequency, time): pass

    @abstractmethod
    def stop(self): pass

    @abstractmethod
    def listen(self, frequency): pass
