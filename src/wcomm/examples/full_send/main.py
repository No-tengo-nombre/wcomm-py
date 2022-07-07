from wcomm.message import Message
from wcomm.modulation import FSK16
from wcomm.encoding.source import HuffmanCode
from wcomm.channels import SoundChannel
from threading import Thread


PERIOD = 20
DELTA_BASES = 2000
BASES = [500 + DELTA_BASES * i for i in range(4)]


def main():
    mod1 = FSK16(BASES[0], 100)
    mod2 = FSK16(BASES[1], 100)
    mod3 = FSK16(BASES[2], 100)
    mod4 = FSK16(BASES[3], 100)
    channel1 = SoundChannel(mod1)
    channel2 = SoundChannel(mod2)
    channel3 = SoundChannel(mod3)
    channel4 = SoundChannel(mod4)

    msg_r = Message.from_image("wcomm/resources/img/img_house.jpeg", 0)
    msg_g = Message.from_image("wcomm/resources/img/img_house.jpeg", 1)
    msg_b = Message.from_image("wcomm/resources/img/img_house.jpeg", 2)
    msg_text = Message.from_file("wcomm/resources/binaries/project2")

    source_r = HuffmanCode.from_message(msg_r)
    source_g = HuffmanCode.from_message(msg_g)
    source_b = HuffmanCode.from_message(msg_b)
    source_text = HuffmanCode.from_message(msg_text)
    encoded_r = source_r.encode(msg_r)
    encoded_g = source_g.encode(msg_g)
    encoded_b = source_b.encode(msg_b)
    encoded_text = source_text.encode(msg_text)

    # Use multithreading to send simultaneously
    thread_r = Thread(target=send, args=(channel2, encoded_r, PERIOD))
    thread_g = Thread(target=send, args=(channel3, encoded_g, PERIOD))
    thread_b = Thread(target=send, args=(channel4, encoded_b, PERIOD))
    thread_text = Thread(target=send, args=(channel1, encoded_text, PERIOD))

    thread_r.start()
    thread_g.start()
    thread_b.start()
    thread_text.start()

    thread_r.join()
    thread_g.join()
    thread_b.join()
    thread_text.join()

def send(channel, message, period):
    channel.send(message, period)
