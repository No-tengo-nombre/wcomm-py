from wcomm.message import Message
from wcomm.encoding.source.source_coding import SourceCoding
from multipledispatch import dispatch
from wcomm.utils.log import log, metric_prefix
from wcomm.utils.data_structures import TreeNode


class HuffmanCode(SourceCoding):
    def __init__(self, code=None):
        """The variable `code` corresponds to a dictionary which assigns
        every char (as a number, so a char is a number between 0 and 255)
        a given string of 0's and 1's. These should correspond to a
        Huffman code.
        """
        self._code = code

    def __str__(self):
        return str(self._code)

    @dispatch(str)
    def __getitem__(self, item):
        return self._code[ord(item)]

    @dispatch(int)
    def __getitem__(self, item):
        return self._code[item]

    def inverted_code(self):
        return {val: key for key, val in self._code.items()}

    def as_string_dict(self):
        return {chr(key): val for key, val in self._code.items()}

    def encode(self, message):
        log(f"INFO::H-CODING INPUT IS {metric_prefix(message.bit_size(), 'b')}")
        output = "".join([self._code[c] for c in message.as_int_array(True)])
        out_msg = Message.from_binary(output)
        log(f"INFO::H-CODING OUTPUT IS {metric_prefix(out_msg.bit_size(), 'b')}")
        log(f"INFO::REDUCED SIZE BY {100 * (message.bit_size(True) - out_msg.bit_size(True)) / message.bit_size(True):.4f}%")
        return out_msg

    def decode(self, message):
        log(f"INFO::H-DECODING INPUT IS {metric_prefix(message.bit_size(True), 'b')}")
        decode_dict = self.inverted_code()
        output = ""
        temp = ""

        for b in message:
            temp += b
            try:
                output += chr(decode_dict[temp])
                temp = ""
            except KeyError:
                pass

        out_msg = Message(output)
        log(f"INFO::H-DECODING OUTPUT IS {metric_prefix(out_msg.bit_size(True), 'b')}")
        return out_msg

    @staticmethod
    def __make_tree(freq_map_items):
        map_items = freq_map_items.copy()
        while len(map_items) > 1:
            (char1, freq1) = map_items.pop(0)
            (char2, freq2) = map_items.pop(0)
            node = TreeNode(char1, char2)
            map_items.append((node, freq1 + freq2))
            map_items = sorted(map_items, key=lambda x: x[1])
        return map_items[0]

    @staticmethod
    def __make_huffman_dict(tree_node, binary_code=""):
        # Border case for the recursion
        if type(tree_node) is int:
            return {tree_node: binary_code}

        # Update the dictionary according to the Huffman algorithm
        (left, right) = tree_node.get_children()
        output = {
            **HuffmanCode.__make_huffman_dict(left, binary_code + "0"),
            **HuffmanCode.__make_huffman_dict(right, binary_code + "1"),
        }
        return output

    @staticmethod
    def generate_code(message):
        log(f"INFO::GENERATING HUFFMAN CODE")
        freq_map = HuffmanCode.generate_frequency_map(message)
        map_items = sorted(freq_map.items(), key=lambda x: x[1])
        tree_node = HuffmanCode.__make_tree(map_items)
        huffman_code = HuffmanCode.__make_huffman_dict(tree_node[0])
        log(f"INFO::FINISHED GENERATING HUFFMAN CODE")
        return huffman_code
