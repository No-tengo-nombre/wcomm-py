import winsound
from time import sleep
from wcomm.channel import Channel
from wcomm.utils.log import log
from pysinewave import SineWave


DEFAULT_SOUND_TIME = 1000
sine = None


def set_sine_freq(freq):
    global sine
    if sine is None:
        sine = SineWave(pitch_per_second=10000)
        sine.set_frequency(freq)
        sine.play()
        return sine
    else:
        sine.set_frequency(freq)
        return sine


class SoundChannel(Channel):
    def __init__(self, modulator):
        log(f"SETTING MODULATION -> {modulator.get_name()}")
        self._modulator = modulator

    def send(self, message, time=DEFAULT_SOUND_TIME):
        log(f"SEND MESSAGE \"{message}\"")
        self._modulator.send_through_channel(self, message, time)

    def play(self, frequency, time=DEFAULT_SOUND_TIME):
        log(f"PLAY {frequency} Hz , {time} ms\n")
        # winsound.Beep(frequency, time)
        set_sine_freq(frequency)
        sleep(time / 1000)

    def listen(self, frequency):
        self._modulator.listen(frequency)
