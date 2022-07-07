from wcomm.channels.sound import SoundChannel
from wcomm.modulation.mfsk import FSK256
from wcomm.encoding.source.huffman import HuffmanCode
from wcomm.message import Message


def main():
    mod_type = FSK256(100, 30)
    channel = SoundChannel(mod_type)

    message = Message("Hello world!")
    source_coding = HuffmanCode.from_message(message)
    encoded_msg = source_coding.encode(message)

    channel.send(message, 100)
    channel.send(Message(" "), 5000)
    channel.send(encoded_msg, 100)


if __name__ == "__main__":
    main()
