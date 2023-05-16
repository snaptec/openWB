#!/usr/bin/python3
import os
import sys

from modules.common.evse import Evse
from modules.common.modbus import ModbusSerialClient_

seradd = str(sys.argv[1])
evseid = int(sys.argv[2])
lla = int(sys.argv[3])


RAMDSIK_PATH = "/var/www/html/openWB/ramdisk/"
EVSE_CONFIGURED_FILE = RAMDSIK_PATH+"evse_configured_"+str(seradd[-4:])+"_"+str(evseid)

evse = Evse(evseid, ModbusSerialClient_(seradd))

if os.path.isfile(EVSE_CONFIGURED_FILE) is False:
    evse.deactivate_precise_current()
    with open(EVSE_CONFIGURED_FILE, 'w+') as f:
        f.write("1")

rq = evse.set_current(lla)
