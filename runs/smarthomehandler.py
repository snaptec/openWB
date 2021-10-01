#!/usr/bin/python3
import paho.mqtt.client as mqtt
import time
import configparser
import json
import os
import argparse
import re
import getopt
import subprocess
from datetime import datetime, timezone
LOGLEVELDEBUG = 0
LOGLEVELINFO = 1
LOGLEVELERROR = 2

basePath = '/var/www/html/openWB'
shconfigfile = basePath+'/smarthome.ini'
os.chdir(basePath)
config = configparser.ConfigParser()
config.read(shconfigfile)
prefixpy = basePath+'/modules/smarthome/'
loglevel=2
maxspeicher = 100
oldmaxspeicher = 0
oldtotalwatt = 0
oldtotalwattot = 0
oldtotalminhaus = -1
olduberschuss = 0
olduberschussoffset = 0
numberOfSupportedDevices=9 # limit number of smarthome devices
DeviceValues = { }
DeviceTempValues = { }
DeviceCounters = { }
DeviceConfigured = []
DeviceConfiguredOld = []

DeviceOn = []
DeviceOnStandby = []
DeviceOnOld = []
DeviceOnOldStandby = []
StatusOld = []

for i in range(1, (numberOfSupportedDevices+1)):
    DeviceTempValues.update({'oldWHI'+str(i) : '2'})
    DeviceTempValues.update({'oldw'+str(i) : '2'})
    DeviceTempValues.update({'oldwh'+str(i) : '2'})
    DeviceTempValues.update({'oldtemp'+str(i) : '2'})
    DeviceTempValues.update({'oldtime'+str(i) : '2'})
    DeviceTempValues.update({'oldrelais'+str(i) : '2'})
    DeviceValues.update({ str(i)+"watt" : int(0)})
    DeviceValues.update({ str(i)+"runningtime" : int(0)})
    DeviceValues.update( {str(i)+"WHImported_tmp" : int(0)})
    DeviceConfigured.append("0")
    DeviceConfiguredOld.append("9")
    DeviceOn.append("0")
    DeviceOnStandby.append("0")
    DeviceOnOld.append("9999")
    DeviceOnOldStandby.append("9999")
    StatusOld.append("9999")
    filename = basePath+'/ramdisk/smarthome_device_minhaus_' + str(i)
    f = open(filename, 'w')
    f.write(str("0"))
    f.close()
    os.chmod(filename, 0o777)
global numberOfDevices

def cleardef(nummer):
    logDebug(LOGLEVELINFO, "(" + str(nummer) + ") Device nicht (mehr) definiert. MQTT auf 0 gesetzt ")
    client.publish("openWB/SmartHome/Devices/"+str(nummer)+"/RelayStatus", "0", qos=0, retain=True)
    client.loop(timeout=2.0)
    client.publish("openWB/SmartHome/Devices/"+str(nummer)+"/Watt", "0", qos=0, retain=True)
    client.loop(timeout=2.0)
    client.publish("openWB/SmartHome/Devices/"+str(nummer)+"/RunningTimeToday", "0", qos=0, retain=True)
    client.loop(timeout=2.0)
    client.publish("openWB/SmartHome/Devices/"+str(nummer)+"/OnCntStandby", "0", qos=0, retain=True)
    client.loop(timeout=2.0)
    client.publish("openWB/SmartHome/Devices/"+str(nummer)+"/OnCountNor", "0", qos=0, retain=True)
    client.loop(timeout=2.0)
    client.publish("openWB/SmartHome/Devices/"+str(nummer)+"/Status", "0", qos=0, retain=True)
    client.loop(timeout=2.0)
    try:
        DeviceValues.update({str(nummer) + "runningtime" : '0'})
    except:
        pass
    if (nummer == 1) or (nummer == 2):
        client.publish("openWB/SmartHome/Devices/"+str(nummer)+"/TemperatureSensor0", "300", qos=0, retain=True)
        client.loop(timeout=2.0)
        client.publish("openWB/SmartHome/Devices/"+str(nummer)+"/TemperatureSensor1", "300", qos=0, retain=True)
        client.loop(timeout=2.0)
        client.publish("openWB/SmartHome/Devices/"+str(nummer)+"/TemperatureSensor2", "300", qos=0, retain=True)
        client.loop(timeout=2.0)
    f = open(basePath+'/ramdisk/device' + str(nummer) + '_watt', 'w')
    f.write(str("0"))
    f.close()
    f = open(basePath+'/ramdisk/device' + str(nummer) + '_relais', 'w')
    f.write(str("0"))
    f.close()
    #status normal setzen
    setstat(nummer,10)
    try:
        del DeviceCounters[str(nummer)+"oldstampeinschaltdauer"]
    except:
        pass
    if os.path.isfile(basePath+'/ramdisk/smarthome_device_'+str(nummer)+'sec0'):
        os.remove(basePath+'/ramdisk/smarthome_device_'+str(nummer)+'sec0')
        logDebug(LOGLEVELINFO, "(" + str(nummer) + ") Device nicht (mehr) definiert. Simcount aktuelle Leistung gelöscht ")
def gettyp(nummer):
    try:
        smarttype =  str(config.get('smarthomedevices', 'device_type_'+str(nummer)))
    except:
        smarttype = 'none'
    if (smarttype == "none"):
        return (smarttype, 0)
    try:
        canswitch = int(config.get('smarthomedevices', 'device_canswitch_'+str(nummer)))
    except:
        canswitch = 1
    return (smarttype, canswitch)
def checkbootdone():
    try:
        with open(basePath+'/ramdisk/bootinprogress', 'r') as value:
            bootinprogress = int(value.read())
    except Exception as e:
        bootinprogress = 1
        logDebug(LOGLEVELERROR, "Ramdisk not set up. Maybe we are still booting (bootinprogress)." + str(e))
        time.sleep(30)
        return 0
    try:
        with open(basePath+'/ramdisk/updateinprogress', 'r') as value:
            updateinprogress = int(value.read())
    except Exception as e:
        updateinprogress = 1
        logDebug(LOGLEVELERROR, "Ramdisk not set up. Maybe we are still booting (updateinprogress)." + str(e))
        time.sleep(30)
        return 0
    if (updateinprogress == 1):
        logDebug(LOGLEVELERROR, "Update in progress.")
        time.sleep(30)
        return 0
    if (bootinprogress == 1):
        logDebug(LOGLEVELERROR, "Boot in progress.")
        time.sleep(30)
        return 0
    return 1
#art der Ueberschussberechnung lesen, relevanten ueberschuss zurueckgeben
def getueb(nummer):
#    (1 = mit Speicher, 2 = mit offset , 0 = manual eingeschaltet)
    ueberschussberechnung = 1
    if os.path.isfile(basePath+'/ramdisk/device' + str(nummer) + '_ueberschuss'):
        f = open(basePath+'/ramdisk/device' + str(nummer) + '_ueberschuss', 'r')
        ueberschussberechnung=int(f.read())
        f.close()
    if (ueberschussberechnung == 2):
        return (uberschussoffset,2)
    else:
        return (uberschuss,1)
# setze art der Ueberschussrechnung
def setueb(nummer,ueberschussberechnung):
#    (1 = mit Speicher, 2 = mit offset, 0 = manual eingeschaltet oder finishtime)
    f = open(basePath+'/ramdisk/device' + str(nummer) + '_ueberschuss', 'w')
    f.write(str(ueberschussberechnung))
    f.close()
# get status

def getstat(nummer):
#    (10 = ueberschuss gesteuert oder manual, 20 = Anlauferkennung aktiv (ausschalten wenn Leistungsaufnahme > Schwelle) , 30 = gestartet um fertig bis zu erreichen
    status = 10
    if os.path.isfile(basePath+'/ramdisk/device' + str(nummer) + '_status'):
        f = open(basePath+'/ramdisk/device' + str(nummer) + '_status', 'r')
        status=int(f.read())
        f.close()
    return status
def setstat(nummer,status):
    f = open(basePath+'/ramdisk/device' + str(nummer) + '_status', 'w')
    f.write(str(status))
    f.close()

# support old smarttypes and new smarttypes
def getdir(smarttype,name):
    if (smarttype == "shelly"):
        dirname = prefixpy + 'shelly'
        return dirname
    if (smarttype == "tasmota"):
        dirname = prefixpy + 'tasmota'
        return dirname
    if (smarttype == "pyt"):
        dirname = prefixpy + name.lower()
        return dirname
    if (smarttype == "avm"):
        dirname = prefixpy + 'avmhomeautomation'
        return dirname
    dirname = prefixpy + smarttype.lower()
    return dirname
