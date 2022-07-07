from wcomm.message import Message
from wcomm.encoding.source.huffman import HuffmanCode


def main():
    test_img = Message.from_file("wcomm/examples/resources/img/img_house.jpeg")
    huffman_coding = HuffmanCode.from_message(test_img)

    encoded = huffman_coding.encode(test_img)
    decoded = huffman_coding.decode(encoded)

    print(f"Equal messages -> {decoded == test_img}")
