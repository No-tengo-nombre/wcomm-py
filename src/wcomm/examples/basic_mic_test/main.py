from wcomm.modulation.mfsk import FSK256
from wcomm.channels.sound import SoundChannel
import numpy as np


def main():
    mod = FSK256(100, 30)
    channel = SoundChannel(mod)
    channel.start_microphone()

    values = []
    predicted = 0
    found = False

    while True:
        detection = channel.detect(441)
        if detection == -1:
            values = []
            if found:
                print(f"PREDICTION : {predicted:5} -> {chr(predicted)}")
            found = False
            continue
        else:
            found = True
            values.append(detection)
            predicted = int(np.round(np.mean(values)))
            # print(f"{detection:5} -> {chr(detection):5}")