def sepwatt(oldwatt,oldwattk,nummer):
    try:
        difmes = int(config.get('smarthomedevices', 'device_differentmeasurement_'+str(nummer)))
    except:
        difmes = 0
    try:
        configuredName = config.get('smarthomedevices', 'device_name_'+str(nummer))
    except:
        configuredName = "(unknown name)"
    if difmes == 0:
        newwatt = oldwatt
       # simcount verwenden wenn newwattk = 0
        newwattk = oldwattk
        return (newwatt, newwattk)
    try:
        meastyp = str(config.get('smarthomedevices', 'device_measuretype_'+str(nummer)))
    except:
        meastyp = "undef"
    logDebug(LOGLEVELDEBUG, "(" + str(nummer) + ") Leistungsmessung durch " +  meastyp)
    argumentList = ['python3', 'undef', str(nummer)]
    try:
        argumentList.append(config.get('smarthomedevices', 'device_measureip_'+str(nummer)))
    except:
        argumentList.append("undef")
    (devuberschuss,ueberschussberechnung )= getueb(nummer)
    argumentList.append(str(devuberschuss))
    if meastyp == "sdm120":
        try:
            measureportsdm = str(config.get('smarthomedevices', 'device_measureportsdm_'+str(nummer)))
        except:
            measureportsdm = "8899"
        argumentList[1] = prefixpy +'sdm120/sdm120.py'
        argumentList[4] = config.get('smarthomedevices', 'device_measureid_'+str(nummer)) # replace uberschuss as third command line parameter with measureid
        argumentList.append(measureportsdm)
    elif meastyp == "sdm630":
        try:
            measureportsdm = str(config.get('smarthomedevices', 'device_measureportsdm_'+str(nummer)))
        except:
            measureportsdm = "8899"
        argumentList[1] = prefixpy +'sdm630/sdm630.py'
        argumentList[4] = config.get('smarthomedevices', 'device_measureid_'+str(nummer)) # replace uberschuss as third command line parameter with measureid
        argumentList.append(measureportsdm)
    elif meastyp == "we514":
        argumentList[1] = prefixpy +'we514/watt.py'
        argumentList[4] = config.get('smarthomedevices', 'device_measureid_'+str(nummer)) # replace uberschuss as third command line parameter with measureid
    elif meastyp == "fronius":
        argumentList[1] = prefixpy +'fronius/watt.py'
        argumentList[4] = config.get('smarthomedevices', 'device_measureid_'+str(nummer)) # replace uberschuss as third command line parameter with measureid
    elif meastyp == "shelly":
        argumentList[1] = prefixpy + 'shelly/watt.py'
    elif meastyp == "mystrom":
        argumentList[1] = prefixpy + 'mystrom/watt.py'
    elif meastyp == "http":
        argumentList[1] = prefixpy + 'http/watt.py'
        try:
            measureurl = str(config.get('smarthomedevices', 'device_measureurl_'+str(nummer)))
            argumentList.append(measureurl)
        except:
            argumentList.append("undef")
        try:
            measureurlc = str(config.get('smarthomedevices', 'device_measureurlc_'+str(nummer)))
            argumentList.append(measureurlc)
        except:
            argumentList.append("none")
    elif meastyp == "json":
        argumentList[1] = prefixpy + 'json/watt.py'
        try:
            argumentList[3] = str(config.get('smarthomedevices', 'device_measurejsonurl_'+str(nummer)))
        except:
            argumentList[3] = "undef"
        try:
            argumentList[4] = str(config.get('smarthomedevices', 'device_measurejsonpower_'+str(nummer)))
        except:
            argumentList[4] = "undef"
        try:
            argumentList.append(str(config.get('smarthomedevices', 'device_measurejsoncounter_'+str(nummer))))
        except:
            argumentList.append("none")
    elif meastyp == "avm":
        argumentList[1] = prefixpy + 'avmhomeautomation/watt.py'
        argumentList.append("undef") # 3
        # 4
        try:
            measureactor = str(config.get('smarthomedevices', 'device_measureavmactor_'+str(nummer)))
            argumentList.append(measureactor)
        except:
            argumentList.append("undef")
        # 5
        try:
            measureusername = str(config.get('smarthomedevices', 'device_measureavmusername_'+str(nummer)))
            argumentList.append(measureusername)
        except:
            argumentList.append("undef")
        # 6
        try:
            measurepassword = str(config.get('smarthomedevices', 'device_measureavmpassword_'+str(nummer)))
            argumentList.append(measurepassword)
        except:
            argumentList.append("undef")
    elif meastyp == "smaem":
        argumentList[1] = prefixpy + 'smaem/watt.py'
    else:
       # no known meastyp, so return the old values directly
        logDebug(LOGLEVELERROR, "Leistungsmessung %s %d %s Geraetetyp ist nicht implementiert!" % (meastyp, nummer, str(configuredName)))
        newwatt = oldwatt
        newwattk = oldwattk
        return (newwatt, newwattk)
    # now we have everthing we need to call the subprocess
    try:
        proc = subprocess.Popen(argumentList)
        proc.communicate()
        f1 = open(basePath+'/ramdisk/smarthome_device_ret' + str(nummer) , 'r')
        answerj = json.load(f1)
        f1.close()
        answer = json.loads(answerj)
        newwatt = int(answer['power'])
        newwattk = int(answer['powerc'])
    except Exception as e1:
        DeviceValues.update( {str(nummer) : "error"})
        logDebug(LOGLEVELERROR, "Leistungsmessung %s %d %s Fehlermeldung: %s " % (meastyp, nummer, str(configuredName), str(e1)))
        raise Exception("error in sepwatt")
    return (newwatt, newwattk)
def logDebug(level, msg):
    if (int(level) >= int(loglevel)):
        local_time = datetime.now(timezone.utc).astimezone()
        file = open(basePath+'/ramdisk/smarthome.log', 'a',encoding='utf8')
        if (int(level) == 0):
            file.write(local_time.strftime(format = "%Y-%m-%d %H:%M:%S") + ': ' + str(msg)+ '\n')
        if (int(level) == 1):
            file.write(local_time.strftime(format = "%Y-%m-%d %H:%M:%S") + ': ' + str(msg)+ '\n')
        if (int(level) == 2):
            file.write(local_time.strftime(format = "%Y-%m-%d %H:%M:%S") + ': ' + str(msg)+ '\n')
        file.close()
def simcount(watt2, pref, importfn, exportfn, nummer,wattks):
    # Zaehler mitgeliefert in WH , zurueckrechnen fuer simcount
    if wattks > 0:
        wattposkh=wattks
        wattnegkh=0
        wattposh=wattks * 3600
        wattnegh= 0
        f = open(basePath+'/ramdisk/'+pref+'watt0pos', 'w')
        f.write(str(wattposh))
        f.close()
        DeviceValues.update( {str(nummer) + "wpos" : wattposh})
        f = open(basePath+'/ramdisk/'+pref+'watt0neg', 'w')
        f.write(str(wattnegh))
        f.close()
        f = open(basePath+'/ramdisk/'+ importfn,'w')
        #    f = open(basePath+'/ramdisk/speicherikwh', 'w')
        DeviceValues.update( {str(nummer) + "wh" : round(wattposkh, 2)})
        f.write(str(round(wattposkh, 2)))
        f.close()
        f = open(basePath+'/ramdisk/' +exportfn , 'w')
        #   f = open(basePath+'/ramdisk/speicherekwh', 'w')
        f.write(str(wattnegkh))
        f.close()
        return
    # emulate import  export
    seconds2= time.time()
    watt1=0
    seconds1=0.0
    if os.path.isfile(basePath+'/ramdisk/'+pref+'sec0'):
        f = open(basePath+'/ramdisk/'+pref+'sec0', 'r')
        seconds1=float(f.read())
        f.close()
        f = open(basePath+'/ramdisk/'+pref+'wh0', 'r')
        watt1=int(f.read())
        f.close()
        f = open(basePath+'/ramdisk/'+pref+'watt0pos', 'r')
        wattposh=int(f.read())
        f.close()
        f = open(basePath+'/ramdisk/'+pref+'watt0neg', 'r')
        wattnegh=int(f.read())
        f.close()
        f = open(basePath+'/ramdisk/'+pref+'sec0', 'w')
        value1 = "%22.6f" % seconds2
        f.write(str(value1))
        f.close()
        f = open(basePath+'/ramdisk/'+pref+'wh0', 'w')
        f.write(str(watt2))
        f.close()
        seconds1=seconds1+1
        deltasec = seconds2- seconds1
        deltasectrun =int(deltasec* 1000) / 1000
        stepsize = int((watt2-watt1)/deltasec)
        while seconds1 <= seconds2:
            if watt1 < 0:
                wattnegh= wattnegh + watt1
            else:
                wattposh= wattposh + watt1
            watt1 = watt1 + stepsize
            if stepsize < 0:
                watt1 = max(watt1,watt2)
            else:
                watt1 = min(watt1,watt2)
            seconds1= seconds1 +1
        rest= deltasec - deltasectrun
        seconds1= seconds1  - 1 + rest
        if rest > 0:
            watt1 = int(watt1 * rest)
            if watt1 < 0:
                wattnegh= wattnegh + watt1
            else:
                wattposh= wattposh + watt1
        wattposkh=wattposh/3600
        wattnegkh=(wattnegh*-1)/3600
        f = open(basePath+'/ramdisk/'+pref+'watt0pos', 'w')
        f.write(str(wattposh))
        f.close()
        DeviceValues.update( {str(nummer) + "wpos" : wattposh})
        f = open(basePath+'/ramdisk/'+pref+'watt0neg', 'w')
        f.write(str(wattnegh))
        f.close()
        f = open(basePath+'/ramdisk/'+ importfn,'w')
        #    f = open(basePath+'/ramdisk/speicherikwh', 'w')
        DeviceValues.update( {str(nummer) + "wh" : round(wattposkh, 2)})
        f.write(str(round(wattposkh, 2)))
        f.close()
        f = open(basePath+'/ramdisk/' +exportfn , 'w')
        #   f = open(basePath+'/ramdisk/speicherekwh', 'w')
        f.write(str(wattnegkh))
        f.close()
    else:
        f = open(basePath+'/ramdisk/'+pref+'sec0', 'w')
        value1 = "%22.6f" % seconds2
        f.write(str(value1))
        f.close()
        f = open(basePath+'/ramdisk/'+pref+'wh0', 'w')
        f.write(str(watt2))
        f.close()

