from wcomm.channels.sound import SoundChannel
from wcomm.modulation.mfsk import FSK256
from wcomm.message import Message


def main():
    mod_type = FSK256(100, 30)
    channel = SoundChannel(mod_type)

    message = Message("Hello world!")

    channel.send(message, 100)
    channel.send(Message("a"), 100)


if __name__ == "__main__":
    main()
