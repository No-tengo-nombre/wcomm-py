from wcomm.utils.data_structures import flatten_matrix
import cv2


class Message:
    def __init__(self, content="", header=""):
        # This turns data into a string of 0's and 1's, whose number of
        # elements is a multiple of 8. This way, every 8 contigous
        # characters represent a char/byte.
        self._header = "".join([bin(ord(c))[2:].zfill(8) for c in header])
        self._data = "".join([bin(ord(c))[2:].zfill(8) for c in content])

    def __iter__(self):
        return iter(self._data)

    def __next__(self):
        return next(self.__iter__())

    def __str__(self):
        return self.as_string()

    @classmethod
    def from_binary(cls, message, *args, **kwargs):
        output = cls(*args, **kwargs)
        output._data = message
        return output

    @classmethod
    def from_image(cls, filename, channel=None, preprocessing=None, *args, **kwargs):
        result = cls(*args, **kwargs)
        
        data = cv2.imread(filename)
        if preprocessing is not None:
            data = preprocessing(data)

        if channel is None:
            # TODO: Implement getting more channels at a time
            pass
        else:
            channel_data = data[:, :, channel]

            # The header is a set of data that is not compressed, and
            # contains information about the image
            msg_header = (
                bin(len(channel_data))[:2].zfill(32)                    # Number of rows
                + bin(len(channel_data[0]))[:2].zfill(32)               # Number of columns
                + bin(1)[:2].zfill(8)                                   # Number of channels
            )
            flattened_data = flatten_matrix(channel_data)               # Vector of pixel data

            result._header = msg_header

            # Since we know every pixel is 8 bits, we can code each one
            # as a string of 8 bits (that way each pixel has a fixed
            # length).
            result._data = "".join(bin(i)[2:].zfill(8) for i in flattened_data)

        return result

    def total_bit_size(self):
        return len(self._header) + self.bit_size()

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
