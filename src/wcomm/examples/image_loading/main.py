from wcomm.message import Message
from wcomm.encoding.source.huffman import HuffmanCode
from wcomm.utils.log import metric_prefix
from skimage.color import rgb2hsv, rgb2yuv
import numpy as np


def main():
    # Reading the data in RGB
    rgb_msg_r = Message.from_image("wcomm/examples/resources/img/img_house.jpeg", 0)
    rgb_msg_g = Message.from_image("wcomm/examples/resources/img/img_house.jpeg", 1)
    rgb_msg_b = Message.from_image("wcomm/examples/resources/img/img_house.jpeg", 2)

    print(f"RGB Before encoding -> {metric_prefix(rgb_msg_r.bit_size() + rgb_msg_g.bit_size() + rgb_msg_b.bit_size(), 'b')}")

    rgb_cd_r = HuffmanCode.from_message(rgb_msg_r)
    rgb_cd_g = HuffmanCode.from_message(rgb_msg_g)
    rgb_cd_b = HuffmanCode.from_message(rgb_msg_b)
    
    print(f"RGB After encoding -> {metric_prefix(rgb_cd_r.encode(rgb_msg_r).bit_size() + rgb_cd_g.encode(rgb_msg_g).bit_size() + rgb_cd_b.encode(rgb_msg_b).bit_size(), 'b')}")


    # Reading the data in HSV
    hsv_msg_h = Message.from_image("wcomm/examples/resources/img/img_house.jpeg", 0, lambda data: (255 * rgb2hsv(data)).astype(np.uint8))
    hsv_msg_s = Message.from_image("wcomm/examples/resources/img/img_house.jpeg", 1, lambda data: (255 * rgb2hsv(data)).astype(np.uint8))
    hsv_msg_v = Message.from_image("wcomm/examples/resources/img/img_house.jpeg", 2, lambda data: (255 * rgb2hsv(data)).astype(np.uint8))


    print(f"HSV Before encoding -> {metric_prefix(hsv_msg_h.bit_size() + hsv_msg_s.bit_size() + hsv_msg_v.bit_size(), 'b')}")

    hsv_cd_h = HuffmanCode.from_message(hsv_msg_h)
    hsv_cd_s = HuffmanCode.from_message(hsv_msg_s)
    hsv_cd_v = HuffmanCode.from_message(hsv_msg_v)
    
    print(f"HSV After encoding -> {metric_prefix(hsv_cd_h.encode(hsv_msg_h).bit_size() + hsv_cd_s.encode(hsv_msg_s).bit_size() + hsv_cd_v.encode(hsv_msg_v).bit_size(), 'b')}")


    # Reading the data in YUV
    yuv_msg_y = Message.from_image("wcomm/examples/resources/img/img_house.jpeg", 0, lambda data: (255 * rgb2yuv(data)).astype(np.uint8))
    yuv_msg_u = Message.from_image("wcomm/examples/resources/img/img_house.jpeg", 1, lambda data: (255 * rgb2yuv(data)).astype(np.uint8))
    yuv_msg_v = Message.from_image("wcomm/examples/resources/img/img_house.jpeg", 2, lambda data: (255 * rgb2yuv(data)).astype(np.uint8))


    print(f"YUV Before encoding -> {metric_prefix(yuv_msg_y.bit_size() + yuv_msg_u.bit_size() + yuv_msg_v.bit_size(), 'b')}")

    yuv_cd_y = HuffmanCode.from_message(yuv_msg_y)
    yuv_cd_u = HuffmanCode.from_message(yuv_msg_u)
    yuv_cd_v = HuffmanCode.from_message(yuv_msg_v)

    print(f"YUV After encoding -> {metric_prefix(yuv_cd_y.encode(yuv_msg_y).bit_size() + yuv_cd_u.encode(yuv_msg_u).bit_size() + yuv_cd_v.encode(yuv_msg_v).bit_size(), 'b')}")
