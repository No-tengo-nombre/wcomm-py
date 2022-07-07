import numpy as np
import cv2


def main():
    data = cv2.imread("wcomm/examples/resources/img_house.jpeg")
    data_arr = np.array(data)
    print(data_arr)
