import argparse
import importlib
from wcomm import WCOMM_CONFIG

parser = argparse.ArgumentParser(description="Run the WComm package.")
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

if args.example_name is not None:
    example = importlib.import_module(
        f"wcomm.examples.{args.example_name}.main")
    example.main()
