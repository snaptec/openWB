#!/usr/bin/python
import os
import time

os.chdir('/var/www/html/openWB/')
loglevel = 1
counter = 0
rfidlist = []
Values = {}
Values.update({'newplugstatlp1': str(0)})
Values.update({'newplugstatlp2': str(0)})
Values.update({'newplugstatlp3': str(0)})
Values.update({'newplugstatlp4': str(0)})
Values.update({'newplugstatlp5': str(0)})
Values.update({'newplugstatlp6': str(0)})
Values.update({'newplugstatlp7': str(0)})
Values.update({'newplugstatlp8': str(0)})
Values.update({'oldplugstatlp1': str(0)})
Values.update({'oldplugstatlp2': str(0)})
Values.update({'oldplugstatlp3': str(0)})
Values.update({'oldplugstatlp4': str(0)})
Values.update({'oldplugstatlp5': str(0)})
Values.update({'oldplugstatlp6': str(0)})
Values.update({'oldplugstatlp7': str(0)})
Values.update({'oldplugstatlp8': str(0)})
Values.update({'lastpluggedlp': str(0)})
Values.update({'lastscannedtag': str(0)})
Values.update({'rfidlasttag': str(0)})


def log_debug(level: int, msg: str):
    if level >= loglevel:
        with open('ramdisk/rfid.log', 'a') as file:
            file.write(time.ctime() + ': ' + msg + '\n')


def read_rfid_list():
    global rfidlist
    try:
        with open('ramdisk/rfidlist', 'r') as value:
            rfidlist = str(value.read()).rstrip().split(",")
            log_debug(0, "Liste gültiger RFIDs aktualisiert: " + str(rfidlist))
    except FileNotFoundError:
        log_debug(2, "Konnte Liste gültiger RFIDs nicht lesen!")
        rfidlist = []


def get_plugstat():
    try:
        with open('ramdisk/plugstat', 'r') as value:
            Values.update({'newplugstatlp1': int(value.read())})
        if (Values["oldplugstatlp1"] != Values["newplugstatlp1"]):
            if (Values["newplugstatlp1"] == 1):
                Values.update({'lastpluggedlp': str(1)})
                log_debug(1, "Angesteckt an LP1")
            else:
                log_debug(1, "Abgesteckt, Sperre LP1")
                with open('ramdisk/lp1enabled', 'w') as file:
                    file.write(str("0"))
            Values.update({"oldplugstatlp1": Values["newplugstatlp1"]})
    except (FileNotFoundError, ValueError):
        pass
    try:
        with open('ramdisk/plugstats1', 'r') as value:
            Values.update({'newplugstatlp2': int(value.read())})
        if (Values["oldplugstatlp2"] != Values["newplugstatlp2"]):
            if (Values["newplugstatlp2"] == 1):
                Values.update({'lastpluggedlp': str(2)})
                log_debug(1, "Angesteckt an LP2")
            else:
                log_debug(1, "Abgesteckt, Sperre LP2")
                with open('ramdisk/lp2enabled', 'w') as file:
                    file.write(str("0"))
            Values.update({"oldplugstatlp2": Values["newplugstatlp2"]})
    except (FileNotFoundError, ValueError):
        pass
    try:
        with open('ramdisk/plugstatlp3', 'r') as value:
            Values.update({'newplugstatlp3': int(value.read())})
        if (Values["oldplugstatlp3"] != Values["newplugstatlp3"]):
            if (Values["newplugstatlp3"] == 1):
                Values.update({'lastpluggedlp': str(3)})
                log_debug(1, "Angesteckt an LP3")
            else:
                log_debug(1, "Abgesteckt, Sperre LP3")
                with open('ramdisk/lp3enabled', 'w') as file:
                    file.write(str("0"))
            Values.update({"oldplugstatlp3": Values["newplugstatlp3"]})
    except (FileNotFoundError, ValueError):
        pass
    try:
        with open('ramdisk/plugstatlp4', 'r') as value:
            Values.update({'newplugstatlp4': int(value.read())})
        if (Values["oldplugstatlp4"] != Values["newplugstatlp4"]):
            if (Values["newplugstatlp4"] == 1):
                Values.update({'lastpluggedlp': str(4)})
                log_debug(1, "Angesteckt an LP4")
            else:
                log_debug(1, "Abgesteckt, Sperre LP4")
                with open('ramdisk/lp4enabled', 'w') as file:
                    file.write(str("0"))
            Values.update({"oldplugstatlp4": Values["newplugstatlp4"]})
    except (FileNotFoundError, ValueError):
        pass
    try:
        with open('ramdisk/plugstatlp5', 'r') as value:
            Values.update({'newplugstatlp5': int(value.read())})
        if (Values["oldplugstatlp5"] != Values["newplugstatlp5"]):
            if (Values["newplugstatlp5"] == 1):
                Values.update({'lastpluggedlp': str(5)})
                log_debug(1, "Angesteckt an LP5")
            else:
                log_debug(1, "Abgesteckt, Sperre LP5")
                with open('ramdisk/lp5enabled', 'w') as file:
                    file.write(str("0"))
            Values.update({"oldplugstatlp5": Values["newplugstatlp5"]})
    except (FileNotFoundError, ValueError):
        pass
    try:
        with open('ramdisk/plugstatlp6', 'r') as value:
            Values.update({'newplugstatlp6': int(value.read())})
        if (Values["oldplugstatlp6"] != Values["newplugstatlp6"]):
            if (Values["newplugstatlp6"] == 1):
                Values.update({'lastpluggedlp': str(6)})
                log_debug(1, "Angesteckt an LP6")
            else:
                log_debug(1, "Abgesteckt, Sperre LP6")
                with open('ramdisk/lp6enabled', 'w') as file:
                    file.write(str("0"))
            Values.update({"oldplugstatlp6": Values["newplugstatlp6"]})
    except (FileNotFoundError, ValueError):
        pass
    try:
        with open('ramdisk/plugstatlp7', 'r') as value:
            Values.update({'newplugstatlp7': int(value.read())})
        if (Values["oldplugstatlp7"] != Values["newplugstatlp7"]):
            if (Values["newplugstatlp7"] == 1):
                Values.update({'lastpluggedlp': str(7)})
                log_debug(1, "Angesteckt an LP7")
            else:
                log_debug(1, "Abgesteckt, Sperre LP7")
                with open('ramdisk/lp7enabled', 'w') as file:
                    file.write(str("0"))
            Values.update({"oldplugstatlp7": Values["newplugstatlp7"]})
    except (FileNotFoundError, ValueError):
        pass
    try:
        with open('ramdisk/plugstatlp8', 'r') as value:
            Values.update({'newplugstatlp8': int(value.read())})
        if (Values["oldplugstatlp8"] != Values["newplugstatlp8"]):
            if (Values["newplugstatlp8"] == 1):
                Values.update({'lastpluggedlp': str(8)})
                log_debug(1, "Angesteckt an LP8")
            else:
                log_debug(1, "Abgesteckt, Sperre LP8")
                with open('ramdisk/lp8enabled', 'w') as file:
                    file.write(str("0"))
            Values.update({"oldplugstatlp8": Values["newplugstatlp8"]})
    except (FileNotFoundError, ValueError):
        pass
    log_debug(0, "Plugstat: " + str(Values["newplugstatlp1"]) + str(Values["newplugstatlp2"]) +
              str(Values["newplugstatlp3"]) + str(Values["newplugstatlp4"]) + str(Values["newplugstatlp5"]) +
              str(Values["newplugstatlp6"]) + str(Values["newplugstatlp7"]) + str(Values["newplugstatlp8"]))


