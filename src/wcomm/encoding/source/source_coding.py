from abc import ABC, abstractmethod, abstractstaticmethod


class SourceCoding(ABC):
    """Abstract class for a source coding scheme."""
    __EMPTY_CHAR_MAPPING = {key: 0 for key in range(256)}

    @classmethod
    def from_message(cls, message):
        return cls(code=cls.generate_code(message))

    def update_code(self, message):
        self._code = self.generate_code(message)

    @staticmethod
    def empty_map():
        return SourceCoding.__EMPTY_CHAR_MAPPING.copy()

    @staticmethod
    def generate_frequency_map(message):
        output = SourceCoding.empty_map()
        for c in message.as_string(True):
            output[ord(c)] += 1
        return output

    @abstractmethod
    def encode(self, message): pass

    @abstractmethod
    def decode(self, message): pass

    @abstractstaticmethod
    def generate_code(message): pass
