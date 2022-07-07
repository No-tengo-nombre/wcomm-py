from wcomm.modulation.mfsk import FSK256
from wcomm.channels.sound import SoundChannel
from wcomm.encoding.source.huffman import HuffmanCode
from wcomm.message import Message
from wcomm.utils.log import log

from skimage.color import rgb2yuv
import numpy as np


def main():
    mod_type = FSK256(100, 30)
    channel = SoundChannel(mod_type)

    log(f"INFO::READING YUV IMAGE")
    yuv_msg_v = Message.from_raw_image("wcomm/examples/resources/img/img_house.jpeg", 2, lambda data: (255 * rgb2yuv(data)).astype(np.uint8))

    log(f"INFO::HUFFMAN CODING YUV IMAGE")
    yuv_cd_v = HuffmanCode.from_message(yuv_msg_v)

    log(f"INFO::SENDING YUV IMAGE THROUGH SOUND")
    channel.send(yuv_cd_v.encode(yuv_msg_v), 1)