def publishmqtt():
    global oldmaxspeicher
    global oldtotalwatt
    global oldtotalwattot
    global oldtotalminhaus
    global olduberschuss
    global olduberschussoffset
    global totalwatt
    global totalwattot
    global totalminhaus
    global numberOfSupportedDevices
    client = mqtt.Client("openWB-SmartHome-bulkpublisher-" + str(os.getpid()))
    client.connect("localhost")
    for key in DeviceValues:
        if ( "relais" in key):
            nummer = int(list(filter(str.isdigit, key))[0])
            if ( DeviceValues[str(key)] != DeviceTempValues['oldrelais' + str(nummer)]):
                client.publish("openWB/SmartHome/Devices/"+str(nummer)+"/RelayStatus", payload=DeviceValues[str(key)], qos=0, retain=True)
                client.loop(timeout=2.0)
                DeviceTempValues.update({'oldrelais'+str(nummer) : DeviceValues[str(key)]})
        if ( "time" in key):
            nummer = str(list(filter(str.isdigit, key))[0])
            if ( DeviceValues[str(key)] != DeviceTempValues['oldtime' + str(nummer)]):
                client.publish("openWB/SmartHome/Devices/"+str(nummer)+"/RunningTimeToday", payload=DeviceValues[str(key)], qos=0, retain=True)
                client.loop(timeout=2.0)
                DeviceTempValues.update({'oldtime'+str(nummer) : DeviceValues[str(key)]})
        if ( "temp" in key):
            nummer = str(list(filter(str.isdigit, key))[0])
            if ( DeviceValues[str(key)] != DeviceTempValues['oldtemp' + str(nummer)]):
                sensor = str(list(filter(str.isdigit, key))[1])
                client.publish("openWB/SmartHome/Devices/"+str(nummer)+"/TemperatureSensor"+str(sensor), payload=DeviceValues[str(key)], qos=0, retain=True)
                client.loop(timeout=2.0)
                DeviceTempValues.update({'oldtemp'+str(nummer) : DeviceValues[str(key)]})
        if ( "watt" in key):
            nummer = int(list(filter(str.isdigit, key))[0])
            if ( DeviceValues[str(key)] != DeviceTempValues['oldw' + str(nummer)]):
                client.publish("openWB/SmartHome/Devices/"+str(nummer)+"/Watt", payload=DeviceValues[str(key)], qos=0, retain=True)
                client.loop(timeout=2.0)
                DeviceTempValues.update({'oldw'+str(nummer) : DeviceValues[str(key)]})
        if ( "wh" in key):
            nummer = int(list(filter(str.isdigit, key))[0])
            if ( DeviceValues[str(key)] != DeviceTempValues['oldwh' + str(nummer)]):
                client.publish("openWB/SmartHome/Devices/"+str(nummer)+"/Wh", payload=DeviceValues[str(key)], qos=0, retain=True)
                client.loop(timeout=2.0)
                DeviceTempValues.update({'oldwh'+str(nummer) : DeviceValues[str(key)]})
        if ( "wpos" in key):
            nummer = int(list(filter(str.isdigit, key))[0])
            if ( DeviceValues[str(key)] != DeviceTempValues['oldWHI' + str(nummer)]):
                client.publish("openWB/SmartHome/Devices/"+str(nummer)+"/WHImported_temp", payload=DeviceValues[str(key)], qos=0, retain=True)
                client.loop(timeout=2.0)
                DeviceTempValues.update({'oldWHI'+str(nummer) : DeviceValues[str(key)]})
    if (oldmaxspeicher != maxspeicher):
        client.publish("openWB/SmartHome/Status/maxspeicherladung", payload=str(maxspeicher), qos=0, retain=True)
        client.loop(timeout=2.0)
        oldmaxspeicher = maxspeicher
    if (oldtotalwatt != totalwatt):
        client.publish("openWB/SmartHome/Status/wattschalt", payload=str(totalwatt), qos=0, retain=True)
        client.loop(timeout=2.0)
        oldtotalwatt = totalwatt
    if (oldtotalwattot != totalwattot):
        client.publish("openWB/SmartHome/Status/wattnichtschalt", payload=str(totalwattot), qos=0, retain=True)
        client.loop(timeout=2.0)
        oldtotalwattot = totalwattot
    if (oldtotalminhaus != totalminhaus):
        client.publish("openWB/SmartHome/Status/wattnichtHaus", payload=str(totalminhaus), qos=0, retain=True)
        client.loop(timeout=2.0)
        oldtotalminhaus = totalminhaus
    if (olduberschuss != uberschuss):
        client.publish("openWB/SmartHome/Status/uberschuss", payload=str(uberschuss), qos=0, retain=True)
        client.loop(timeout=2.0)
        olduberschuss = uberschuss
    if (olduberschussoffset != uberschussoffset):
        client.publish("openWB/SmartHome/Status/uberschussoffset", payload=str(uberschussoffset), qos=0, retain=True)
        client.loop(timeout=2.0)
        olduberschussoffset = uberschussoffset
    for i in range(1, (numberOfSupportedDevices+1)):
        if (DeviceOn[i-1] != DeviceOnOld [i-1]):
            client.publish("openWB/SmartHome/Devices/"+str(i)+"/OnCountNor", payload=str(DeviceOn[i-1]) , qos=0, retain=True)
            client.loop(timeout=2.0)
            DeviceOnOld [i-1] =  DeviceOn[i-1]
        if (DeviceOnStandby[i-1] != DeviceOnOldStandby [i-1]):
            client.publish("openWB/SmartHome/Devices/"+str(i)+"/OnCntStandby", payload=str(DeviceOnStandby[i-1]) , qos=0, retain=True)
            client.loop(timeout=2.0)
            DeviceOnOldStandby [i-1] =  DeviceOnStandby[i-1]
        devstatus=getstat(i)
        #nur bei Status 10 on status mitnehmen
        if (devstatus == 10):
            if str(i)+"relais" in DeviceValues:
                devstatus = devstatus + int( DeviceValues[str(i)+"relais"])
        if (devstatus != StatusOld [i-1]):
            client.publish("openWB/SmartHome/Devices/"+str(i)+"/Status", payload=str(devstatus) , qos=0, retain=True)
            client.loop(timeout=2.0)
            StatusOld [i-1] =  devstatus
    client.disconnect()
# Lese aus der Ramdisk Regelrelevante Werte ein
def loadregelvars():
    global uberschuss
    global uberschussoffset
    global speicherleistung
    global speichersoc
    global speichervorhanden
    global loglevel
    global reread
    global wattbezug
    global numberOfSupportedDevices
    global maxspeicher
    try:
        with open(basePath+'/ramdisk/speichervorhanden', 'r') as value:
            speichervorhanden = int(value.read())
        if ( speichervorhanden == 1):
            with open(basePath+'/ramdisk/speicherleistung', 'r') as value:
                speicherleistung = int(float(value.read()))
            with open(basePath+'/ramdisk/speichersoc', 'r') as value:
                speichersoc = int(float(value.read()))
        else:
            speicherleistung = 0
            speichersoc = 100
    except Exception as e:
        logDebug(LOGLEVELERROR, "Fehler beim Auslesen der Ramdisk (speichervorhanden,speicherleistung,speichersoc): " + str(e))
        speichervorhanden = 0
        speicherleistung = 0
        speichersoc = 100
    try:
        with open(basePath+'/ramdisk/wattbezug', 'r') as value:
            wattbezug = int(float(value.read())) * -1
    except Exception as e:
        logDebug(LOGLEVELERROR, "Fehler beim Auslesen der Ramdisk (wattbezug): " + str(e))
        wattbezug = 0
    uberschuss = wattbezug + speicherleistung
    try:
        with open(basePath+'/ramdisk/smarthomehandlermaxbatterypower', 'r') as value:
            maxspeicher = int(value.read())
    except Exception as e:
        logDebug(LOGLEVELERROR, "Fehler beim Auslesen der Ramdisk (smarthomehandlermaxbatterypower): " + str(e))
        maxspeicher = 0
    uberschussoffset = wattbezug + speicherleistung - maxspeicher
    try:
        with open('ramdisk/smarthomehandlerloglevel', 'r') as value:
            loglevel = int(value.read())
    except:
            loglevel=2
            f = open(basePath+'/ramdisk/smarthomehandlerloglevel', 'w')
            f.write(str(2))
            f.close()
    try:
        with open('ramdisk/rereadsmarthomedevices', 'r') as value:
            reread = int(value.read())
    except:
        reread = 1
        config.read(shconfigfile)
    if ( reread == 1):
        config.read(shconfigfile)
        f = open(basePath+'/ramdisk/rereadsmarthomedevices', 'w')
        f.write(str(0))
        f.close()
        logDebug(LOGLEVELERROR, "Config reRead")
    for i in range(1, (numberOfSupportedDevices+1)):
        try:
            with open('ramdisk/smarthome_device_manual_' + str(i), 'r') as value:
                DeviceValues.update( {str(i) + "manual": int(value.read())})
        except:
            DeviceValues.update( {str(i) + "manual": 0})
    for i in range(1, (numberOfSupportedDevices+1)):
        try:
            with open('ramdisk/smarthome_device_manual_control_' + str(i), 'r') as value:
                DeviceValues.update( {str(i) + "manualmodevar": int(value.read())})
        except:
            DeviceValues.update( {str(i) + "manualmodevar": 2})
    logDebug(LOGLEVELDEBUG, "EVU Bezug(-)/Einspeisung(+): " + str(wattbezug) + " max Speicherladung: " + str(maxspeicher))
    logDebug(LOGLEVELDEBUG, "Uberschuss: " + str(uberschuss)  + " Uberschuss mit Offset: " + str(uberschussoffset) )
    logDebug(LOGLEVELDEBUG, "Speicher Entladung(-)/Ladung(+): " + str(speicherleistung) + " SpeicherSoC: " + str(speichersoc))
    f = open(basePath+'/ramdisk/devicemaxspeicher', 'w')
    f.write(str(maxspeicher))
    f.close()
