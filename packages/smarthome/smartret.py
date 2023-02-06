import json


def writeret(jsonstr: str, devicenumber: int) -> None:
    fname = '/var/www/html/openWB/ramdisk/smarthome_device_ret'
    fname += str(devicenumber)
    with open(fname, 'w') as f1:
        json.dump(jsonstr, f1)
