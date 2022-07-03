import argparse
import importlib

parser = argparse.ArgumentParser(description="Run the WComm package.")
parser.add_argument(
    "-e", "--example",
    dest="example_name",
    help="Run an example.",
)

args = parser.parse_args()

if args.example_name is not None:
    example = importlib.import_module(
        f"wcomm.examples.{args.example_name}.main")
    example.main()
