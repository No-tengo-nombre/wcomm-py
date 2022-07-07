from wcomm.message import Message
from wcomm.encoding.source.huffman import HuffmanCode
from wcomm.utils.log import metric_prefix
from skimage.color import rgb2hsv


def main():
    # Reading the data in RGB
    rgb_msg_r = Message.from_raw_image("wcomm/examples/resources/img/img_house.jpeg", 0)
    rgb_msg_g = Message.from_raw_image("wcomm/examples/resources/img/img_house.jpeg", 1)
    rgb_msg_b = Message.from_raw_image("wcomm/examples/resources/img/img_house.jpeg", 2)

    print(f"RGB Before encoding -> {metric_prefix(rgb_msg_r.bit_size() + rgb_msg_g.bit_size() + rgb_msg_b.bit_size(), 'b')}")

    rgb_cd_r = HuffmanCode.from_message(rgb_msg_r)
    rgb_cd_g = HuffmanCode.from_message(rgb_msg_g)
    rgb_cd_b = HuffmanCode.from_message(rgb_msg_b)
    
    print(f"RGB After encoding -> {metric_prefix(rgb_cd_r.encode(rgb_msg_r).bit_size() + rgb_cd_g.encode(rgb_msg_g).bit_size() + rgb_cd_b.encode(rgb_msg_b).bit_size(), 'b')}")


    # Reading the data in HSV
    hsv_msg_h = Message.from_raw_image("wcomm/examples/resources/img/img_house.jpeg", 0, rgb2hsv)
    hsv_msg_s = Message.from_raw_image("wcomm/examples/resources/img/img_house.jpeg", 1, rgb2hsv)
    hsv_msg_v = Message.from_raw_image("wcomm/examples/resources/img/img_house.jpeg", 2, rgb2hsv)

    print(f"HSV Before encoding -> {metric_prefix(hsv_msg_h.bit_size() + hsv_msg_s.bit_size() + hsv_msg_v.bit_size(), 'b')}")

    hsv_cd_r = HuffmanCode.from_message(hsv_msg_h)
    hsv_cd_g = HuffmanCode.from_message(hsv_msg_s)
    hsv_cd_b = HuffmanCode.from_message(hsv_msg_v)
    
    print(f"HSV After encoding -> {metric_prefix(hsv_cd_r.encode(hsv_msg_h).bit_size() + hsv_cd_g.encode(hsv_msg_s).bit_size() + hsv_cd_b.encode(hsv_msg_v).bit_size(), 'b')}")
