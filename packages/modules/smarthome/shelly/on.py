#!/usr/bin/python3
import sys
import urllib.request
import os
import json
devicenumber = str(sys.argv[1])
ipadr = str(sys.argv[2])
uberschuss = int(sys.argv[3])
gen = '1'
model = '???'
try:
    chan = int(sys.argv[4])
except Exception:
    chan = 0
shaut = int(sys.argv[5])
user = str(sys.argv[6])
pw = str(sys.argv[7])
fbase = '/var/www/html/openWB/ramdisk/smarthome_device_ret.'
fnameg = fbase + str(ipadr) + '_shelly_infogv1'
if os.path.isfile(fnameg):
    with open(fnameg, 'r') as f:
        jsonin = json.loads(f.read())
        gen = str(jsonin['gen'])
        model = str(jsonin['model'])
else:
    gen = "1"
if (gen == "1"):
    if (chan == 0):
        url = "http://" + str(ipadr) + "/relay/0?turn=on"
    #    urllib.request.urlopen("http://"+str(ipadr)+"/relay/0?turn=on",
    #                           timeout=3)
    else:
        chan = chan - 1
        url = "http://" + str(ipadr) + "/relay/" + str(chan) + "?turn=on"
    #   urllib.request.urlopen("http://"+str(ipadr)+"/relay/" + str(chan) +
    #                           "?turn=on", timeout=3)
else:
    if (chan > 0):
        chan = chan - 1
    # shelly pro 3em mit add on hat fix id 100 als switch Kanal, das Device muss auf jeden fall mit separater
    # Leistunsmessung erfasst werden, da die Leistung auf drei verschiedenenen Kanälen angeliefert werden kann
    if ("SPEM-003CE" in model):
        chan = 100
    # gen 2 will das als on cmd /rpc/Switch.Set?id=100&on=true
    url = "http://" + str(ipadr) + "/rpc/Switch.Set?id=" + str(chan) + "&on=true"
if (shaut == 1):
    #  print("Shelly on" + str(shaut) + user + pw)
    passman = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, url, user, pw)
    authhandler = urllib.request.HTTPBasicAuthHandler(passman)
    opener = urllib.request.build_opener(authhandler)
    urllib.request.install_opener(opener)
with urllib.request.urlopen(url) as response:
    response.read().decode("utf-8")
