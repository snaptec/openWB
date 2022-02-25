#!/usr/bin/python3
import os
import sys
from bezug_rct2 import rct_lib
from typing import List
#
# Author Heinz Hoefling
# Version 1.0 Okt.2021
# Fragt die Werte gebuendelt ab,
#


def writeRam(fn, val, rctname):
    fnn = "/var/www/html/openWB/ramdisk/"+str(fn)
    if rct_lib.bVerbose == True:
        f = open(fnn, 'r')
        oldv = f.read()
        f.close()
        rct_lib.dbglog("field " + str(fnn) + " val is " + str(val) + " oldval:" + str(oldv) + " " + str(rctname))

    f = open(fnn, 'w')
    f.write(str(val))
    f.close()


# Entry point with parameter check
def main(argv: List[str]):
    rct_lib.init(argv)

    clientsocket = rct_lib.connect_to_server()
    if clientsocket is not None:

        socx = rct_lib.read(clientsocket, 0x959930BF)
        soc = int(socx * 100.0)
        writeRam('speichersoc', soc, '0x959930BF battery.soc')

        watt = int(rct_lib.read(clientsocket, 0x400F015B) * -1.0)
        writeRam('speicherleistung', watt, '0x400F015B g_sync.p_acc_lp')

        watt = int(rct_lib.read(clientsocket, 0x5570401B))
        #rct_lib.dbglog("speicherikwh will be battery.stored_energy "+ str(watt))
        writeRam('speicherikwh', watt, '0x5570401B battery.stored_energy')

        watt = int(rct_lib.read(clientsocket, 0xA9033880))
        #rct_lib.dbglog("speicherekwh will be battery.used_energy "+ str(watt))
        writeRam('speicherekwh', watt, '#0xA9033880 battery.used_energy')

        stat1 = int(rct_lib.read(clientsocket, 0x70A2AF4F))
        rct_lib.dbglog("battery.bat_status " + str(stat1))

        stat2 = int(rct_lib.read(clientsocket, 0x71765BD8))
        rct_lib.dbglog("battery.status " + str(stat2))

        stat3 = int(rct_lib.read(clientsocket, 0x0DE3D20D))
        rct_lib.dbglog("battery.status2 " + str(stat3))

        faultStr = ''
        faultState = 0

        if (stat1 + stat2 + stat3) > 0:
            faultStr = "Battery ALARM Battery-Status nicht 0"
            faultState = 2
            # speicher in mqtt

        os.system('mosquitto_pub -r -t openWB/housebattery/faultState -m "' + str(faultState) + '"')
        os.system('mosquitto_pub -r -t openWB/housebattery/faultStr -m "' + str(faultStr) + '"')

        socsoll = int(rct_lib.read(clientsocket, 0x8B9FF008) * 100.0)
        os.system('mosquitto_pub -r -t openWB/housebattery/soctarget -m "' + str(socsoll) + '"')

        rct_lib.close(clientsocket)
    sys.exit(0)
