#!/usr/bin/python3
import os
import sys

from modules.common.evse import Evse
from modules.common.modbus import ModbusSerialClient_

evseid = int(sys.argv[2])
lla = int(sys.argv[3])


def detect_modbus_usb_port():
    """guess USB/modbus device name"""
    known_devices = ("/dev/ttyUSB0", "/dev/ttyACM0", "/dev/serial0")
    for device in known_devices:
        try:
            with open(device):
                return device
        except Exception:
            pass
    return known_devices[-1]  # this does not make sense, but is the same behavior as the old code


serial_port = detect_modbus_usb_port()

RAMDSIK_PATH = "/var/www/html/openWB/ramdisk/"
EVSE_CONFIGURED_FILE = RAMDSIK_PATH+"evse_configured_"+str(serial_port[-4:])+"_"+str(evseid)

evse = Evse(evseid, ModbusSerialClient_(serial_port))

if os.path.isfile(EVSE_CONFIGURED_FILE) is False:
    evse.deactivate_precise_current()
    with open(EVSE_CONFIGURED_FILE, 'w+') as f:
        f.write("1")

rq = evse.set_current(lla)
