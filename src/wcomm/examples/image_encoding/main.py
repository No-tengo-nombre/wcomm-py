from wcomm.message import Message
from wcomm.encoding.source.huffman import HuffmanCode


def main():
    images = [
        # "img_airplane.png",
        # "img_baboon.png",
        "img_house.jpeg",
        # "img_parrots.jpeg",
        # "img_peppers.jpeg",
        # "img_sailboat.png",
    ]

    img_r = Message.from_image("wcomm/examples/resources/img/img_house.jpeg", 0)
    img_g = Message.from_image("wcomm/examples/resources/img/img_house.jpeg", 1)
    img_b = Message.from_image("wcomm/examples/resources/img/img_house.jpeg", 2)
    huffman_r = HuffmanCode.from_message(img_r)
    huffman_g = HuffmanCode.from_message(img_g)
    huffman_b = HuffmanCode.from_message(img_b)

    for img_name in images:
        print(f"=== IMAGE <{img_name}> ===")
        img_r = Message.from_image(f"wcomm/examples/resources/img/{img_name}", 0)
        img_g = Message.from_image(f"wcomm/examples/resources/img/{img_name}", 1)
        img_b = Message.from_image(f"wcomm/examples/resources/img/{img_name}", 2)

        # huffman_r = HuffmanCode.from_message(img_r)
        # huffman_g = HuffmanCode.from_message(img_g)
        # huffman_b = HuffmanCode.from_message(img_b)

        encoded_r = huffman_r.encode(img_r)
        encoded_g = huffman_g.encode(img_g)
        encoded_b = huffman_b.encode(img_b)

        print(f"<{img_name}> R:> {img_r.bit_size()} b -> {encoded_r.bit_size()} b    <=>    {100 * (img_r.bit_size() - encoded_r.bit_size()) / img_r.bit_size():.2f}%")
        print(f"<{img_name}> G:> {img_g.bit_size()} b -> {encoded_g.bit_size()} b    <=>    {100 * (img_g.bit_size() - encoded_g.bit_size()) / img_g.bit_size():.2f}%")
        print(f"<{img_name}> B:> {img_b.bit_size()} b -> {encoded_b.bit_size()} b    <=>    {100 * (img_b.bit_size() - encoded_b.bit_size()) / img_b.bit_size():.2f}%")

        decoded_r = huffman_r.decode(encoded_r)
        decoded_g = huffman_g.decode(encoded_g)
        decoded_b = huffman_b.decode(encoded_b)

        print(f"<{img_name}> R:> EQUAL {img_r == decoded_r}")
        print(f"<{img_name}> G:> EQUAL {img_g == decoded_g}")
        print(f"<{img_name}> B:> EQUAL {img_b == decoded_b}")
        print("\n\n")
