from abc import ABC, abstractmethod


class Channel(ABC):
    """Interface for a channel."""

    @abstractmethod
    def send(self, message, time): pass

    @abstractmethod
    def play(self, frequency, time): pass

    @abstractmethod
    def listen(self, frequency): pass