def on_connect(client, userdata, flags, rc):
    client.subscribe("openWB/SmartHome/#", 2)

def on_message(client, userdata, msg):
    global numberOfSupportedDevices
    #logDebug(LOGLEVELERROR, "(" + str(msg.topic) + ") " +   str(msg.payload) )
    if (( "openWB/SmartHome/Device" in msg.topic) and ("WHImported_temp" in msg.topic)):
        devicenumb=re.sub(r'\D', '', msg.topic)
        if ( 1 <= int(devicenumb) <= numberOfSupportedDevices ):
            DeviceValues.update( {str(devicenumb)+"WHImported_tmp": int(msg.payload)})
            importtemp = int(DeviceValues[str(devicenumb)+"WHImported_tmp"])
            logDebug(LOGLEVELERROR,"(" + str(devicenumb) + ") WHImported_temp read from mqtt " + str(importtemp))
    if (( "openWB/SmartHome/Device" in msg.topic) and ("RunningTimeToday" in msg.topic)):
        devicenumb=re.sub(r'\D', '', msg.topic)
        if ( 1 <= int(devicenumb) <= numberOfSupportedDevices ):
            DeviceValues.update( {str(devicenumb)+"runningtime": int(msg.payload)})
            runtime=DeviceValues[str(devicenumb)+"runningtime"]
            if runtime != 0:
                logDebug(LOGLEVELERROR, "(" + str(devicenumb) + ") runningtime read from mqtt: " +  str(runtime))
    if (( "openWB/SmartHome/Device" in msg.topic) and ("OnCountNor" in msg.topic)):
        devicenumb=re.sub(r'\D', '', msg.topic)
        if ( 1 <= int(devicenumb) <= numberOfSupportedDevices ):
            DeviceOn[int(devicenumb)-1] = str(int(msg.payload))
            logDebug(LOGLEVELERROR, "(" + str(devicenumb) + ") onCountNor read from mqtt " +  str(DeviceOn[int(devicenumb)-1]))
    if (( "openWB/SmartHome/Device" in msg.topic) and ("OnCntStandby" in msg.topic)):
        devicenumb=re.sub(r'\D', '', msg.topic)
        if ( 1 <= int(devicenumb) <= numberOfSupportedDevices ):
            DeviceOnStandby[int(devicenumb)-1] = str(int(msg.payload))
            #status normal setzen
            setstat(devicenumb,10)
            logDebug(LOGLEVELERROR, "(" + str(devicenumb) + ") OnCntStandby read from mqtt " +  str(DeviceOnStandby[int(devicenumb)-1]) + ", set status = 10 ")
