from wcomm.message import Message
from wcomm.modulation import FSK16, MFSK
from wcomm.encoding.source import HuffmanCode
from wcomm.channels import SoundChannel
from threading import Thread
from skimage.color import rgb2yuv
import numpy as np


PERIOD = 20
DELTA_BASES = 2000
BASES = [500 + DELTA_BASES * i for i in range(4)]


def main():
    mod1 = MFSK(16, BASES[0], 100)
    mod2 = MFSK(16, BASES[1], 100)
    mod3 = MFSK(16, BASES[2], 100)
    mod4 = MFSK(16, BASES[3], 100)
    channel1 = SoundChannel(mod1)
    channel2 = SoundChannel(mod2)
    channel3 = SoundChannel(mod3)
    channel4 = SoundChannel(mod4)

    msg_y = Message.from_image("wcomm/resources/img/img_house.jpeg",
                               0, lambda data: (255 * rgb2yuv(data)).astype(np.uint8))
    msg_u = Message.from_image("wcomm/resources/img/img_house.jpeg",
                               1, lambda data: (255 * rgb2yuv(data)).astype(np.uint8))
    msg_v = Message.from_image("wcomm/resources/img/img_house.jpeg",
                               2, lambda data: (255 * rgb2yuv(data)).astype(np.uint8))
    msg_text = Message.from_file("wcomm/resources/binaries/project2")

    source_y = HuffmanCode.from_message(msg_y)
    source_u = HuffmanCode.from_message(msg_u)
    source_v = HuffmanCode.from_message(msg_v)
    source_text = HuffmanCode.from_message(msg_text)
    encoded_y = source_y.encode(msg_y)
    encoded_u = source_u.encode(msg_u)
    encoded_v = source_v.encode(msg_v)
    encoded_text = source_text.encode(msg_text)

    # Use multithreading to send simultaneously
    thread_y = Thread(target=send, args=(channel2, encoded_y, PERIOD))
    thread_u = Thread(target=send, args=(channel3, encoded_u, PERIOD))
    thread_v = Thread(target=send, args=(channel4, encoded_v, PERIOD))
    thread_text = Thread(target=send, args=(channel1, encoded_text, PERIOD))

    thread_y.start()
    thread_u.start()
    thread_v.start()
    thread_text.start()

    thread_y.join()
    thread_u.join()
    thread_v.join()
    thread_text.join()


def send(channel, message, period):
    channel.send(message, period)