def conditions():
    if (Values["lastpluggedlp"] != "0"):
        log_debug(0, str(Values["lastpluggedlp"]) + "prüfe auf rfid scan")
        try:
            with open('ramdisk/readtag', 'r') as value:
                Values.update({'lastscannedtag': str(value.read().rstrip())})
            if (Values["lastscannedtag"] != "0"):
                for tag in rfidlist:
                    if (str(tag) == str(Values["lastscannedtag"])):
                        log_debug(1, "Schalte Ladepunkt: " + str(Values["lastpluggedlp"]) + " frei")
                        with open('ramdisk/lp'+str(Values["lastpluggedlp"])+'enabled', 'w') as file:
                            file.write(str("1"))
                        with open('ramdisk/rfidlp' + str(Values["lastpluggedlp"]), 'w') as file:
                            file.write(str(Values["lastscannedtag"]))
                        log_debug(1, "Schreibe Tag: " + str(Values["lastscannedtag"]) + " zu Ladepunkt")
                        Values.update({'lastpluggedlp': "0"})
                        with open('ramdisk/readtag', 'w') as file:
                            file.write("0")
        except Exception as e:
            log_debug(1, str(e))
            pass


def save_last_rfidtag():
    with open('ramdisk/readtag', 'r') as readtagfile:
        readtag = str(readtagfile.read().rstrip())
    if ((readtag != Values["rfidlasttag"]) and (readtag != "0")):
        log_debug(1, "savelastrfidtag: change detected, updating ramdisk: " + str(readtag))
        with open('ramdisk/rfidlasttag', 'w') as file:
            file.write(readtag + "," + str(os.path.getmtime('ramdisk/readtag')))
        Values.update({'rfidlasttag': readtag})


def clear_old_rfidtag():
    null_tag_value = "0"
    null_tag = False
    with open('ramdisk/readtag', 'r') as readtagfile:
        null_tag = bool(str(readtagfile.read().rstrip()) == null_tag_value)
    if null_tag is False:
        t = os.path.getmtime('ramdisk/readtag')
        timediff = time.time() - t
        if timediff > 300:
            log_debug(1, "Verwerfe Tag nach " + str(timediff) + " Sekunden")
            with open('ramdisk/readtag', 'w') as file:
                file.write(null_tag_value)


while True:
    if counter == 0:
        read_rfid_list()
    get_plugstat()
    conditions()
    save_last_rfidtag()
    clear_old_rfidtag()
    counter = (counter + 1) % 10
    time.sleep(2)
