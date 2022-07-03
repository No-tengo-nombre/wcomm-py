from wcomm import WCOMM_CONFIG


def log(message):
    if WCOMM_CONFIG["verbose"]:
        print(message)
