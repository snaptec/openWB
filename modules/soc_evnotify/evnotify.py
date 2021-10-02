import sys
from datetime import datetime
import requests

RAMDISK_PATH = "/var/www/html/openWB/ramdisk/"
debuglevel = 2


def log(level: int, msg: str):
    if debuglevel >= level:
        with open(RAMDISK_PATH + "soc.log", "a") as fd:
            fd.write("%s: EVNotify: %s\n" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg))


def write_to_ramdisk_file(filename: str, content: str):
    with open(RAMDISK_PATH + filename, 'w') as f:
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


def chargepoint_number_to_string(chargepoint: str):
    if chargepoint == "1":
        return ""
    else:
        return chargepoint


def refresh_soc(akey: str, token: str, chargepoint: str):
    try:
        soc = load_evnotify_soc(akey, token)
    except Exception as e:
        log(0, "Lp%s: Failed to retrieve SoC: %s" % (chargepoint, e))
        return

    log(1, "Lp%s: SoC from Server: %d" % (chargepoint, soc))
    if soc >= 100:
        write_float_to_ramdisk_file("soc" + chargepoint_number_to_string(chargepoint), soc)
    else:
        log(0, "Lp%s: SoC=%f is invalid!" % (chargepoint, soc))


if __name__ == '__main__':
    debuglevelArg = sys.argv[4]
    if debuglevelArg.isdigit():
        debuglevel = int(debuglevelArg)

    refresh_soc(sys.argv[1], sys.argv[2], sys.argv[3])
