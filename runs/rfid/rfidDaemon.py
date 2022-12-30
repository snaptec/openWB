#!/usr/bin/env python3
import os
import time
import traceback

basePath = "/var/www/html/openWB"
ramdiskPath = basePath + "/ramdisk"
logFilename = ramdiskPath + "/rfid.log"

loglevel = 1
counter = 0
null_tag_value = "0"
rfid_list = []
Values = {
    'newplugstatlp1': str(0),
    'newplugstatlp2': str(0),
    'newplugstatlp3': str(0),
    'newplugstatlp4': str(0),
    'newplugstatlp5': str(0),
    'newplugstatlp6': str(0),
    'newplugstatlp7': str(0),
    'newplugstatlp8': str(0),
    'oldplugstatlp1': str(0),
    'oldplugstatlp2': str(0),
    'oldplugstatlp3': str(0),
    'oldplugstatlp4': str(0),
    'oldplugstatlp5': str(0),
    'oldplugstatlp6': str(0),
    'oldplugstatlp7': str(0),
    'oldplugstatlp8': str(0),
    'lastpluggedlp': str(0),
    'lastscannedtag': str(0),
    'rfidlasttag': str(0)
}


# handling of all logging statements
def log_debug(level: int, msg: str, traceback_str: str = None) -> None:
    if level >= loglevel:
        with open(logFilename, 'a') as log_file:
            log_file.write(time.ctime() + ': ' + msg + '\n')
            if traceback_str is not None:
                log_file.write(traceback_str + '\n')


# write value to file in ramdisk
def write_to_ramdisk(filename: str, content: str) -> None:
    with open(ramdiskPath + "/" + filename, "w") as file:
        file.write(content)


# read value from file in ramdisk
def read_from_ramdisk(filename: str) -> str:
    try:
        with open(ramdiskPath + "/" + filename, 'r') as file:
            return file.read()
    except FileNotFoundError:
        log_debug(2, "Error reading file '" + filename + "' from ramdisk!", traceback.format_exc())
        return ""


def read_rfid_list():
    global rfid_list
    try:
        rfid_list = read_from_ramdisk("rfidlist").rstrip().split(",")
        log_debug(0, "Liste gültiger RFIDs aktualisiert: " + str(rfid_list))
    except FileNotFoundError:
        log_debug(2, "Konnte Liste gültiger RFIDs nicht lesen!")
        rfid_list = []


def get_plug_state():
    for chargepoint in range(1, 9):
        if chargepoint == 1:
            ramdisk_file = "plugstat"
        elif chargepoint == 2:
            ramdisk_file = "plugstats1"
        else:
            ramdisk_file = "plugstatlp" + str(chargepoint)
        try:
            Values.update({"newplugstatlp" + str(chargepoint): int(read_from_ramdisk(ramdisk_file))})
            if (Values["oldplugstatlp" + str(chargepoint)] != Values["newplugstatlp" + str(chargepoint)]):
                if (Values["newplugstatlp" + str(chargepoint)] == 1):
                    Values.update({'lastpluggedlp': str(chargepoint)})
                    log_debug(1, "Angesteckt an LP" + str(chargepoint))
                else:
                    log_debug(1, "Abgesteckt, Sperre LP" + str(chargepoint))
                    write_to_ramdisk("lp" + str(chargepoint) + "enabled", "0")
                Values.update({"oldplugstatlp" + str(chargepoint): Values["newplugstatlp" + str(chargepoint)]})
        except (FileNotFoundError, ValueError):
            pass
    log_debug(0, "plug state: " + str(Values["newplugstatlp1"]) + str(Values["newplugstatlp2"]) +
              str(Values["newplugstatlp3"]) + str(Values["newplugstatlp4"]) + str(Values["newplugstatlp5"]) +
              str(Values["newplugstatlp6"]) + str(Values["newplugstatlp7"]) + str(Values["newplugstatlp8"]))


def conditions():
    if (Values["lastpluggedlp"] != "0"):
        log_debug(0, str(Values["lastpluggedlp"]) + "prüfe auf rfid scan")
        try:
            Values.update({'lastscannedtag': str(read_from_ramdisk("readtag").rstrip())})
            if (Values["lastscannedtag"] != null_tag_value):
                for tag in rfid_list:
                    if (str(tag) == str(Values["lastscannedtag"])):
                        log_debug(1, "Schalte Ladepunkt: " + str(Values["lastpluggedlp"]) + " frei")
                        write_to_ramdisk("lp" + str(Values["lastpluggedlp"]) + "enabled", "1")
                        write_to_ramdisk("rfidlp" + str(Values["lastpluggedlp"]), str(Values["lastscannedtag"]))
                        log_debug(1, "Schreibe Tag: " + str(Values["lastscannedtag"]) + " zu Ladepunkt")
                        Values.update({'lastpluggedlp': "0"})
                        write_to_ramdisk("readtag", null_tag_value)
        except Exception as e:
            log_debug(1, str(e))
            pass


def save_last_rfid_tag():
    read_tag = read_from_ramdisk("readtag").rstrip()
    if ((read_tag != Values["rfidlasttag"]) and (read_tag != "0")):
        log_debug(1, "save_last_rfid_tag: change detected, updating ramdisk: " + str(read_tag))
        write_to_ramdisk("rfidlasttag", read_tag + "," + str(os.path.getmtime(ramdiskPath + "/readtag")))
        Values.update({'rfidlasttag': read_tag})


def clear_old_rfid_tag():
    null_tag = False
    null_tag = bool(str(read_from_ramdisk("readtag").rstrip()) == null_tag_value)
    if null_tag is False:
        t = os.path.getmtime(ramdiskPath + '/readtag')
        time_diff = time.time() - t
        if time_diff > 300:
            log_debug(1, "Verwerfe Tag nach " + str(time_diff) + " Sekunden")
            write_to_ramdisk("readtag", null_tag_value)


while True:
    if counter == 0:
        read_rfid_list()
    get_plug_state()
    conditions()
    save_last_rfid_tag()
    clear_old_rfid_tag()
    counter = (counter + 1) % 10
    time.sleep(2)
