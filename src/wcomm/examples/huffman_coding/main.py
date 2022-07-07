from wcomm.message import Message
from wcomm.encoding.source.huffman import HuffmanCode


def main():
    small_msg = Message("Hello world!", "HEADER")
    encoder = HuffmanCode.from_message(small_msg)
    encoded_small_msg = encoder.encode(small_msg)
    headerless_encoded = Message.from_binary(encoded_small_msg._header + encoded_small_msg._data)
    decoded_small_msg = encoder.decode(encoded_small_msg)
    headerless_decoded = encoder.decode(headerless_encoded, 6 * 8)
    print(f"{small_msg} -> ENCODED : {encoded_small_msg}   DECODED : {decoded_small_msg}")
    print(f"{small_msg} -> ENCODED : {headerless_encoded}   DECODED : {headerless_decoded}")
    
    # This message should code the 'p' char as the highest probability
    # one, probably followed by 'P'
    message1 = Message("""Peter Piper picked a peck of pickled peppers
A peck of pickled peppers Peter Piper picked
If Peter Piper picked a peck of pickled peppers
Where's the peck of pickled peppers Peter Piper picked?""")

    #This one should code 'w' as the highest
    message2 = Message("""How much wood would a woodchuck chuck if a woodchuck could chuck wood?
He would chuck, he would, as much as he could, and chuck as much wood
As a woodchuck would if a woodchuck could chuck wood""")

    test1 = HuffmanCode.generate_frequency_map(message1)
    print(f"Message 1 (P) -> {test1[ord('P')]}")
    print(f"Message 1 (p) -> {test1[ord('p')]}")
    print(f"Message 1 (e) -> {test1[ord('e')]}")
    print(f"Message 1 (f) -> {test1[ord('f')]}")
    print(f"Message 1 (s) -> {test1[ord('s')]}")
    print(f"Message 1 (t) -> {test1[ord('t')]}")

    test2 = HuffmanCode.generate_frequency_map(message2)
    print(f"Message 2 (w) -> {test2[ord('w')]}")


    source_coding1 = HuffmanCode.from_message(message1)
    source_coding2 = HuffmanCode.from_message(message2)

    print(f"Huffman coding from message 1 -> {source_coding1.as_string_dict()}")
    print(f"Huffman coding from message 2 -> {source_coding2.as_string_dict()}")

    encoded_msg1_1 = source_coding1.encode(message1)
    encoded_msg2_1 = source_coding1.encode(message2)
    encoded_msg1_2 = source_coding2.encode(message1)
    encoded_msg2_2 = source_coding2.encode(message2)
    print(f"Message 1 encoded from message 1 ===\n{encoded_msg1_1}\n")
    print(f"Message 2 encoded from message 1 ===\n{encoded_msg2_1}\n")
    print(f"Message 1 encoded from message 2 ===\n{encoded_msg1_2}\n")
    print(f"Message 2 encoded from message 2 ===\n{encoded_msg2_2}\n")
    decoded_msg1_1 = source_coding1.decode(encoded_msg1_1)
    decoded_msg2_1 = source_coding1.decode(encoded_msg2_1)
    decoded_msg1_2 = source_coding2.decode(encoded_msg1_2)
    decoded_msg2_2 = source_coding2.decode(encoded_msg2_2)
    print(f"Message 1 decoded from message 1 ===\n{decoded_msg1_1}\n")
    print(f"Message 2 decoded from message 1 ===\n{decoded_msg2_1}\n")
    print(f"Message 1 decoded from message 2 ===\n{decoded_msg1_2}\n")
    print(f"Message 2 decoded from message 2 ===\n{decoded_msg2_2}\n")


if __name__ == "__main__":
    main()
