import sys
from os.path import dirname, realpath, join

import requests

sys.path.append(join(dirname(dirname(dirname(realpath(__file__)))), "lib"))
from openwb.config import RAMDISK_PATH, Config
from openwb.logger import Logger, LogFile

logger = Logger(LogFile.EVSOC, "EVNotify")
config = Config()


def write_to_ramdisk_file(filename: str, content: str):
    with open(join(RAMDISK_PATH, filename), 'w') as f:
        f.write(content)
        f.write("\n")


def write_float_to_ramdisk_file(filename: str, content: float):
    write_to_ramdisk_file(filename, str(round(content)))


def load_evnotify_soc(akey: str, token: str):
    response = requests.get("https://app.evnotify.de/soc", params={"akey": akey, "token": token})
    response.raise_for_status()
    json = response.json()
    if "soc_display" in json and isinstance(json["soc_display"], (int, float)):
        return json["soc_display"]
    raise Exception("Expected response with number property soc_display. Got: " + response.text)


def refresh_soc(akey: str, token: str, chargepoint: str):
    try:
        soc = load_evnotify_soc(akey, token)
    except Exception as e:
        logger.info(f"Lp{chargepoint}: Failed to retrieve SoC: {e}")
        return

    logger.debug(f"Lp{chargepoint}: SoC from Server: {soc}")
    if soc <= 100:
        write_float_to_ramdisk_file("soc" if chargepoint == "1" else "soc1", soc)
    else:
        logger.info(f"Lp{chargepoint}: SoC={soc} is invalid!")


if __name__ == '__main__':
    chargePointName = "lp2" if sys.argv[1] == "2" else ""
    refresh_soc(config["evnotifyakey" + chargePointName], config["evnotifytoken" + chargePointName], sys.argv[1])
