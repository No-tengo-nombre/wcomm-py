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

    def __getitem__(self, key):
        return self.raw_string()[key]

    @classmethod
    def from_binary(cls, content="", header="", *args, **kwargs):
        output = cls(*args, **kwargs)
        output._data = content
        output._header = header
        return output

    @classmethod
    def from_raw_image(cls, filename, channel=None, preprocessing=None, *args, **kwargs):
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
            # contains information about the image. In this case, it is
            # 32 bits for the number of rows, 32 bits for the number of
            # columns, and 8 bits for the number of channels
            msg_header = (
                bin(len(channel_data))[:2].zfill(32)
                + bin(len(channel_data[0]))[:2].zfill(32)
                + bin(1)[:2].zfill(8)
            )
            flattened_data = flatten_matrix(channel_data)

            result._header = msg_header

            # Since we know every pixel is 8 bits, we can code each one
            # as a string of 8 bits (that way each pixel has a fixed
            # length).
            result._data = "".join(bin(i)[2:].zfill(8) for i in flattened_data)

        return result

    def get_header(self):
        return "".join([chr(int(c, 2)) for c in self.group_string(self._header, 8)])

    def bit_size(self, only_data=False):
        return len(self._data) if only_data else len(self._header) + len(self._data)

    @staticmethod
    def group_string(message, num):
        result = []
        temp = message
        while temp != "":
            result.append(temp[:num])
            temp = temp[num:]
        return result

    def group(self, num, only_data=False):
        if only_data:
            return self.group_string(self._data, num)
        else:
            return self.group_string(self._header + self._data, num)
        # result = []
        # temp = self._data if only_data else self._header + self._data
        # while temp != "":
        #     result.append(temp[:num])
        #     temp = temp[num:]
        # return result

    def as_int_array(self, only_data=False):
        return [int(c, 2) for c in self.group(8, only_data)]

    def as_char_array(self, only_data=False):
        return [chr(int(c, 2)) for c in self.group(8, only_data)]

    def as_string(self, only_data=False):
        return "".join(self.as_char_array(only_data))

    def raw_string(self, only_data=False):
        return self._data if only_data else self._header + self._data
