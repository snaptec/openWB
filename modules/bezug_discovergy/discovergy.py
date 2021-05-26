#!/usr/bin/python3
import json
import sys
import urllib.request
import urllib.parse
import base64
from datetime import datetime

RAMDISK_PATH = "/var/www/html/openWB/ramdisk/"


def log(msg: str):
    with open("/var/log/openWB.log", "a") as fd:
        fd.write("%s: Discovergy: %s\n" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg))


def write_to_ramdisk_file(filename: str, content: str):
    with open(RAMDISK_PATH + filename, 'w') as f:
        f.write(content)
        f.write("\n")


def write_float_to_ramdisk_file(filename: str, content: float):
    write_to_ramdisk_file(filename, str(round(content)))


def get_last_reading(user: str, password: str, meter_id: str):
    try:
        return try_get_last_reading(user, password, meter_id)
    except Exception as e:
        log("Getting last readings failed: " + str(e))
        raise e


def try_get_last_reading(user: str, password: str, meter_id: str):
    request = urllib.request.Request(
        "https://api.discovergy.com/public/v1/last_reading?" + urllib.parse.urlencode({"meterId": meter_id}))
    request.add_header("Authorization",
                       "Basic " + base64.b64encode(bytes("%s:%s" % (user, password), "utf-8")).decode("utf-8"))
    return json.loads(str(urllib.request.urlopen(request, timeout=3).read().decode("utf-8")))


def write_readings_to_ramdisk(discovergy: dict):
    values = discovergy["values"]
    write_float_to_ramdisk_file("wattbezug", values["power"] / 1000)
    write_float_to_ramdisk_file("einspeisungkwh", values["energyOut"] / 10000000)
    write_float_to_ramdisk_file("bezugkwh", values["energy"] / 10000000)

    for phase in range(1, 4):
        str_phase = str(phase)
        voltage = values["voltage" + str_phase] / 1000
        power = values["power" + str_phase] / 1000
        current = power / (voltage if voltage > 150 else 230)
        write_float_to_ramdisk_file("evuv" + str_phase, voltage)
        write_float_to_ramdisk_file("bezugw" + str_phase, power)
        write_float_to_ramdisk_file("bezuga" + str_phase, current)


def update(user: str, password: str, meter_id: str):
    write_readings_to_ramdisk(get_last_reading(user, password, meter_id))


if __name__ == '__main__':
    update(sys.argv[1], sys.argv[2], sys.argv[3])
