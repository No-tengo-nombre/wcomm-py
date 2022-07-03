from wcomm.channels.sound import SoundChannel
from wcomm.modulation.mfsk import FSK256
from wcomm.message import Message


def main():
    mod_type = FSK256()
    channel = SoundChannel(mod_type)

    message = Message("Hello world!")

    channel.send(message, 10)
    channel.send('a', 200)
    channel.play(13100, 2000)


if __name__ == "__main__":
    main()
