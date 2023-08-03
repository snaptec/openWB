#!/usr/bin/python3
from smarthome.smartcommon import mainloop, initparam
import time
import logging
import os
log = logging.getLogger("smarthome")
# openwb 1.9 spec
mqttcg = 'openWB/config/get/SmartHome/'
mqttcs = 'openWB/config/set/SmartHome/'
mqttsdevstat = 'openWB/SmartHome/Devices'
mqttsglobstat = 'openWB/SmartHome/Status/'
mqtttopicdisengageable = 'openWB/SmartHome/Status/wattschalt'
ramdiskwrite = True
mqttport = 1883
#
#  openwb 2.0 spec
#  mqttcg = 'openWB/LegacySmartHome/config/get/'
#  mqttcs = 'openWB/LegacySmartHome/config/set/'
#  mqttsdevstat = 'openWB/LegacySmartHome/Devices'
#  mqttsglobstat = 'openWB/LegacySmartHome/Status/'
#  mqtttopicdisengageable = 'openWB/set/counter/set/disengageable_smarthome_power'
#  ramdiskwrite = False
#  mqttport = 1886
#

bp = '/var/www/html/openWB'


def initlog() -> None:
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    log.setLevel(logging.DEBUG)
    fh = logging.FileHandler(bp+'/ramdisk/smarthome.log', encoding='utf8')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    log.addHandler(fh)


def checkbootdone() -> int:
    try:
        with open(bp+'/ramdisk/bootinprogress', 'r') as value:
            bootinprogress = int(value.read())
    except Exception as e:
        bootinprogress = 1
        log.warning("Ramdisk not set up. Maybe we are still" +
                    "booting (bootinprogress)." + str(e))
        time.sleep(30)
        return 0
    try:
        with open(bp+'/ramdisk/updateinprogress', 'r') as value:
            updateinprogress = int(value.read())
    except Exception as e:
        updateinprogress = 1
        log.warning("Ramdisk not set up. Maybe we are still" +
                    " booting (updateinprogress)." + str(e))
        time.sleep(30)
        return 0
    if (updateinprogress == 1):
        log.warning("Update in progress.")
        time.sleep(30)
        return 0
    if (bootinprogress == 1):
        log.warning("Boot in progress.")
        time.sleep(30)
        return 0
    return 1


# Lese aus der Ramdisk Regelrelevante Werte ein
if __name__ == "__main__":
    initlog()
    log.info("*** Smarthome mq openWB 1.9 Start ***")
    initparam(mqttcg, mqttcs, mqttsdevstat, mqttsglobstat, mqtttopicdisengageable, ramdiskwrite, mqttport)
    while True:
        if (checkbootdone() == 1):
            break
        time.sleep(5)
    while True:
        try:
            with open(bp+'/ramdisk/speichervorhanden', 'r') as value:
                speichervorhanden = int(value.read())
            if (speichervorhanden == 1):
                with open(bp+'/ramdisk/speicherleistung', 'r') as value:
                    speicherleistung = int(float(value.read()))
                with open(bp+'/ramdisk/speichersoc', 'r') as value:
                    speichersoc = int(float(value.read()))
            else:
                speicherleistung = 0
                speichersoc = 100
        except Exception as e:
            log.warning("Fehler beim Auslesen der Ramdisk " +
                        "(speichervorhanden,speicherleistung,speichersoc): " +
                        str(e))
            speichervorhanden = 0
            speicherleistung = 0
            speichersoc = 100
        try:
            with open(bp+'/ramdisk/wattbezug', 'r') as value:
                wattbezug = int(float(value.read())) * -1
        except Exception as e:
            log.warning("Fehler beim Auslesen der Ramdisk (wattbezug):"
                        + str(e))
            wattbezug = 0
        try:
            with open(bp+'/ramdisk/pvallwatt', 'r') as value:
                pvwatt = int(float(value.read())) * -1
        except Exception as e:
            log.warning("Fehler beim Auslesen der Ramdisk (pvallwatt):"
                        + str(e))
            pvwatt = 0
        file_charge = '/var/www/html/openWB/ramdisk/llkombiniert'
        testcharge = 0.0
        try:
            if os.path.isfile(file_charge):
                with open(file_charge, 'r') as f:
                    testcharge = float(f.read())
        except Exception:
            pass
        if testcharge <= 1000:
            chargestatus = False
        else:
            chargestatus = True
        mainloop(wattbezug, speicherleistung, speichersoc, pvwatt, chargestatus)
        time.sleep(5)
