#!/usr/bin/python3
from pathlib import Path
import sys
from pymodbus.client.sync import ModbusSerialClient

from modules.common.evse import Evse

seradd = str(sys.argv[1])
evseid = int(sys.argv[2])
lla = int(sys.argv[3])

RAMDSIK_PATH = Path(__file__).resolve().parents[1] / "ramdisk"
EVSE_CONFIGURED_FILE = RAMDSIK_PATH+"evse_configured_"+str(seradd)+"_"+str(evseid)

client = ModbusSerialClient(method="rtu", port=seradd, baudrate=9600, stopbits=1, bytesize=8, timeout=1)

if Path.is_file(EVSE_CONFIGURED_FILE) is False:
    Evse(client, evseid).deactivate_precise_current()
    with open(EVSE_CONFIGURED_FILE, 'w') as f:
        f.write("1")

rq = client.write_registers(1000, lla, unit=evseid)
