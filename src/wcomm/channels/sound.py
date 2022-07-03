import sounddevice as sd
import numpy as np
from time import sleep
from wcomm.channel import Channel
from wcomm.utils.log import log
import winsound
from tones import SINE_WAVE
from tones.mixer import Mixer
from pysinewave import SineWave
from multipledispatch import dispatch
from numbers import Number

import pyaudio




class ToneGenerator(object):
 
    def __init__(self, samplerate=44100, frames_per_buffer=220):
        self.p = pyaudio.PyAudio()
        self.samplerate = samplerate
        self.frames_per_buffer = frames_per_buffer
        self.streamOpen = False
 
    def sinewave(self):
        if self.buffer_offset + self.frames_per_buffer - 1 > self.x_max:
            # We don't need a full buffer or audio so pad the end with 0's
            xs = np.arange(self.buffer_offset,
                              self.x_max)
            tmp = self.amplitude * np.sin(xs * self.omega)
            out = np.append(tmp,
                               np.zeros(self.frames_per_buffer - len(tmp)))
        else:
            xs = np.arange(self.buffer_offset,
                              self.buffer_offset + self.frames_per_buffer)
            out = self.amplitude * np.sin(xs * self.omega)
        self.buffer_offset += self.frames_per_buffer
        return out
 
    def callback(self, in_data, frame_count, time_info, status):
        if self.buffer_offset < self.x_max:
            data = self.sinewave().astype(np.float32)
            return (data.tostring(), pyaudio.paContinue)
        else:
            return (None, pyaudio.paComplete)
 
    def is_playing(self):
        if self.stream.is_active():
            return True
        else:
            if self.streamOpen:
                self.stream.stop_stream()
                self.stream.close()
                self.streamOpen = False
            return False
 
    def play(self, frequency, duration, amplitude):
        self.omega = float(frequency) * (np.pi * 2) / self.samplerate
        self.amplitude = amplitude
        self.buffer_offset = 0
        self.streamOpen = True
        self.x_max = np.ceil(self.samplerate * duration) - 1
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=self.samplerate,
                                  output=True,
                                  frames_per_buffer=self.frames_per_buffer,
                                  stream_callback=self.callback)




DEFAULT_BLOCKSIZE = 441
DEFAULT_THRESHOLD = 20
DEFAULT_SOUND_TIME = 1000
sine = None
mixer = Mixer(44100, 1)
mixer.create_track(0, SINE_WAVE)
generator = ToneGenerator()


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

        # set_sine_freq(frequency)
        # sleep(time / 1000)

        generator.play(frequency, time / 1000, 1)
        while generator.is_playing():
            pass

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
        return abs(np.dot(data, base_fn)) > threshold
        # return np.log(abs(np.dot(data, base_fn))) > threshold
        # return data.shape, base_fn.shape

    @dispatch(object)
    def listen(self, frequencies, threshold=DEFAULT_THRESHOLD, blocksize=DEFAULT_BLOCKSIZE):
        data = self.fetch_microphone(blocksize)
