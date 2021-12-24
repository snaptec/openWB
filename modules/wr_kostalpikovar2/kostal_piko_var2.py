# initially created by Stefan Schefler for openWB 2019
# modified by Kevin Wieland
# modified by Lena Kuemmel
# based on Homematic Script v0.2 (c) 2018 by Alchy

#!/usr/bin/env python3

from datetime import datetime, timezone
import os
import re
import requests
import sys

Debug = int(os.environ.get('debug'))
myPid = str(os.getpid())

num = int(sys.argv[1])
wr_piko2_url = str(sys.argv[2])
wr_piko2_user = str(sys.argv[3])
wr_piko2_pass = str(sys.argv[4])


def DebugLog(message):
    local_time = datetime.now(timezone.utc).astimezone()
    print(local_time.strftime(format="%Y-%m-%d %H:%M:%S") + ": PID: " + myPid + ": " + message)


if Debug >= 2:
    DebugLog('Wechselrichter Kostal Piko Var 2 User: ' + wr_piko2_user)
    DebugLog('Wechselrichter Kostal Piko Var 2 Passwort: ' + wr_piko2_pass)
    DebugLog('Wechselrichter Kostal Piko Var 2 URL: ' + wr_piko2_url)

if num == 1:
    file_ext = ""
elif num == 2:
    file_ext = "2"
else:
    raise Exception("unbekannte Modul-ID")

# Daten einlesen
response = requests.get(wr_piko2_url, verify=False, auth=(wr_piko2_user, wr_piko2_pass), timeout=10)
# request html, concat to one line, remove spaces, add spaces before color changes (#)
response.encoding = 'utf-8'
HTML = response.text
HTML = HTML.replace("\r", "")
HTML = HTML.replace("\n", "")
HTML = HTML.replace(" ", "")
HTML = HTML.replace("#", " ")

if HTML != "":             # check if valid content of request
    counter = 0
    for LINE in HTML:         # parse all html lines
        if re.search("FFFFFF", LINE) != None:   # search for white background color
            counter = counter + 1
            # PART2=${LINE##*F\">}   # strip before number
            # VALUE=${PART2%%<*}   # strip after number
            VALUE = re.search('^[0-9]+.?[0-9]*$', LINE).group()

            if counter == 1:   # pvwatt
                if VALUE == "xxx":    # off-value equals zero
                    VALUE = "0"
                regex = '^[-+]?[0-9]+.?[0-9]*$'
                if re.search(regex, VALUE) == None:   # check for valid number
                    with open("/var/www/html/openWB/ramdisk/pv"+file_ext+"watt", "r") as f:
                        VALUE = f.read()
                if Debug >= 1:
                    DebugLog('WR Leistung: ' + str(VALUE*-1))
                with open("/var/www/html/openWB/ramdisk/pv"+file_ext+"watt", "w") as f:
                    f.write(str(VALUE*-1))
            elif counter == 2:   # pvkwhk
                if Debug >= 1:
                    DebugLog('WR Energie: ' + str(VALUE))
                with open("/var/www/html/openWB/ramdisk/pv"+file_ext+"kwhk", "w") as f:
                    f.write(str(VALUE))
                if num == 1:
                    with open("/var/www/html/openWB/ramdisk/pv"+file_ext+"kwh", "w") as f:
                        f.write(str(VALUE*1000))

exit(0)
