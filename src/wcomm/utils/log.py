from wcomm import WCOMM_CONFIG
from quantiphy import Quantity


def log(message):
    if WCOMM_CONFIG["verbose"]:
        print(message)


def metric_prefix(quantity, prefix):
    return str(Quantity(quantity, prefix))
