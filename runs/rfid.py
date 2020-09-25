#!/usr/bin/python
import argparse
import paho.mqtt.client as mqtt
import sys
import os 
import time 
import datetime
import getopt 
import socket 
import struct 
import binascii 
import RPi.GPIO as GPIO
loglevel=1
counter=0
Values = { }
Values.update({'newplugstatlp1' : str(0)})
Values.update({'newplugstatlp2' : str(0)})
Values.update({'newplugstatlp3' : str(0)})
Values.update({'newplugstatlp4' : str(0)})
Values.update({'oldplugstatlp1' : str(0)})
Values.update({'oldplugstatlp2' : str(0)})
Values.update({'oldplugstatlp3' : str(0)})
Values.update({'oldplugstatlp4' : str(0)})
Values.update({'lastpluggedlp' : str(0)})
Values.update({'lastscannedtag' : str(0)})
def logDebug(level, msg): 
    if (int(level) >= int(loglevel)): 
        file = open('/var/www/html/openWB/ramdisk/rfid.log', 'a') 
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
readrfidlist()
def getplugstat():

    
    try:
        with open('ramdisk/plug1stat', 'r') as value:
            Values.update({'newplugstatlp1' : int(value.read())})
        if ( Values["oldplugstatlp1"] != Values["newplugstatlp1"] ):
            if ( Values["newplugstatlp1"] == 1 ):
                Values.update({'lastpluggedlp' : str(1)})
                logDebug(1, str("Angesteckt an LP1"))
            else:
                logDebug(1, str("Abgesteckt, Sperre LP1"))
            Values.update({"oldplugstatlp1" : Values["newplugstatlp1"]})
    except:
        pass
    try:
        with open('ramdisk/plug2stat', 'r') as value:
            Values.update({'newplugstatlp2' : int(value.read())})
        if ( Values["oldplugstatlp2"] != Values["newplugstatlp2"] ):
            if ( Values["newplugstatlp2"] == 1 ):
                Values.update({'lastpluggedlp' : str(2)})
                logDebug(1, str("Angesteckt an LP2"))
            else:
                logDebug(1, str("Abgesteckt, Sperre LP2"))
            Values.update({"oldplugstatlp2" : Values["newplugstatlp2"]})
    except:
        pass
    try:
        with open('ramdisk/plug3stat', 'r') as value:
            Values.update({'newplugstatlp3' : int(value.read())})
        if ( Values["oldplugstatlp3"] != Values["newplugstatlp3"] ):
            if ( Values["newplugstatlp3"] == 1 ):
                Values.update({'lastpluggedlp' : str(3)})
                logDebug(1, str("Angesteckt an LP3"))
            else:
                logDebug(1, str("Abgesteckt, Sperre LP3"))
            Values.update({"oldplugstatlp3" : Values["newplugstatlp3"]})
    except:
        pass
    try:
        with open('ramdisk/plug4stat', 'r') as value:
            Values.update({'newplugstatlp4' : int(value.read())})
        if ( Values["oldplugstatlp4"] != Values["newplugstatlp4"] ):
            if ( Values["newplugstatlp4"] == 1 ):
                Values.update({'lastpluggedlp' : str(4)})
                logDebug(1, str("Angesteckt an LP4"))
            else:
                logDebug(1, str("Abgesteckt, Sperre LP4"))
            Values.update({"oldplugstatlp4" : Values["newplugstatlp4"]})
    except:
        pass
    logDebug(1, str("Plugstat:" + str(Values["newplugstatlp1"]) + str(Values["newplugstatlp2"]) + str(Values["newplugstatlp3"]) + str(Values["newplugstatlp4"])))
def conditions():
    if ( Values["lastpluggedlp"] != "0"):
        logDebug(1, str(Values["lastpluggedlp"]) + str("prüfe auf rfid scan"))
        try:
            with open('ramdisk/readtag', 'r') as value:
                Values.update({'lastscannedtag' : int(value.read())})
            if ( Values["lastscannedtag"] != "0"):
                for i in rfidlist:
                    if (str(i) == str(Values["lastscannedtag"])):
                        logDebug(1, str("Schalte Ladepunkt: ") + str(Values["lastpluggedlp"]) + str("frei"))
                        f = open('/var/www/html/openWB/ramdisk/rfidlp' + str(Values["lastpluggedlp"]), 'w')
                        f.write(str(Values["lastscannedtag"]))
                        f.close()
                        logDebug(1, str("Schreibe Tag zu Ladepunkt"))
                        Values.update({'lastpluggedlp' : "0"})
                        f = open('/var/www/html/openWB/ramdisk/readtag', 'w')
                        f.write(str(0))
                        f.close()
        except:
            pass     
def clearoldrfidtag():
    t = os.path.getmtime('/var/www/html/openWB/ramdisk/readtag')
    timediff = time.time() - t
    if timediff > 300:
        logDebug(1, str("Verwerfe Tag") + str(timediff))
        f = open('/var/www/html/openWB/ramdisk/readtag', 'w')
        f.write(str("0"))
        f.close()

while True:
    getplugstat()
    conditions()    
    clearoldrfidtag()
    counter= counter + 1
    if ( counter > 10 ):
        readrfidlist()
        counter = 0
    time.sleep(2)
