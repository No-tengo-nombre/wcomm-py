from wcomm.channel import Channel
from wcomm.utils.log import log
from wcomm.utils.audio import play_tone


DEFAULT_SOUND_TIME = 1000


class SoundChannel(Channel):
    def __init__(self, modulator):
        log(f"SETTING MODULATION -> {modulator.get_name()}")
        self._modulator = modulator

    def send(self, message, time=DEFAULT_SOUND_TIME):
        log(f"SEND MESSAGE {message}")
        self._modulator.send_through_channel(self, message, time)

    def play(self, frequency, time=DEFAULT_SOUND_TIME):
        log(f"PLAY {frequency} Hz , {time} ms\n")
        play_tone(frequency, time)
