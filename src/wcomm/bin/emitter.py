from wcomm.channels.sound import SoundChannel
from wcomm.modulation.mfsk import FSK256, FSK16
from wcomm.encoding.source.huffman import HuffmanCode
from wcomm.message import Message
from time import sleep


def main(filename, modulation, source, source_template, channel_type, period):
    channel = channel_type(modulation())

    message = Message.from_file(filename)

    source_coding = source.from_message(message)
    encoded_msg = source_coding.encode(message)

    channel.send(encoded_msg, period)
