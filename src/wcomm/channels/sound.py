import sounddevice as sd
import numpy as np
from time import sleep
from wcomm.channels.channel import Channel
from wcomm.utils.log import log
from pysinewave import SineWave
from multipledispatch import dispatch
from numbers import Number

DEFAULT_BLOCKSIZE = 441
DEFAULT_THRESHOLD = 20
DEFAULT_SOUND_TIME = 1000
sine = None


def set_sine_freq(freq):
    global sine
    if sine is None:
        sine = SineWave(pitch_per_second=100000)
        sine.set_frequency(freq)
        sine.play()
        return sine
    else:
        sine.set_frequency(freq)
        return sine


class SoundChannel(Channel):
    def __init__(self, modulator):
        log(f"INFO::SETTING MODULATION -> {modulator.get_name()}")
        self._modulator = modulator
        self._mic_source = None

    def send(self, message, time=DEFAULT_SOUND_TIME):
        log(f"INFO::SEND MESSAGE \"{message}\"")
        self._modulator.send_through_channel(self, message, time)

    def play(self, frequency, time=DEFAULT_SOUND_TIME):
        log(f"INFO::PLAY {frequency} Hz , {time} ms\n")

        set_sine_freq(frequency)
        sleep(time / 1000)

    def start_microphone(self, sample_rate=None, channels=1):
        if sample_rate is None:
            sr = self._modulator._sampling_frequency
        else:
            sr = sample_rate

        log(f"INFO::STARTING MICROPHONE")
        self._mic_source = sd.InputStream(sr, channels=channels)
        self._mic_source.start()

    def stop_microphone(self):
        self._mic_source.stop()

    def fetch_microphone(self, blocksize=DEFAULT_BLOCKSIZE): 
        output = self._mic_source.read(blocksize)
        if output[1]:
            log(f"WARNING::OVERFLOW IN MICROPHONE")
        return output[0]

    def detect(self, blocksize=DEFAULT_BLOCKSIZE, threshold=DEFAULT_THRESHOLD):
        raw_data = self.fetch_microphone(blocksize)
        data = np.array([val[0] for val in raw_data])
        return self._modulator.detect(data, threshold)

    @dispatch(Number)
    def listen(self, frequency, threshold=DEFAULT_THRESHOLD, blocksize=DEFAULT_BLOCKSIZE):
        raw_data = self.fetch_microphone(blocksize)
        data = np.array([val[0] for val in raw_data])
        base_fn = np.cos(2 * np.pi * frequency * np.arange(blocksize) / self._modulator._sampling_frequency)
        return abs(np.dot(data, base_fn)) ** 2 > threshold
        # return np.log(abs(np.dot(data, base_fn))) > threshold
        # return data.shape, base_fn.shape

    @dispatch(object)
    def listen(self, frequencies, threshold=DEFAULT_THRESHOLD, blocksize=DEFAULT_BLOCKSIZE):
        data = self.fetch_microphone(blocksize)
