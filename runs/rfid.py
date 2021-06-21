#!/usr/bin/python
import paho.mqtt.client as mqtt
import os 
import time 

os.chdir('/var/www/html/openWB/')
loglevel=1
counter=0
Values = { }
Values.update({'newplugstatlp1' : str(0)})
Values.update({'newplugstatlp2' : str(0)})
Values.update({'newplugstatlp3' : str(0)})
Values.update({'newplugstatlp4' : str(0)})
Values.update({'newplugstatlp5' : str(0)})
Values.update({'newplugstatlp6' : str(0)})
Values.update({'newplugstatlp7' : str(0)})
Values.update({'newplugstatlp8' : str(0)})
Values.update({'oldplugstatlp1' : str(0)})
Values.update({'oldplugstatlp2' : str(0)})
Values.update({'oldplugstatlp3' : str(0)})
Values.update({'oldplugstatlp4' : str(0)})
Values.update({'oldplugstatlp5' : str(0)})
Values.update({'oldplugstatlp6' : str(0)})
Values.update({'oldplugstatlp7' : str(0)})
Values.update({'oldplugstatlp8' : str(0)})
Values.update({'lastpluggedlp' : str(0)})
Values.update({'lastscannedtag' : str(0)})
Values.update({'rfidlasttag' : str(0)})

def logDebug(level, msg): 
    if (int(level) >= int(loglevel)): 
        file = open('ramdisk/rfid.log', 'a') 
        if (int(level) == 0): 
            file.write(time.ctime() + ': ' + str(msg)+ '\n') 
        if (int(level) == 1): 
            file.write(time.ctime() + ': ' + str(msg)+ '\n') 
        if (int(level) == 2): 
            file.write(time.ctime() + ': ' + str('\x1b[6;30;42m' + msg + '\x1b[0m')+ '\n') 
        file.close()

def readrfidlist():
    global rfidlist
    with open('ramdisk/rfidlist', 'r') as value:
        rfidstring = str(value.read())
    rfidlist=rfidstring.rstrip().split(",") 

def getplugstat():
    try:
        with open('ramdisk/plugstat', 'r') as value:
            Values.update({'newplugstatlp1' : int(value.read())})
        if ( Values["oldplugstatlp1"] != Values["newplugstatlp1"] ):
            if ( Values["newplugstatlp1"] == 1 ):
                Values.update({'lastpluggedlp' : str(1)})
                logDebug(1, str("Angesteckt an LP1"))
            else:
                logDebug(1, str("Abgesteckt, Sperre LP1"))
                f = open('ramdisk/lp1enabled', 'w')
                f.write(str("0"))
                f.close()
            Values.update({"oldplugstatlp1" : Values["newplugstatlp1"]})
    except:
        pass
    try:
        with open('ramdisk/plugstats1', 'r') as value:
            Values.update({'newplugstatlp2' : int(value.read())})
        if ( Values["oldplugstatlp2"] != Values["newplugstatlp2"] ):
            if ( Values["newplugstatlp2"] == 1 ):
                Values.update({'lastpluggedlp' : str(2)})
                logDebug(1, str("Angesteckt an LP2"))
            else:
                logDebug(1, str("Abgesteckt, Sperre LP2"))
                f = open('ramdisk/lp2enabled', 'w')
                f.write(str("0"))
                f.close()
            Values.update({"oldplugstatlp2" : Values["newplugstatlp2"]})
    except:
        pass
    try:
        with open('ramdisk/plugstatlp3', 'r') as value:
            Values.update({'newplugstatlp3' : int(value.read())})
        if ( Values["oldplugstatlp3"] != Values["newplugstatlp3"] ):
            if ( Values["newplugstatlp3"] == 1 ):
                Values.update({'lastpluggedlp' : str(3)})
                logDebug(1, str("Angesteckt an LP3"))
            else:
                logDebug(1, str("Abgesteckt, Sperre LP3"))
                f = open('ramdisk/lp3enabled', 'w')
                f.write(str("0"))
                f.close()
            Values.update({"oldplugstatlp3" : Values["newplugstatlp3"]})
    except:
        pass
    try:
        with open('ramdisk/plugstatlp4', 'r') as value:
            Values.update({'newplugstatlp4' : int(value.read())})
        if ( Values["oldplugstatlp4"] != Values["newplugstatlp4"] ):
            if ( Values["newplugstatlp4"] == 1 ):
                Values.update({'lastpluggedlp' : str(4)})
                logDebug(1, str("Angesteckt an LP4"))
            else:
                logDebug(1, str("Abgesteckt, Sperre LP4"))
                f = open('ramdisk/lp4enabled', 'w')
                f.write(str("0"))
                f.close()
            Values.update({"oldplugstatlp4" : Values["newplugstatlp4"]})
    except:
        pass
    try:
        with open('ramdisk/plugstatlp5', 'r') as value:
            Values.update({'newplugstatlp5' : int(value.read())})
        if ( Values["oldplugstatlp5"] != Values["newplugstatlp5"] ):
            if ( Values["newplugstatlp5"] == 1 ):
                Values.update({'lastpluggedlp' : str(5)})
                logDebug(1, str("Angesteckt an LP5"))
            else:
                logDebug(1, str("Abgesteckt, Sperre LP5"))
                f = open('ramdisk/lp5enabled', 'w')
                f.write(str("0"))
                f.close()
            Values.update({"oldplugstatlp5" : Values["newplugstatlp5"]})
    except:
        pass
    try:
        with open('ramdisk/plugstatlp6', 'r') as value:
            Values.update({'newplugstatlp6' : int(value.read())})
        if ( Values["oldplugstatlp6"] != Values["newplugstatlp6"] ):
            if ( Values["newplugstatlp6"] == 1 ):
                Values.update({'lastpluggedlp' : str(6)})
                logDebug(1, str("Angesteckt an LP6"))
            else:
                logDebug(1, str("Abgesteckt, Sperre LP6"))
                f = open('ramdisk/lp6enabled', 'w')
                f.write(str("0"))
                f.close()
            Values.update({"oldplugstatlp6" : Values["newplugstatlp6"]})
    except:
        pass
    try:
        with open('ramdisk/plugstatlp7', 'r') as value:
            Values.update({'newplugstatlp7' : int(value.read())})
        if ( Values["oldplugstatlp7"] != Values["newplugstatlp7"] ):
            if ( Values["newplugstatlp7"] == 1 ):
                Values.update({'lastpluggedlp' : str(7)})
                logDebug(1, str("Angesteckt an LP7"))
            else:
                logDebug(1, str("Abgesteckt, Sperre LP7"))
                f = open('ramdisk/lp7enabled', 'w')
                f.write(str("0"))
                f.close()
            Values.update({"oldplugstatlp7" : Values["newplugstatlp7"]})
    except:
        pass
    try:
        with open('ramdisk/plugstatlp8', 'r') as value:
            Values.update({'newplugstatlp8' : int(value.read())})
        if ( Values["oldplugstatlp8"] != Values["newplugstatlp8"] ):
            if ( Values["newplugstatlp8"] == 1 ):
                Values.update({'lastpluggedlp' : str(8)})
                logDebug(1, str("Angesteckt an LP8"))
            else:
                logDebug(1, str("Abgesteckt, Sperre LP8"))
                f = open('ramdisk/lp8enabled', 'w')
                f.write(str("0"))
                f.close()
            Values.update({"oldplugstatlp8" : Values["newplugstatlp8"]})
    except:
        pass
    #logDebug(1, str("Plugstat: " + str(Values["newplugstatlp1"]) + str(Values["newplugstatlp2"]) + str(Values["newplugstatlp3"]) + str(Values["newplugstatlp4"]) + str(Values["newplugstatlp5"]) + str(Values["newplugstatlp6"]) + str(Values["newplugstatlp7"]) + str(Values["newplugstatlp8"])))

