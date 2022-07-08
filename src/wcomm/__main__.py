import argparse
import importlib
from wcomm import WCOMM_CONFIG
from wcomm import modulation, channels
from wcomm.bin import receiver, transmitter
from wcomm.encoding import channel, source

parser = argparse.ArgumentParser(description="Run the WComm package.")

parser.add_argument(
    "-T", "--transmitter",
    dest="transmitter_filename",
    help="Run the transmitter application with the given configuration.",
)

parser.add_argument(
    "-R", "--receiver",
    dest="receiver_filename",
    help="Run the receiver application with the given configuration.",
)

parser.add_argument(
    "-I", "--is-image",
    dest="is_image",
    action="store_true",
    help="Specify whether to treat the given file as an image or binaries.",
)

parser.add_argument(
    "--image-channel",
    dest="image_channel",
    default=0,
    help="Channel of the image to read.",
)

parser.add_argument(
    "-m", "--modulation",
    dest="modulation_type",
    default="FSK16",
    help="Specify the type of modulation used.",
)

parser.add_argument(
    "-c", "--channel",
    dest="channel_type",
    default="SoundChannel",
    help="Specify the channel type.",
)

parser.add_argument(
    "-s", "--source-coding",
    dest="source_coding_type",
    default="HuffmanCode",
    help="Specify the type of source coding used.",
)

parser.add_argument(
    "-S", "--source-coding-filename",
    dest="source_coding_filename",
    help="Specify the filename of the premade code used for the source coding.",
)

parser.add_argument(
    "-t", "--time",
    dest="period",
    default=100,
    help="Specify the time (ms) that each emission should take.",
)

parser.add_argument(
    "-e", "--example",
    dest="example_name",
    help="Run an example.",
)

parser.add_argument(
    "-v", "--verbose",
    dest="verbose",
    action="store_true",
    help="Run in verbose mode.",
)

args = parser.parse_args()

if args.verbose:
    WCOMM_CONFIG["verbose"] = True

if args.transmitter_filename is not None:
    transmitter.main(
        filename=args.transmitter_filename,
        modulation=getattr(modulation, args.modulation_type),
        source=getattr(source, args.source_coding_type),
        source_template=args.source_coding_filename,
        channel_type=getattr(channels, args.channel_type),
        period=int(args.period),
        is_image=args.is_image,
        image_channel=int(args.image_channel),
    )

elif args.receiver_filename is not None:
    receiver.main(filename=args.receiver_filename)

elif args.example_name is not None:
    example = importlib.import_module(
        f"wcomm.examples.{args.example_name}.main")
    example.main()