# Auslesen des Smarthome Devices (Watt und/oder Temperatur)
def getdevicevalues():
    global totalwatt
    global totalwattot
    global totalminhaus
    for i in range(1, (numberOfSupportedDevices+1)):
        DeviceConfigured[i-1] = config.get('smarthomedevices', 'device_configured_'+str(i)) # list starts at 0
        if (DeviceConfigured[i-1] != DeviceConfiguredOld[i-1]) and (DeviceConfigured[i-1] == "0"):
            cleardef(i)
            DeviceOn[i-1]= str("0")
            DeviceOnStandby[i-1]= str("0")
        if (DeviceConfiguredOld[i-1] == "9") and (DeviceConfigured[i-1] == "1"):
            try:
                deactivatewhileevcharging = int(config.get('smarthomedevices', 'device_deactivatewhileevcharging_'+str(i)))
            except:
                deactivatewhileevcharging = 0
            if deactivatewhileevcharging == 1:
            # nach startup alle aktiven devices mit Autoladen aus als other fuehren
                DeviceCounters.update( {str(i) + "mantime" : time.time()})
        DeviceConfiguredOld[i-1] = DeviceConfigured[i-1]
    numberOfDevices = 0
    totalwatt = 0
    totalwattot = 0
    totalminhaus = 0
    for n in DeviceConfigured:
        numberOfDevices += 1
        # prepare
        abschalt = 0
        try:
            deactivatewhileevcharging = int(config.get('smarthomedevices', 'device_deactivatewhileevcharging_'+str(numberOfDevices)))
        except:
            deactivatewhileevcharging = 0
        try:
            mineinschaltdauer = int(config.get('smarthomedevices', 'device_mineinschaltdauer_'+str(numberOfDevices))) * 60
        except:
            mineinschaltdauer = 0
        if deactivatewhileevcharging == 1:
            if str(numberOfDevices)+"eintime" in DeviceCounters:
                timestart = int(time.time()) - int(DeviceCounters[str(numberOfDevices)+"eintime"])
                if ( mineinschaltdauer < timestart):
                    abschalt = 1
                else:
                    abschalt = 0
            else:
                abschalt = 1
        # prepare end
        if ( n == "1" ):
            #alle devices laufen gleich
            (switchtyp,canswitch) = gettyp(numberOfDevices)
            devicename = str(config.get('smarthomedevices', 'device_name_'+str(numberOfDevices)))
            (devuberschuss,ueberschussberechnung) = getueb(numberOfDevices)
            try:
                device_leistungurl = str(config.get('smarthomedevices', 'device_leistungurl_'+str(numberOfDevices)))
            except:
                device_leistungurl = "undef"
            try:
                device_actor = str(config.get('smarthomedevices','device_actor_'+str(numberOfDevices)))
            except:
                device_actor = "undef"
            try:
                device_username = str(config.get('smarthomedevices','device_username_'+str(numberOfDevices)))
            except:
                device_username = "undef"
            try:
                device_password = str(config.get('smarthomedevices','device_password_'+str(numberOfDevices)))
            except:
                device_password = "undef"
            try:
                device_ip = str(config.get('smarthomedevices', 'device_ip_'+str(numberOfDevices)))
            except:
                device_ip = "undef"
            try:
                device_acthortype = str(config.get('smarthomedevices', 'device_acthortype_'+str(numberOfDevices)))
            except:
                device_acthortype = "undef"
            try:
                device_acthorpower = int(config.get('smarthomedevices', 'device_acthorpower_'+str(numberOfDevices)))
            except:
                device_acthorpower = 0
            try:
                device_homeconsumtion = int(config.get('smarthomedevices', 'device_homeconsumtion_'+str(numberOfDevices)))
            except:
                device_homeconsumtion = 0
            pyname0 = getdir(switchtyp,devicename)
            try:
                pyname = pyname0 +"/watt.py"
                if os.path.isfile(pyname) and (switchtyp != "none"):
                    argumentList = ['python3', pyname, str(numberOfDevices)]
                    argumentList.append(device_ip)
                    argumentList.append(str(devuberschuss))
                    if (switchtyp == "acthor"):
                        argumentList.append(device_acthortype)
                        argumentList.append(str(device_acthorpower))
                    else:
                        argumentList.append(device_leistungurl)
                        argumentList.append(device_actor)
                    argumentList.append(device_username)
                    argumentList.append(device_password)
                    try:
                        proc=subprocess.Popen(argumentList)
                        proc.communicate()
                    except Exception as e:
                        DeviceValues.update( {str(numberOfDevices) : "error"})
                        logDebug(LOGLEVELERROR, "Device " + str(switchtyp) + str(numberOfDevices) + str(devicename) + " Fehlermeldung (zugriff watt.py): " + str(e))
                    try:
                        f1 = open(basePath+'/ramdisk/smarthome_device_ret' +str(numberOfDevices) , 'r')
                        answerj=json.load(f1)
                        f1.close()
                    except Exception as e:
                        DeviceValues.update( {str(numberOfDevices) : "error"})
                        logDebug(LOGLEVELERROR, "Device " + str(switchtyp) + str(numberOfDevices) + str(devicename) + " Fehlermeldung (zugriff return file (1)): " + str(e))
                    try:
                        answer = json.loads(answerj)
                        wattstart = int(answer['power'])
                        wattkstart = int(answer['powerc'])
                        # bei laufender Anlauferkennung deivce nicht aktiv setzten
                        devstatus=getstat(numberOfDevices)
                        if (int(answer['on']) == 1) and (devstatus != 20):
                            relais=1
                        else:
                            relais=0
                    except Exception as e:
                        DeviceValues.update( {str(numberOfDevices) : "error"})
                        logDebug(LOGLEVELERROR, "Device " + str(switchtyp) + str(numberOfDevices) + str(devicename) + " Fehlermeldung (zugriff return file (2)): " + str(e) + str(answerj))
                    #Shelly temp sensor
                    if (switchtyp == "shelly")  and (canswitch == 1):
                        try:
                            anzahltemp = int(config.get('smarthomedevices', 'device_temperatur_configured_'+str(numberOfDevices)))
                            if ( anzahltemp > 0):
                                for i in range(anzahltemp):
                                    temp = str(answer['temp' +  str(i)])
                                    logDebug(LOGLEVELERROR, "(" + str(numberOfDevices) + ") Shelly temp sensor: " + str(i+1) + " Grad: " +  temp)
                                    DeviceValues.update( {str(numberOfDevices) + "temp" + str(i) : temp })
                                    f = open(basePath+'/ramdisk/device' + str(numberOfDevices) + '_temp'+ str(i), 'w')
                                    f.write(str(temp))
                                    f.close()
                        except:
                            pass
                    #mystrom temp sensor
                    if (switchtyp == "mystrom")  and (canswitch == 1):
                        temp = str(answer['temp0'])
                        logDebug(LOGLEVELERROR, "(" + str(numberOfDevices) + ") mystrom temp sensor: 1 Grad: " +  temp)
                        DeviceValues.update( {str(numberOfDevices) + "temp0"  : temp })
                        f = open(basePath+'/ramdisk/device' + str(numberOfDevices) + '_temp0', 'w')
                        f.write(str(temp))
                        f.close()
                else:
                    wattstart = 0
                    wattkstart = 0
                    relais = 0
                   # only relevant for canswitch == 1, file not found
                    if (canswitch == 1):
                        logDebug(LOGLEVELDEBUG, "Device " + str(switchtyp) + str(numberOfDevices) + str(devicename) + " File not found: " + str(pyname))
                # Separate Leistungs messung ?
                (watt,wattk) = sepwatt(wattstart,wattkstart,numberOfDevices)
                # nur abschaltbar wenn openwb in pv modus gesetzt hat und nicht manual gesteuert
                # elwa Warmwassersicherstellung Problem
                if str(numberOfDevices)+"mantime" in DeviceCounters and (DeviceValues[str(numberOfDevices)+"manual"] != 1):
                    # nach Ausschalten manueller Modus mindestens 30 Sek + max( ausschaltverzögerung,mindeseinschaltdauer
                    #  als nicht abschaltbarer
                    # device fuehren, damit nicht ungewollt pv überwchuss erkannt wird
                    manverz = max( int(config.get('smarthomedevices', 'device_ausschaltverzoegerung_'+str(numberOfDevices))) * 60, int(config.get('smarthomedevices', 'device_mineinschaltdauer_'+str(numberOfDevices))) * 60) + 30
                    timesince = int(time.time()) - int(DeviceCounters[str(numberOfDevices)+"mantime"])
                    if ( manverz < timesince ):
                        del DeviceCounters[str(numberOfDevices)+"mantime"]
                        logDebug(LOGLEVELDEBUG, "(" + str(numberOfDevices) + ") " + str(devicename) + " von Manuell auf Automatisch gestellt oder startup, Uebergangsfrist abgelaufen")
                    else:
                        logDebug(LOGLEVELDEBUG, "(" + str(numberOfDevices) + ") " + str(devicename) + " von Manuell auf Automatisch gestellt oder startup, Uebergangsfrist laueft noch " + str(manverz) + " > " + str(timesince) )
                        abschalt = 0
                if (abschalt == 1) and (relais == 1) and (DeviceValues[str(numberOfDevices)+"manual"] != 1):
                    totalwatt = totalwatt + watt
                else:
                    totalwattot = totalwattot + watt
                if (device_homeconsumtion == 0):
                    totalminhaus = totalminhaus + watt
                f = open(basePath+'/ramdisk/smarthome_device_minhaus_' + str(numberOfDevices), 'w')
                f.write(str(device_homeconsumtion))
                f.close()
                DeviceValues.update( {str(numberOfDevices) + "watt" : watt})
                DeviceValues.update( {str(numberOfDevices) + "relais" : relais})
                f = open(basePath+'/ramdisk/device' + str(numberOfDevices) + '_watt', 'w')
                f.write(str(watt))
                f.close()
                f = open(basePath+'/ramdisk/device' + str(numberOfDevices) + '_relais', 'w')
                f.write(str(relais))
                f.close()
                try:
                    with open(basePath+'/ramdisk/smarthome_device_' + str(numberOfDevices) + 'watt0pos', 'r') as value:
                        importtemp = int(value.read())
                    simcount(watt, "smarthome_device_"+ str(numberOfDevices), "device"+ str(numberOfDevices)+"_wh" ,"device"+ str(numberOfDevices)+"_whe", str(numberOfDevices),wattk)
                   #importtemp1 = int(DeviceValues[str(numberOfDevices)+"wpos"]) # unused variable
                except Exception as e:
                    importtemp = int(DeviceValues[str(numberOfDevices)+"WHImported_tmp"])
                    f = open(basePath+'/ramdisk/smarthome_device_' + str(numberOfDevices) + 'watt0pos', 'w')
                    f.write(str(importtemp))
                    f.close()
                    f = open(basePath+'/ramdisk/smarthome_device_' + str(numberOfDevices) + 'watt0neg', 'w')
                    f.write(str("0"))
                    f.close()
                #Update Einschaltdauer Timer
                if ( relais == 1):
                    newtime = int(time.time())
                    try:
                        if str(numberOfDevices)+"oldstampeinschaltdauer" in DeviceCounters:
                            timediff = newtime - DeviceCounters[str(numberOfDevices)+"oldstampeinschaltdauer"]
                            try:
                                DeviceValues[str(numberOfDevices)+"runningtime"]= DeviceValues[str(numberOfDevices)+"runningtime"] + int(timediff)
                            except Exception as e:
                                DeviceValues.update( {str(numberOfDevices) + "runningtime" : int(0)})
                            DeviceCounters.update( {str(numberOfDevices) + "oldstampeinschaltdauer" : newtime})
                        else:
                            DeviceCounters.update( {str(numberOfDevices) + "oldstampeinschaltdauer" : newtime})
                    except Exception as e:
                       logDebug(LOGLEVELERROR, "Device " + str(switchtyp) + str(numberOfDevices) + str(devicename) + " (Einschaltdauer)Fehlermeldung: " + str(e))
                else:
                    try:
                        del DeviceCounters[str(numberOfDevices)+"oldstampeinschaltdauer"]
                    except:
                        pass
                #Einschaltzeit des Relais setzen
                if str(numberOfDevices)+"relais" in DeviceValues:
                    if ( DeviceValues[str(numberOfDevices)+"relais"] == 0 ):
                        if ( relais == 1 ):
                            DeviceCounters.update( {str(numberOfDevices) + "eintime" : time.time()})
                    else:
                        if ( relais == 0 ):
                            if str(numberOfDevices) + "eintime" in DeviceCounters:
                                del DeviceCounters[str(numberOfDevices) + "eintime"]
                DeviceValues.update( {str(numberOfDevices) + "relais" : relais})
                devstatus=getstat(numberOfDevices)
                try:
                    runtime=DeviceValues[str(numberOfDevices)+"runningtime"]
                except:
                    runtime=0
                logDebug(LOGLEVELDEBUG, "(" + str(numberOfDevices) + ") " + str(devicename) + " rel: " + str(relais)  +  " oncnt/onstandby/time: " + str(DeviceOn[numberOfDevices-1]) + "/" +  str(DeviceOnStandby[numberOfDevices-1]) + "/" + str(runtime) + " Status: " + str(devstatus) + " akt: " + str(watt) + " Z Hw: " + str(wattk))
            except Exception as e:
                DeviceValues.update( {str(numberOfDevices) : "error"})
                logDebug(LOGLEVELERROR, "Device " + str(switchtyp) + str(numberOfDevices) + str(devicename) + " Fehlermeldung: " + str(e))
    f = open(basePath+'/ramdisk/devicetotal_watt', 'w')
    f.write(str(totalwatt))
    f.close()
    f = open(basePath+'/ramdisk/devicetotal_watt_other', 'w')
    f.write(str(totalwattot))
    f.close()
    f = open(basePath+'/ramdisk/devicetotal_watt_hausmin', 'w')
    f.write(str(totalminhaus))
    f.close()
    logDebug(LOGLEVELDEBUG, "Total Watt abschaltbarer smarthomedevices: " + str(totalwatt)  )
    logDebug(LOGLEVELDEBUG, "Total Watt nichtabschaltbarer smarthomedevices: " + str(totalwattot) )
    logDebug(LOGLEVELDEBUG, "Total Watt nicht im Hausverbrauch: " + str(totalminhaus) )
    publishmqtt()

def turndevicerelais(nummer, zustand,ueberschussberechnung,updatecnt):
    (switchtyp,canswitch) = gettyp(nummer)
    devicename = str(config.get('smarthomedevices', 'device_name_'+str(nummer)))
    try:
        device_einschalturl = str(config.get('smarthomedevices', 'device_einschalturl_'+str(nummer)))
    except:
        device_einschalturl = "undef"
    try:
        device_ausschalturl = str(config.get('smarthomedevices', 'device_ausschalturl_'+str(nummer)))
    except:
        device_ausschalturl = "undef"
    try:
        device_actor = str(config.get('smarthomedevices','device_actor_'+str(nummer)))
    except:
        device_actor = "undef"
    try:
        device_username = str(config.get('smarthomedevices','device_username_'+str(nummer)))
    except:
        device_username = "undef"
    try:
        device_password = str(config.get('smarthomedevices','device_password_'+str(nummer)))
    except:
        device_password = "undef"
    try:
        device_ip = str(config.get('smarthomedevices', 'device_ip_'+str(nummer)))
    except:
        device_ip = "undef"
    pyname0 = getdir(switchtyp,devicename)
    setueb(nummer,ueberschussberechnung)
    (devuberschuss, ueberschussberechnung) = getueb(nummer)
    argumentList = ['python3', "", str(nummer)] # element with index 1 will be set to on.py or off.py
    argumentList.append(device_ip)
    argumentList.append(str(devuberschuss))
    argumentList.append("") # element with index 5 will be set on URL for switch on or off
    argumentList.append(device_actor)
    argumentList.append(device_username)
    argumentList.append(device_password)
    if ( zustand == 1):
        try:
            pyname = pyname0 +"/on.py"
            if os.path.isfile(pyname):
                argumentList[1] = pyname
                argumentList[5] = device_einschalturl
                if updatecnt == 1:
                    DeviceOn[nummer-1]= str(int(DeviceOn[nummer-1])+1)
                else:
                    DeviceOnStandby[nummer-1]= str(int(DeviceOnStandby[nummer-1])+1)
                logDebug(LOGLEVELINFO, "(" + str(nummer) + ") " + str(devicename) + " angeschaltet. Ueberschussberechnung (1 = mit Speicher, 2 = mit Offset) " + str(ueberschussberechnung) + " oncount: " + str(DeviceOn[nummer-1]) + " onstandby: " + str(DeviceOnStandby[nummer-1]) )
                f = open(basePath+'/ramdisk/device' + str(nummer) + '_req_relais', 'w')
                f.write(str(zustand))
                f.close()
                if updatecnt == 1:
                    DeviceCounters.update( {str(nummer) + "eintime" : time.time()})
                proc=subprocess.Popen(argumentList)
                proc.communicate()
            else:
               logDebug(LOGLEVELDEBUG, "Device " + str(switchtyp) + str(nummer) + str(devicename) + " File not found: " + str(pyname))
        except Exception as e:
            logDebug(LOGLEVELERROR, "Fehler beim Einschalten von (" + str(nummer) + ") Fehlermeldung: " + str(e))
    if ( zustand == 0):
        try:
            pyname = pyname0 +"/off.py"
            if os.path.isfile( pyname  ):
                argumentList[1] = pyname
                argumentList[5] = device_ausschalturl
                proc=subprocess.Popen(argumentList)
                proc.communicate()
                logDebug(LOGLEVELINFO, "(" + str(nummer) + ") " + str(devicename) + " ausgeschaltet")
                f = open(basePath+'/ramdisk/device' + str(nummer) + '_req_relais', 'w')
                f.write(str(zustand))
                f.close()
            else:
                logDebug(LOGLEVELDEBUG, "Device " + str(switchtyp) + str(nummer) + str(devicename) + " File not found: " + str(pyname))
        except Exception as e:
            logDebug(LOGLEVELERROR, "Fehler beim Ausschalten von (" + str(nummer) + ") Fehlermeldung: " + str(e))