def conditions():
    if ( Values["lastpluggedlp"] != "0"):
        #logDebug(1, str(Values["lastpluggedlp"]) + str("prüfe auf rfid scan"))
        try:
            with open('ramdisk/readtag', 'r') as value:
                Values.update({'lastscannedtag' : str(value.read().rstrip())})
            if ( Values["lastscannedtag"] != "0"):
                for i in rfidlist:
                    if (str(i) == str(Values["lastscannedtag"])):
                        logDebug(1, str("Schalte Ladepunkt: ") + str(Values["lastpluggedlp"]) + str(" frei"))
                        f = open('ramdisk/lp'+str(Values["lastpluggedlp"])+'enabled', 'w')
                        f.write(str("1"))
                        f.close()
                        f = open('ramdisk/rfidlp' + str(Values["lastpluggedlp"]), 'w')
                        f.write(str(Values["lastscannedtag"]))
                        f.close()
                        logDebug(1, str("Schreibe Tag: ")+str(Values["lastscannedtag"])+str(" zu Ladepunkt"))
                        Values.update({'lastpluggedlp' : "0"})
                        f = open('ramdisk/readtag', 'w')
                        f.write(str(0))
                        f.close()
        except Exception as e:
            logDebug(1, str(e))
            pass

def savelastrfidtag():
    with open('ramdisk/readtag', 'r') as readtagfile:
        readtag = str( readtagfile.read().rstrip() )
    if ( ( readtag != Values["rfidlasttag"] ) and ( readtag != "0" ) ):
        logDebug(1, str("savelastrfidtag: change detected, updating ramdisk: ") + str(readtag))
        f = open('ramdisk/rfidlasttag', 'w')
        f.write(readtag + str(",") + str(os.path.getmtime('ramdisk/readtag')))
        f.close()
        Values.update({'rfidlasttag' : readtag})

def clearoldrfidtag():
    t = os.path.getmtime('ramdisk/readtag')
    timediff = time.time() - t
    if timediff > 300:
        logDebug(1, str("Verwerfe Tag nach ") + str(timediff) + str(" Sekunden"))
        f = open('ramdisk/readtag', 'w')
        f.write(str("0"))
        f.close()

readrfidlist()

while True:
    getplugstat()
    conditions()
    savelastrfidtag()
    clearoldrfidtag()
    counter= counter + 1
    if ( counter > 10 ):
        readrfidlist()
        counter = 0
    time.sleep(2)
