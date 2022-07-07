from wcomm.message import Message
from wcomm.encoding.source.huffman import HuffmanCode


def main():
    message_r = Message.from_image("wcomm/examples/resources/img/img_house.jpeg", 0)
    message_g = Message.from_image("wcomm/examples/resources/img/img_house.jpeg", 1)
    message_b = Message.from_image("wcomm/examples/resources/img/img_house.jpeg", 2)

    print(message_r.bit_size() + message_g.bit_size() + message_b.bit_size())

    coding_r = HuffmanCode.from_message(message_r)
    coding_g = HuffmanCode.from_message(message_g)
    coding_b = HuffmanCode.from_message(message_b)
    
    print(coding_r.encode(message_r).bit_size() + coding_g.encode(message_g).bit_size() + coding_b.encode(message_b).bit_size())