def conditions(nummer):
    try:
        speichersocbeforestop = int(config.get('smarthomedevices', 'device_speichersocbeforestop_'+str(nummer)))
    except:
        speichersocbeforestop = 100
    try:
        speichersocbeforestart = int(config.get('smarthomedevices', 'device_speichersocbeforestart_'+str(nummer)))
    except:
        speichersocbeforestart = 0
    try:
        deactivatewhileevcharging = int(config.get('smarthomedevices', 'device_deactivatewhileevcharging_'+str(nummer)))
    except:
        deactivatewhileevcharging = 0
    try:
        finishtime = str(config.get('smarthomedevices', 'device_finishtime_'+str(nummer)))
    except:
        finishtime = '00:00'
    try:
        starttimedev = str(config.get('smarthomedevices', 'device_starttime_'+str(nummer)))
    except:
        starttimedev = '00:00'
    try:
        endtime = str(config.get('smarthomedevices', 'device_endtime_'+str(nummer)))
    except:
        endtime = '00:00'
    try:
        startupdetection = int(config.get('smarthomedevices', 'device_startupdetection_'+str(nummer)))
    except:
        startupdetection = 0
    try:
        standbypower = int(config.get('smarthomedevices', 'device_standbypower_'+str(nummer)))
    except:
        standbypower = 0
    try:
        standbyduration = int(config.get('smarthomedevices', 'device_standbyduration_'+str(nummer)))
    except:
        standbyduration = 0
    try:
        ontime = str(config.get('smarthomedevices', 'device_ontime_'+str(nummer)))
    except:
        ontime = '00:00'
    try:
        startupmuldetection = int(config.get('smarthomedevices', 'device_startupmuldetection_'+str(nummer)))
    except:
        startupmuldetection = 0
    file_charge= '/var/www/html/openWB/ramdisk/llkombiniert'
    testcharge = 0
    if os.path.isfile(file_charge):
        f = open( file_charge, 'r')
        testcharge =int(f.read())
        f.close()
    if testcharge <= 1000:
        chargestatus = 0
    else:
        chargestatus = 1
    einschwelle = int(config.get('smarthomedevices', 'device_einschaltschwelle_'+str(nummer)))
    ausschwelle = int(config.get('smarthomedevices', 'device_ausschaltschwelle_'+str(nummer))) * -1
    einverz = int(config.get('smarthomedevices', 'device_einschaltverzoegerung_'+str(nummer))) * 60
    ausverz = int(config.get('smarthomedevices', 'device_ausschaltverzoegerung_'+str(nummer))) * 60
    mineinschaltdauer = int(config.get('smarthomedevices', 'device_mineinschaltdauer_'+str(nummer))) * 60
    maxeinschaltdauer = int(config.get('smarthomedevices', 'device_maxeinschaltdauer_'+str(nummer))) * 60
    name = str(config.get('smarthomedevices', 'device_name_'+str(nummer)))
    #logDebug(LOGLEVELDEBUG,"(" + str(nummer) + ") " + str(name) + " finishtime definiert " + str(finishtime) + ">" + str(DeviceOn[nummer-1]))
    local_time = datetime.now(timezone.utc).astimezone()
    localhour = int(local_time.strftime(format = "%H"))
    localminute = int(local_time.strftime(format = "%M"))
    localinsec = int(( localhour * 60 * 60 )  + (localminute * 60))
    # onnow = 0 -> normale Regelung
    # onnow = 1 -> Zeitpunkt erreciht, immer ein ohne Ueberschuss regelung
    onnow = 0
    if (ontime != '00:00'):
        onhour = int(str("0") +str(ontime).partition(':')[0])
        onminute = int(str(ontime)[-2:] )
        logDebug(LOGLEVELDEBUG,"(" + str(nummer) + ") " + str(name) + " Immer an nach definiert " + str(onhour) + ":" +  str ('%.2d' % onminute) +   " aktuelle Zeit " + str (localhour) + ":" + str ('%.2d' % localminute))
        if ((onhour > localhour )  or  ((onhour == localhour ) and (onminute >=localminute) )):
            pass
        else:
            logDebug(LOGLEVELDEBUG,"(" + str(nummer) + ") " + str(name) + " schalte ein wegen Immer an nach")
            onnow = 1
    if (finishtime != '00:00') and (DeviceOn[nummer-1] ==str("0")):
        finishhour = int(str("0") +str(finishtime).partition(':')[0])
        finishminute = int(str(finishtime)[-2:] )
        startspatsec = int(( finishhour * 60 * 60 )  + (finishminute * 60) - mineinschaltdauer)
        logDebug(LOGLEVELDEBUG,"(" + str(nummer) + ") " + str(name) + " finishtime definiert " + str(finishhour) + ":" +  str ('%.2d' % finishminute) +   " aktuelle Zeit " + str (localhour) + ":" + str ('%.2d' % localminute) + " Anzahl Starts heute 0 Mineinschaltdauer (Sec) " + str (mineinschaltdauer))
        if ((finishhour > localhour )  or  ((finishhour == localhour ) and (finishminute >=localminute) )) and (startspatsec <= localinsec):
            logDebug(LOGLEVELDEBUG,"(" + str(nummer) + ") " + str(name) + " schalte ein wegen finishtime, spaetester start in sec " + str(startspatsec) + " aktuelle sec " + str(localinsec))
            turndevicerelais(nummer, 1,0,1)
            setstat(nummer,30)
            return
    devstatus=getstat(nummer)
    if devstatus == 30:
        logDebug(LOGLEVELDEBUG,"(" + str(nummer) + ") " + str(name) + " finishtime laueft, pruefe Mindestlaufzeit")
        if str(nummer)+"eintime" in DeviceCounters:
            timestart = int(time.time()) - int(DeviceCounters[str(nummer)+"eintime"])
            if ( mineinschaltdauer < timestart):
                logDebug(LOGLEVELINFO,"(" + str(nummer) + ") " + str(name)  + " Mindesteinschaltdauer erreicht, finishtime erreicht")
                setstat(nummer,10)
                return
            else:
                logDebug(LOGLEVELINFO,"(" + str(nummer) + ") " + str(name)  + " finishtime laueft, Mindesteinschaltdauer nicht erreicht, " + str(mineinschaltdauer) + " > " + str(timestart))
                return
        else:
            logDebug(LOGLEVELINFO,"(" + str(nummer) + ") " + str(name)+ " Mindesteinschaltdauer nicht bekannt, finishtime erreicht")
            setstat(nummer,10)
            return
    # here startup device_startupdetection
    if ((startupdetection == 0) or (onnow == 1)) and (devstatus == 20):
        setstat(nummer,10)
        turndevicerelais(nummer, 0,0,1)
        logDebug(LOGLEVELINFO,"(" + str(nummer) + ") " + str(name)  + " Anlauferkennung nun abgeschaltet ")
        return
    #remove condition that device has to be off
    if (startupdetection == 1) and (DeviceOnStandby[nummer-1] ==str("0")) and (DeviceOn[nummer-1] ==str("0")) and (devstatus != 20):
        setstat(nummer,20)
        logDebug(LOGLEVELINFO,"(" + str(nummer) + ") " + str(name)  + " Anlauferkennung nun aktiv, eingeschaltet ")
        turndevicerelais(nummer, 1,0,0)
        return
    if (devstatus == 20):
        if (int(DeviceValues[str(nummer)+"watt"]) > standbypower):
            if  str(nummer)+"anlaufz" in DeviceCounters:
                timesince = int(time.time()) - int(DeviceCounters[str(nummer)+"anlaufz"])
                if ( standbyduration < timesince ):
                    logDebug(LOGLEVELINFO,"(" + str(nummer) + ") " + str(name)  + " standbycheck abgelaufen " + str(standbyduration) + " ,sec pruefe Einschaltschwelle " + str(standbypower))
                    setstat(nummer,10)
                    del DeviceCounters[str(nummer)+"anlaufz"]
                    oldueberschussberechnung = 0
                    devuberschuss = 0
                    ( devuberschuss, oldueberschussberechnung)= getueb(nummer)
                    if (( devuberschuss > einschwelle) or (onnow == 1)):
                        try:
                            del DeviceCounters[str(nummer)+"ausverz"]
                        except:
                            pass
                        try:
                            del DeviceCounters[str(nummer)+"einverz"]
                        except:
                            pass
                        logDebug(LOGLEVELDEBUG,"(" + str(nummer) + ") " + str(config.get('smarthomedevices', 'device_name_'+str(nummer)))+ " Überschuss "  + str(devuberschuss) + " größer Einschaltschwelle oder Immer an zeit erreicht, schalte ein (ohne Einschaltverzoegerung) " + str(einschwelle) )
                        turndevicerelais(nummer, 1,oldueberschussberechnung,1)
                    else:
                        logDebug(LOGLEVELDEBUG,"(" + str(nummer) + ") " + str(config.get('smarthomedevices', 'device_name_'+str(nummer)))+ " Überschuss "  + str(devuberschuss) + " kleiner Einschaltschwelle, schalte aus " + str(einschwelle) )
                        turndevicerelais(nummer, 0,0,1)
                    return
                else:
                    logDebug(LOGLEVELINFO,"(" + str(nummer) + ") " + str(name) + " standbycheck noch nicht erreicht " +  str(standbyduration)+ " > " + str(timesince))
            else:
                    DeviceCounters.update( {str(nummer) + "anlaufz" : time.time()})
                    logDebug(LOGLEVELINFO,"(" + str(nummer) + ") " + str(name) + " standbycheck gestartet " + str (int(DeviceValues[str(nummer)+"watt"]))+  " > " + str(standbypower) )
        else:
            if  str(nummer)+"anlaufz" in DeviceCounters:
                del DeviceCounters[str(nummer)+"anlaufz"]
            logDebug(LOGLEVELINFO,"(" + str(nummer) + ") " + str(name) + " unter standbyschwelle , timer geloescht")
    if ( maxeinschaltdauer > int(DeviceValues[str(nummer)+"runningtime"])):
        logDebug(LOGLEVELDEBUG,"(" + str(nummer) + ") " + str(name) + " Maximale Einschaltdauer nicht erreicht")
    else:
        if ( DeviceValues[str(nummer)+"relais"] == 1 ):
            logDebug(LOGLEVELINFO,"(" + str(nummer) + ") " + str(name) + " Maximale Einschaltdauer erreicht schalte ab")
            turndevicerelais(nummer, 0,0,1)
        else:
            logDebug(LOGLEVELDEBUG,"(" + str(nummer) + ")" + str(name) + " Maximale Einschaltdauer erreicht bereits abgeschaltet")
        return
    # Auto ladung
    if deactivatewhileevcharging == 1:
        if ( DeviceValues[str(nummer)+"relais"] == 1 ):
            logDebug(LOGLEVELDEBUG,"(" + str(nummer) + ") " + str(name) + " Soll reduziert werden bei Ladung, pruefe " + str( testcharge))
            if chargestatus == 1:
                logDebug(LOGLEVELDEBUG,"(" + str(nummer) + ") " + str(name) + " Ladung läuft, pruefe Mindestlaufzeit")
                if str(nummer)+"eintime" in DeviceCounters:
                    timestart = int(time.time()) - int(DeviceCounters[str(nummer)+"eintime"])
                    if ( mineinschaltdauer < timestart):
                        logDebug(LOGLEVELINFO,"(" + str(nummer) + ") " + str(name)  + " Mindesteinschaltdauer erreicht, setze Ausschaltschwelle auf 0")
                        #turndevicerelais(nummer, 0,0,1)
                        #return
                        ausverz = 0
                        if (ausschwelle < 0):
                            ausschwelle = 0
                    else:
                        logDebug(LOGLEVELINFO,"(" + str(nummer) + ") " + str(name)  + " Mindesteinschaltdauer nicht erreicht, " + str(mineinschaltdauer) + " > " + str(timestart))
                else:
                    logDebug(LOGLEVELINFO,"(" + str(nummer) + ") " + str(name)+ " Mindesteinschaltdauer nicht bekannt,setze Ausschaltschwelle auf 0")
                    #turndevicerelais(nummer, 0,0,1)
                    #return
                    ausverz = 0
                    if (ausschwelle < 0):
                        ausschwelle = 0
            else:
                logDebug(LOGLEVELDEBUG,"(" + str(nummer) + ") " + str(name) + " Ladung läuft nicht, pruefe weiter")
        #else:
            #logDebug(LOGLEVELDEBUG,"(" + str(nummer) + ") " + str(name) + " Soll nicht eingeschaltet werden bei Ladung, pruefe " + str( testcharge) )
            #if chargestatus == 1:
                #logDebug(LOGLEVELDEBUG,"(" + str(nummer) + ") " + str(name) + " Ladung läuft, wird nicht eingeschaltet")
                #return
            #else:
                #logDebug(LOGLEVELDEBUG,"(" + str(nummer) + ") " + str(name) + " Ladung läuft nicht, pruefe weiter")
    # Auto ladung ende
    # Art vom ueberschussberechnung pruefen
    ueberschussberechnung = 0
    oldueberschussberechnung = 0
    devuberschuss = 0
    ( devuberschuss, oldueberschussberechnung)= getueb(nummer)
    if (speichersocbeforestart == 0):
        # Berechnung aus, Ueberschuss mit Speicher nehmen
        devuberschuss = uberschuss
        ueberschussberechnung = 1
    else:
        if ( speichersoc < speichersocbeforestart ) and (speichersoc < 97):
            # unter dem Speicher soc, nur EVU Ueberschuss
            # Berechnung mit Ueberschuss nur mit Speicherentladung
            devuberschuss = uberschussoffset
            ueberschussberechnung = 2
        else:
            # sonst drueber oder gleich Speicher soc Berechnung mit Ueberschuss mit Speicher nehmen
            # oder nehmen wenn speicher fast voll
            devuberschuss = uberschuss
            ueberschussberechnung = 1
    if ( oldueberschussberechnung !=  ueberschussberechnung):
        setueb(nummer,ueberschussberechnung)
        logDebug(LOGLEVELDEBUG,"(" + str(nummer) + ") " + str(name)+ " SoC " + str(speichersoc) + " Einschalt SoC " + str(speichersocbeforestart) +  " Ueberschuss " + str(devuberschuss))
        logDebug(LOGLEVELDEBUG,"(" + str(nummer) + ") " + str(name)+ " Ueberschussberechnung anders (1 = mit Speicher, 2 = mit Offset) " + str(ueberschussberechnung))
    if (devstatus == 20):
        logDebug(LOGLEVELINFO,"(" + str(nummer) + ") " + str(name)  + " Anlauferkennung immer noch aktiv, keine Ueberprüfung auf Einschalt oder Ausschaltschwelle ")
        return
    # Device mit Anlauferkennung (mehrfach pro tag) welches im PV Modus ist ?
    if (devstatus == 10) and (startupmuldetection == 1) and (startupdetection == 1) and (int(DeviceOn[nummer-1]) > 0):
        if  str(nummer)+"eintime" in DeviceCounters:
            timestart = int(time.time()) - int(DeviceCounters[str(nummer)+"eintime"])
            if ( mineinschaltdauer < timestart):
                logDebug(LOGLEVELINFO,"(" + str(nummer) + ") " + str(name)  + " Mindesteinschaltdauer erreicht, restarte Anlauferkennung ")
                del DeviceCounters[str(nummer) + "eintime"]
                setstat(nummer,20)
                DeviceOnStandby[nummer-1] = str("0")
                DeviceOn[nummer-1] = str("0")
                logDebug(LOGLEVELINFO,"(" + str(nummer) + ") " + str(name)  + " Anlauferkennung nun aktiv, eingeschaltet ")
                turndevicerelais(nummer, 1,0,0)
                return
        else:
            logDebug(LOGLEVELINFO,"(" + str(nummer) + ") " + str(name)+ " Mindesteinschaltdauer nicht bekannt, restarte Anlauferkennung ")
            setstat(nummer,20)
            DeviceOnStandby[nummer-1] = str("0")
            DeviceOn[nummer-1] = str("0")
            logDebug(LOGLEVELINFO,"(" + str(nummer) + ") " + str(name)  + " Anlauferkennung nun aktiv, eingeschaltet ")
            turndevicerelais(nummer, 1,0,0)
            return
    if (( devuberschuss > einschwelle) or (onnow == 1)):
        try:
            del DeviceCounters[str(nummer)+"ausverz"]
        except:
            pass
        logDebug(LOGLEVELDEBUG,"(" + str(nummer) + ") " + str(config.get('smarthomedevices', 'device_name_'+str(nummer)))+ " Überschuss "  + str(devuberschuss) + " größer Einschaltschwelle oder Immer an zeit erreicht " + str(einschwelle) )
        if ( DeviceValues[str(nummer)+"relais"] == 0 ):
            #speichersocbeforestart
            #if ( speichersoc < speichersocbeforestart ):
            #    logDebug(LOGLEVELINFO,"(" + str(nummer) + ") " + str(name)+ " SoC " + str(speichersoc) + " kleiner als Einschalt SoC " + str(speichersocbeforestart) + " , schalte Gerät nicht ein")
            #    return
            #else:
            #    logDebug(LOGLEVELINFO,"(" + str(nummer) + ") " + str(name)+ " SoC " + str(speichersoc) + " grösser gleich als Einschalt SoC " + str(speichersocbeforestart) + " , pruefe weiter")
            logDebug(LOGLEVELDEBUG,"(" + str(nummer) + ") " + str(name)+ " SoC " + str(speichersoc) + " Einschalt SoC " + str(speichersocbeforestart) + " Ueberschuss " + str(devuberschuss))
            logDebug(LOGLEVELDEBUG,"(" + str(nummer) + ") " + str(name)+ " Ueberschussberechnung (1 = mit Speicher, 2 = mit Offset) " + str(ueberschussberechnung))
            #check for valid time frame
            #starttimedev
            #endtime
            if (starttimedev != '00:00'):
                starthour = int(str("0") +str(starttimedev).partition(':')[0])
                startminute = int(str(starttimedev)[-2:] )
                logDebug(LOGLEVELDEBUG,"(" + str(nummer) + ") " + str(name) + " Fruehster Start um definiert " + str(starthour) + ":" +  str ('%.2d' % startminute) +   " aktuelle Zeit " + str (localhour) + ":" + str ('%.2d' % localminute))
                if ((starthour > localhour )  or  ((starthour == localhour ) and (startminute >=localminute) )):
                    logDebug(LOGLEVELDEBUG,"(" + str(nummer) + ") " + str(name) + " Fruehster Start noch nicht erreicht ")
                    return
            if (endtime != '00:00'):
                endhour = int(str("0") +str(endtime).partition(':')[0])
                endminute = int(str(endtime)[-2:] )
                logDebug(LOGLEVELDEBUG,"(" + str(nummer) + ") " + str(name) + " Spaetester Start um definiert " + str(endhour) + ":" +  str ('%.2d' % endminute) +   " aktuelle Zeit " + str (localhour) + ":" + str ('%.2d' % localminute))
                if ((endhour > localhour )  or  ((endhour == localhour ) and (endminute >=localminute) )):
                    pass
                else:
                    logDebug(LOGLEVELDEBUG,"(" + str(nummer) + ") " + str(name) + " Spaetester Start vorbei ")
                    return
            #speichersocbeforestart
            if  str(nummer)+"einverz" in DeviceCounters:
                timesince = int(time.time()) - int(DeviceCounters[str(nummer)+"einverz"])
                if ( einverz < timesince ):
                    logDebug(LOGLEVELINFO,"(" + str(nummer) + ") " + str(name)  + " Einschaltverzögerung erreicht, schalte ein " + str(einschwelle))
                    turndevicerelais(nummer, 1,ueberschussberechnung,1)
                    del DeviceCounters[str(nummer)+"einverz"]
                else:
                    logDebug(LOGLEVELINFO,"(" + str(nummer) + ") " + str(name) + " Einschaltverzögerung nicht erreicht. " + str(einverz) + " > " + str(timesince))
            else:
                DeviceCounters.update( {str(nummer) + "einverz" : time.time()})
                logDebug(LOGLEVELINFO,"(" + str(nummer) + ") " + str(name) + " Einschaltverzögerung gestartet")
        else:
            logDebug(LOGLEVELDEBUG,"(" + str(nummer) + ") " + str(name)+ " Einschaltverzögerung erreicht, bereits ein")
            try:
                del DeviceCounters[str(nummer)+"einverz"]
            except:
                pass
    else:
        try:
            del DeviceCounters[str(nummer)+"einverz"]
        except:
            pass
        if (devuberschuss < ausschwelle) :
            if ( speichersoc > speichersocbeforestop ):
                logDebug(LOGLEVELDEBUG,"(" + str(nummer) + ") " + str(name)+ " SoC höher als Abschalt SoC, lasse Gerät weiterlaufen")
                return
            else:
                logDebug(LOGLEVELDEBUG,"(" + str(nummer) + ") " + str(name)+ " SoC niedriger als Abschalt SoC, prüfe weiter")
            logDebug(LOGLEVELDEBUG,"(" + str(nummer) + ") " + str(name)+ " Überschuss " + str(devuberschuss)  + " kleiner Ausschaltschwelle " + str(ausschwelle))
            if ( DeviceValues[str(nummer)+"relais"] == 1 ):
                if  str(nummer)+"ausverz" in DeviceCounters:
                    timesince = int(time.time()) - int(DeviceCounters[str(nummer)+"ausverz"])
                    if ( ausverz < timesince ):
                        if  str(nummer)+"eintime" in DeviceCounters:
                            timestart = int(time.time()) - int(DeviceCounters[str(nummer)+"eintime"])
                            if ( mineinschaltdauer < timestart):
                                logDebug(LOGLEVELINFO,"(" + str(nummer) + ") " + str(name)  + " Ausschaltverzögerung & Mindesteinschaltdauer erreicht, schalte aus " + str(ausschwelle))
                                turndevicerelais(nummer, 0,0,1)
                                del DeviceCounters[str(nummer)+"ausverz"]
                            else:
                                logDebug(LOGLEVELINFO,"(" + str(nummer) + ") " + str(name)  + " Ausschaltverzögerung erreicht, Mindesteinschaltdauer nicht erreicht, " + str(mineinschaltdauer) + " > " + str(timestart))
                        else:
                            logDebug(LOGLEVELINFO,"(" + str(nummer) + ") " + str(name)+ " Mindesteinschaltdauer nicht bekannt, schalte aus")
                            turndevicerelais(nummer, 0,0,1)
                    else:
                        logDebug(LOGLEVELINFO,"(" + str(nummer) + ") " + str(name) + " Ausschaltverzögerung nicht erreicht. " + str(ausverz) + " > " + str(timesince))
                else:
                    DeviceCounters.update( {str(nummer) + "ausverz" : time.time()})
                    logDebug(LOGLEVELINFO,"(" + str(nummer) + ") " + str(name) + " Ausschaltverzögerung gestartet")
            else:
                logDebug(LOGLEVELDEBUG,"(" + str(nummer) + ") " + str(name)+ " Ausschaltverzögerung erreicht, bereits aus")
                try:
                    del DeviceCounters[str(nummer)+"ausverz"]
                except:
                    pass
        else:
            logDebug(LOGLEVELDEBUG,"(" + str(nummer) + ") " + str(name) + " Überschuss kleiner als Einschaltschwelle und größer als Ausschaltschwelle. Ueberschuss " + str(devuberschuss) )
            try:
                del DeviceCounters[str(nummer)+"einverz"]
            except:
                pass
            try:
                del DeviceCounters[str(nummer)+"ausverz"]
            except:
                pass

