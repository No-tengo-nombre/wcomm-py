from abc import ABC, abstractmethod


class SourceCoding(ABC):
    """Abstract class for a source coding scheme."""

    @abstractmethod
    def encode(self, message): pass
