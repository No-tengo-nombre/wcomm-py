class Message:
    def __init__(self, content=""):
        # This turns data into a string of 0's and 1's, whose number of
        # elements is a multiple of 8. This way, every 8 contigous
        # characters represent a char.
        self._data = "".join([bin(ord(c))[2:].zfill(8) for c in content])

    def __iter__(self):
        return iter(self._data)

    def __next__(self):
        return next(self.__iter__())

    def __str__(self):
        return self.as_string()

    @classmethod
    def from_binary(cls, message):
        output = cls()
        output._data = message
        return output

    def bit_size(self):
        return len(self._data)

    def group(self, num):
        result = []
        temp = self._data
        while temp != "":
            result.append(temp[:num])
            temp = temp[num:]
        return result

    def as_int_array(self):
        return [int(c, 2) for c in self.group(8)]

    def as_char_array(self):
        return [chr(int(c, 2)) for c in self.group(8)]

    def as_string(self):
        return "".join(self.as_char_array())
