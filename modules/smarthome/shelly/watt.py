#!/usr/bin/python3
import sys
import os
import time
import json
import urllib.request


def totalPowerFromShellyJson(answer, workchan):
    if (workchan == 0):
        if 'meters' in answer:
            meters = answer['meters']   # shelly
        else:
            meters = answer['emeters']  # shellyEM & shelly3EM
        total = 0
        # shellyEM has one meter, shelly3EM has three meters:
        for meter in meters:
            total = total + meter['power']
        return int(total)
    workchan = workchan - 1
    try:
        total = int(answer['meters'][workchan]['power'])   # Abfrage shelly
    except Exception:
        total = int(answer['emeters'][workchan]['power'])  # Abfrage shellyEM
    return int(total)


named_tuple = time.localtime()   # getstruct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S shelly watty.py", named_tuple)
devicenumber = str(sys.argv[1])
ipadr = str(sys.argv[2])
uberschuss = int(sys.argv[3])
try:
    chan = int(sys.argv[4])
except Exception:
    chan = 0
# chan = 0 alle Meter, Kan 0
# chan = 1 meter 1, Kan 0
# chan = 2 meter 2, kan 1
# Setze Default-Werte, andernfalls wird der letzte Wert ewig fortgeschrieben.
# Insbesondere wichtig für aktuelle Leistung
# Zähler wird beim Neustart auf 0 gesetzt, darf daher nicht übergeben werden.
powerc = 0
temp0 = '0.0'
temp1 = '0.0'
temp2 = '0.0'
aktpower = 0
relais = 0
gen = '1'

# test dic
g_dictionary = {"gen": 1}

a_dictionary = {"switch:1": {"id": 0, "source": "init", "output": True,
                             "apower": 93.000, "voltage": 218.794,
                "aenergy": {"total": 4327.45, "minute_ts": 1637430901},
                "temperature": {"tC": 49.1, "tF": 120.3}}}

# test dic ende
# lesen endpoint, gen bestimmem. gen 1 hat unter Umstaenden keinen Eintrag
fbase = '/var/www/html/openWB/ramdisk/smarthome_device_ret.'
fname = fbase + str(ipadr) + '_shelly_info'
fnameg = fbase + str(ipadr) + '_shelly_infog'
if os.path.isfile(fnameg):
    with open(fnameg, 'r') as f:
        gen = str(f.read())
else:
    aread = urllib.request.urlopen("http://" + str(ipadr) + "/shelly",
                                   timeout=3).read().decode("utf-8")
    agen = json.loads(str(aread))
    # agen.update(g_dictionary)
    with open(fname, 'w') as f:
        json.dump(agen, f)
    if 'gen' in agen:
        gen = str(int(agen['gen']))
    with open(fnameg, 'w') as f:
        f.write(str(gen))
# Versuche Daten von Shelly abzurufen.
try:
    if (gen == "1"):
        aread = urllib.request.urlopen("http://"+str(ipadr)+"/status",
                                       timeout=3).read().decode("utf-8")
        answer = json.loads(str(aread))
        # answer.update(a_dictionary)
        # fake new gen
        # gen = '2'
    else:
        aread = urllib.request.urlopen("http://"+str(ipadr) +
                                       "/rpc/Shelly.GetStatus",
                                       timeout=3).read().decode("utf-8")
        answer = json.loads(str(aread))
    with open('/var/www/html/openWB/ramdisk/smarthome_device_ret.' +
              str(ipadr) + '_shelly', 'w') as f:
        f.write(str(answer))
except Exception:
    print("failed to connect to device on " +
          ipadr + ", setting all values to 0")
#  answer.update(a_dictionary)
#  Versuche Werte aus der Antwort zu extrahieren.
try:
    if (gen == "1"):
        aktpower = totalPowerFromShellyJson(answer, chan)
    else:
        if (chan > 0):
            workchan = chan - 1
        else:
            workchan = chan
        sw = 'switch:' + str(workchan)
        aktpower = int(answer[sw]['apower'])
except Exception:
    pass

try:
    if (chan > 0):
        workchan = chan - 1
    else:
        workchan = chan
    if (gen == "1"):
        relais = int(answer['relays'][workchan]['ison'])
    else:
        sw = 'switch:' + str(workchan)
        relais = int(answer[sw]['output'])
except Exception:
    pass

try:
    temp0 = str(answer['ext_temperature']['0']['tC'])
except Exception:
    pass

try:
    temp1 = str(answer['ext_temperature']['1']['tC'])
except Exception:
    pass

try:
    temp2 = str(answer['ext_temperature']['2']['tC'])
except Exception:
    pass
answer = '{"power":' + str(aktpower) + ',"powerc":' + str(powerc)
answer += ',"on":' + str(relais) + ',"temp0":' + str(temp0)
answer += ',"temp1":' + str(temp1) + ',"temp2":' + str(temp2) + '}'
with open('/var/www/html/openWB/ramdisk/smarthome_device_ret' +
          str(devicenumber), 'w') as f1:
    json.dump(answer, f1)
