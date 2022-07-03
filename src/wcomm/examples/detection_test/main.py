from wcomm.modulation.mfsk import FSK256
import numpy as np


def main():
    num = 10000
    
    mod = FSK256()
    test_axis1 = np.cos(
        2 * np.pi * 300 * mod._sampling_frequency * np.arange(num))
    test_axis1_phased = np.cos(
        2 * np.pi * 300 * mod._sampling_frequency * np.arange(num) + 1)
    test_axis2 = np.cos(
        2 * np.pi * 650 * mod._sampling_frequency * np.arange(num))
    test_axis2_phased = np.cos(
        2 * np.pi * 650 * mod._sampling_frequency * np.arange(num) + 1)

    print(f"AXIS 1 -> {mod.detect(test_axis1)} , {mod.detect(test_axis1_phased)}\nAXIS 2 -> {mod.detect(test_axis2)} , {mod.detect(test_axis2_phased)}")