def resetmaxeinschaltdauerfunc():
    global resetmaxeinschaltdauer
    global numberOfSupportedDevices
    hour=time.strftime("%H")
    if (int(hour) == 0):
        try:
            if (int(resetmaxeinschaltdauer) == 0):
                for i in range(1, (numberOfSupportedDevices+1)):
                    DeviceValues.update({str(i) + "runningtime" : '0'})
                    DeviceTempValues.update({'oldtime'+str(i) : '2'})
                    logDebug(LOGLEVELINFO, "(" + str(i) + ") RunningTime auf 0 gesetzt")
                    DeviceOn[i-1]= str("0")
                    devstatus=getstat(i)
                    #Sofern Anlauferkennung laueft counter nicht zuruecksetzen
                    if (devstatus != 20):
                        DeviceOnStandby[i-1]= str("0")
                    try:
                        del DeviceCounters[str(i)+"oldstampeinschaltdauer"]
                    except:
                        pass
                resetmaxeinschaltdauer=1
        except:
            resetmaxeinschaltdauer=0
    if (int(hour) == 1):
        resetmaxeinschaltdauer=0

client = mqtt.Client("openWB-mqttsmarthome")
client.on_connect = on_connect
client.on_message = on_message
startTime = time.time()
waitTime = 5
client.connect("localhost")
while True:
    client.loop()
    #client.subscribe("openWB/SmartHome/#", 2)
    elapsedTime = time.time() - startTime
    if elapsedTime > waitTime:
        client.disconnect()
        break
time.sleep(5)
while True:
    config.read(shconfigfile)
    bootdone = checkbootdone()
    if (bootdone == 1):
        loadregelvars()
        getdevicevalues()
        resetmaxeinschaltdauerfunc()
        for i in range(1, (numberOfSupportedDevices+1)):
            try:
                configured = config.get('smarthomedevices', 'device_configured_' + str(i))
                if (configured == "1"):
                    if ( DeviceValues[str(i)+"manual"] == 1 ):
                        if ( DeviceValues[str(i)+"manualmodevar"] == 0 ):
                            if ( DeviceValues[str(i)+"relais"] == 1 ):
                                turndevicerelais(i, 0,0,1)
                        if ( DeviceValues[str(i)+"manualmodevar"] == 1 ):
                            if ( DeviceValues[str(i)+"relais"] == 0 ):
                                turndevicerelais(i, 1,0,1)
                        DeviceCounters.update( {str(i) + "mantime" : time.time()})
                        logDebug(LOGLEVELDEBUG,"(" + str(i) + ") " + str(config.get('smarthomedevices', 'device_name_'+str(i))) + " manueller Modus aktiviert, keine Regelung")
                    else:
                        (switchtyp,canswitch) = gettyp(i)
                        try:
                            if canswitch == 1:
                                conditions(int(i))
                        except Exception as e:
                            logDebug(LOGLEVELERROR, "Conditions (" + str(i) + ") " + str(config.get('smarthomedevices', 'device_name_'+str(i))) + " Fehlermeldung: " + str(e))
            except Exception as e:
                logDebug(LOGLEVELERROR, "Main routine (" + str(i) + ") " + str(config.get('smarthomedevices', 'device_name_'+str(i))) + " Fehlermeldung: " + str(e))
    #conditions(2)
    #if "2eintime" in DeviceCounters:
    #    print(DeviceCounters["2eintime"])
    time.sleep(5)
    #except:
    #exit()
