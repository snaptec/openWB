import paho.mqtt.client as mqtt
from subprocess import run
import os
import sys
import subprocess
import time
import fileinput
from datetime import datetime
import configparser
import re
import threading
global inaction
inaction=0
openwbconffile = "/var/www/html/openWB/openwb.conf"
config = configparser.ConfigParser()
shconfigfile='/var/www/html/openWB/smarthome.ini'
config.read(shconfigfile)
numberOfSupportedDevices=9 # limit number of smarthome devices
lock=threading.Lock()

for i in range(1,(numberOfSupportedDevices+1)):
    try:
        confvar = config.get('smarthomedevices', 'device_configured_' + str(i))
    except:
        try:
            config.set('smarthomedevices', 'device_configured_' + str(i), str(0))
        except:
            config.add_section('smarthomedevices')
            config.set('smarthomedevices', 'device_configured_' + str(i), str(0))
with open(shconfigfile, 'w') as f:
    config.write(f)

def writetoconfig(configpart,section,key,value):
    config.read(configpart)
    try:
        config.set(section, key, value)
    except:
        config.add_section(section)
        config.set(section, key, value)
    with open(configpart, 'w') as f:
        config.write(f)
    try:
        f = open('/var/www/html/openWB/ramdisk/reread'+str(section), 'w+')
        f.write(str(1))
        f.close()
    except Exception as e:
        print(str(e))

def replaceAll(changeval,newval):
    global inaction
    if ( inaction == 0 ):
        inaction=1
        for line in fileinput.input(openwbconffile, inplace=1):
            if line.startswith(changeval):
                line = changeval + newval + "\n"
            sys.stdout.write(line)
        time.sleep(0.1)
        inaction=0

def getConfigValue(key):
    for line in fileinput.input(openwbconffile):
        if line.startswith(str(key+"=")):
            return line.split("=", 1)[1]
    return

def getserial():
    # Extract serial from cpuinfo file
    with open('/proc/cpuinfo','r') as f:
        for line in f:
            if line[0:6] == 'Serial':
                return line[10:26]
        return "0000000000000000"

mqtt_broker_ip = "localhost"
client = mqtt.Client("openWB-mqttsub-" + getserial())
ipallowed='^[0-9.]+$'
nameallowed='^[a-zA-Z ]+$'
namenumballowed='^[0-9a-zA-Z ]+$'

# connect to broker and subscribe to set topics
def on_connect(client, userdata, flags, rc):
    #subscribe to all set topics
    #client.subscribe("openWB/#", 2)
    client.subscribe("openWB/set/#", 2)
    client.subscribe("openWB/config/set/#", 2)

# handle each set topic
def on_message(client, userdata, msg):
    global numberOfSupportedDevices
    # log all messages before any error forces this process to die
    if (len(msg.payload.decode("utf-8")) >= 1):
        lock.acquire()
        try:
            setTopicCleared = False
            theTime = datetime.now()
            timestamp = theTime.strftime(format = "%Y-%m-%d %H:%M:%S")
            file = open('/var/www/html/openWB/ramdisk/mqtt.log', 'a')
            file.write( "%s Topic: %s Message: %s\n" % (timestamp, msg.topic, str(msg.payload.decode("utf-8"))) )
            file.close()

            if (( "openWB/set/lp" in msg.topic) and ("ChargePointEnabled" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= 8 and 0 <= int(msg.payload) <= 1):
                    f = open('/var/www/html/openWB/ramdisk/lp'+str(devicenumb)+'enabled', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    client.publish("openWB/lp/"+str(devicenumb)+"/ChargePointEnabled", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (( "openWB/set/lp" in msg.topic) and ("ForceSoCUpdate" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= 2 and int(msg.payload) == 1):
                    if ( int(devicenumb) == 1 ):
                        soctimerfile = '/var/www/html/openWB/ramdisk/soctimer'
                    elif ( int(devicenumb) == 2 ):
                        soctimerfile = '/var/www/html/openWB/ramdisk/soctimer1'
                    f = open(soctimerfile, 'w')
                    f.write("20005")
                    f.close()
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_configured" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices and 0 <= int(msg.payload) <= 1):
                    writetoconfig(shconfigfile,'smarthomedevices','device_configured_'+str(devicenumb),msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_configured", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_canSwitch" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices and 0 <= int(msg.payload) <= 1):
                    writetoconfig(shconfigfile,'smarthomedevices','device_canSwitch_'+str(devicenumb),msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_canSwitch", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_differentMeasurement" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices and 0 <= int(msg.payload) <= 1):
                    writetoconfig(shconfigfile,'smarthomedevices','device_differentMeasurement_'+str(devicenumb),msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_differentMeasurement", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_ip" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices and len(str(msg.payload.decode("utf-8"))) > 6 and bool(re.match(ipallowed, msg.payload.decode("utf-8")))):
                    writetoconfig(shconfigfile,'smarthomedevices','device_ip_'+str(devicenumb), msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_ip", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_measureip" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices and len(str(msg.payload.decode("utf-8"))) > 6 and bool(re.match(ipallowed, msg.payload.decode("utf-8")))):
                    writetoconfig(shconfigfile,'smarthomedevices','device_measureip_'+str(devicenumb), msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_measureip", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_name" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices and  3 <= len(str(msg.payload.decode("utf8"))) <= 12 and bool(re.match(nameallowed, msg.payload.decode("utf-8")))):
                    writetoconfig(shconfigfile,'smarthomedevices','device_name_'+str(devicenumb), msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_name", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_type" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                validDeviceTypes = ['none','shelly','tasmota','acthor','elwa','idm','stiebel','http','avm','mystrom','viessmann','mqtt','pyt'] # 'pyt' is deprecated and will be removed!
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices and len(str(msg.payload.decode("utf-8"))) > 2):
                    try:
                        # just check vor payload in list, deviceTypeIndex is not used
                        deviceTypeIndex = validDeviceTypes.index(msg.payload.decode("utf-8"))
                    except ValueError:
                        pass
                    else:
                        writetoconfig(shconfigfile,'smarthomedevices','device_type_'+str(devicenumb), msg.payload.decode("utf-8"))
                        client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_type", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_measureType" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                validDeviceMeasureTypes = ['shelly','http','mystrom','sdm630','we514','fronius','json','avm','mqtt','sdm120','smaem'] # 'pyt' is deprecated and will be removed!
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices and len(str(msg.payload.decode("utf-8"))) > 2):
                    try:
                        deviceMeasureTypeIndex = validDeviceMeasureTypes.index(msg.payload.decode("utf-8"))
                    except ValueError:
                        pass
                    else:
                        writetoconfig(shconfigfile,'smarthomedevices','device_measuretype_'+str(devicenumb), msg.payload.decode("utf-8"))
                        client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_measureType", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_temperatur_configured" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices and 0 <= int(msg.payload) <= 3):
                    writetoconfig(shconfigfile,'smarthomedevices','device_temperatur_configured_'+str(devicenumb), msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_temperatur_configured", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_einschaltschwelle" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices and -100000 <= int(msg.payload) <= 100000):
                    writetoconfig(shconfigfile,'smarthomedevices','device_einschaltschwelle_'+str(devicenumb), msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_einschaltschwelle", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_deactivateWhileEvCharging" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices and 0 <= int(msg.payload) <= 1):
                    writetoconfig(shconfigfile,'smarthomedevices','device_deactivateWhileEvCharging_'+str(devicenumb), msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_deactivateWhileEvCharging", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_ausschaltschwelle" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices and -100000 <= int(msg.payload) <= 100000):
                    writetoconfig(shconfigfile,'smarthomedevices','device_ausschaltschwelle_'+str(devicenumb), msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_ausschaltschwelle", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_ausschaltverzoegerung" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices and 0 <= int(msg.payload) <= 10000):
                    writetoconfig(shconfigfile,'smarthomedevices','device_ausschaltverzoegerung_'+str(devicenumb), msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_ausschaltverzoegerung", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_einschaltverzoegerung" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices and 0 <= int(msg.payload) <= 100000):
                    writetoconfig(shconfigfile,'smarthomedevices','device_einschaltverzoegerung_'+str(devicenumb), msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_einschaltverzoegerung", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_measureid" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices and 1 <= int(msg.payload) <= 255):
                    writetoconfig(shconfigfile,'smarthomedevices','device_measureid_'+str(devicenumb), msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_measureid", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_speichersocbeforestart" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices and 0 <= int(msg.payload) <= 100):
                    writetoconfig(shconfigfile,'smarthomedevices','device_speichersocbeforestart_'+str(devicenumb), msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_speichersocbeforestart", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_speichersocbeforestop" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices and 0 <= int(msg.payload) <= 100):
                    writetoconfig(shconfigfile,'smarthomedevices','device_speichersocbeforestop_'+str(devicenumb), msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_speichersocbeforestop", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_maxeinschaltdauer" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices and 0 <= int(msg.payload) <= 100000):
                    writetoconfig(shconfigfile,'smarthomedevices','device_maxeinschaltdauer_'+str(devicenumb), msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_maxeinschaltdauer", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_mineinschaltdauer" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices and 0 <= int(msg.payload) <= 100000):
                    writetoconfig(shconfigfile,'smarthomedevices','device_mineinschaltdauer_'+str(devicenumb), msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_mineinschaltdauer", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_manual_control" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices and 0 <= int(msg.payload) <= 1):
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_manual_control", msg.payload.decode("utf-8"), qos=0, retain=True)
                    f = open('/var/www/html/openWB/ramdisk/smarthome_device_manual_control_'+str(devicenumb), 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("mode" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices and 0 <= int(msg.payload) <= 1):
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/mode", msg.payload.decode("utf-8"), qos=0, retain=True)
                    f = open('/var/www/html/openWB/ramdisk/smarthome_device_manual_'+str(devicenumb), 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_einschalturl" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices ):
                    writetoconfig(shconfigfile,'smarthomedevices','device_einschalturl_'+str(devicenumb), msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_einschalturl", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_ausschalturl" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices ):
                    writetoconfig(shconfigfile,'smarthomedevices','device_ausschalturl_'+str(devicenumb), msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_ausschalturl", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_leistungurl" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices ):
                    writetoconfig(shconfigfile,'smarthomedevices','device_leistungurl_'+str(devicenumb), msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_leistungurl", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_measureurlc" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices ):
                    if ( msg.payload.decode("utf-8") == "none"):
                        # print("received message 'none'")
                        client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_measureurlc", "", qos=0, retain=True)
                    else:
                        client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_measureurlc", msg.payload.decode("utf-8"), qos=0, retain=True)
                    writetoconfig(shconfigfile,'smarthomedevices','device_measureurlc_'+str(devicenumb), msg.payload.decode("utf-8"))
            elif (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_measureurl" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices ):
                    writetoconfig(shconfigfile,'smarthomedevices','device_measureurl_'+str(devicenumb), msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_measureurl", msg.payload.decode("utf-8"), qos=0, retain=True)
            elif (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_measurejsonurl" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices ):
                    writetoconfig(shconfigfile,'smarthomedevices','device_measurejsonurl_'+str(devicenumb), msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_measurejsonurl", msg.payload.decode("utf-8"), qos=0, retain=True)
            elif (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_measurejsonpower" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices ):
                    writetoconfig(shconfigfile,'smarthomedevices','device_measurejsonpower_'+str(devicenumb), msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_measurejsonpower", msg.payload.decode("utf-8"), qos=0, retain=True)
            elif (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_measurejsoncounter" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices ):
                    writetoconfig(shconfigfile,'smarthomedevices','device_measurejsoncounter_'+str(devicenumb), msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_measurejsoncounter", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_username" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices ):
                    writetoconfig(shconfigfile,'smarthomedevices','device_username_'+str(devicenumb), msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_username", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_password" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices ):
                    writetoconfig(shconfigfile,'smarthomedevices','device_password_'+str(devicenumb), msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_password", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_actor" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices ):
                    writetoconfig(shconfigfile,'smarthomedevices','device_actor_'+str(devicenumb), msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_actor", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_measureavmusername" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices ):
                    writetoconfig(shconfigfile,'smarthomedevices','device_measureavmusername_'+str(devicenumb), msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_measureavmusername", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_measureavmpassword" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices ):
                    writetoconfig(shconfigfile,'smarthomedevices','device_measureavmpassword_'+str(devicenumb), msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_measureavmpassword", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_measureavmactor" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices ):
                    writetoconfig(shconfigfile,'smarthomedevices','device_measureavmactor_'+str(devicenumb), msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_measureavmactor", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_acthortype" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                validDeviceTypes = ['M1','M3','9s']
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices and len(str(msg.payload.decode("utf-8"))) == 2):
                    try:
                        # just check vor payload in list, deviceTypeIndex is not used
                        deviceTypeIndex = validDeviceTypes.index(msg.payload.decode("utf-8"))
                    except ValueError:
                        pass
                    else:
                        writetoconfig(shconfigfile,'smarthomedevices','device_acthortype_'+str(devicenumb), msg.payload.decode("utf-8"))
                        client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_acthortype", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_acthorpower" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices and 0 <= int(msg.payload) <= 9000 ):
                    writetoconfig(shconfigfile,'smarthomedevices','device_acthorpower_'+str(devicenumb), msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_acthorpower", msg.payload.decode("utf-8"), qos=0, retain=True)

            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_finishTime" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices and re.search(r'^([01]{0,1}\d|2[0-3]):[0-5]\d$', msg.payload.decode("utf-8") ) ):
                    writetoconfig(shconfigfile,'smarthomedevices','device_finishtime_'+str(devicenumb), msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_finishTime", msg.payload.decode("utf-8"), qos=0, retain=True)
                else:
                    print( "invalid payload for topic '" + msg.topic + "': " + msg.payload.decode("utf-8"))

            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_onTime" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices and re.search(r'^([01]{0,1}\d|2[0-3]):[0-5]\d$', msg.payload.decode("utf-8") ) ):
                    writetoconfig(shconfigfile,'smarthomedevices','device_ontime_'+str(devicenumb), msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_onTime", msg.payload.decode("utf-8"), qos=0, retain=True)
                else:
                    print( "invalid payload for topic '" + msg.topic + "': " + msg.payload.decode("utf-8"))

            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_startTime" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices and re.search(r'^([01]{0,1}\d|2[0-3]):[0-5]\d$', msg.payload.decode("utf-8") ) ):
                    writetoconfig(shconfigfile,'smarthomedevices','device_startTime_'+str(devicenumb), msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_startTime", msg.payload.decode("utf-8"), qos=0, retain=True)
                else:
                    print( "invalid payload for topic '" + msg.topic + "': " + msg.payload.decode("utf-8"))
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_endTime" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices and re.search(r'^([01]{0,1}\d|2[0-3]):[0-5]\d$', msg.payload.decode("utf-8") ) ):
                    writetoconfig(shconfigfile,'smarthomedevices','device_endTime_'+str(devicenumb), msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_endTime", msg.payload.decode("utf-8"), qos=0, retain=True)
                else:
                    print( "invalid payload for topic '" + msg.topic + "': " + msg.payload.decode("utf-8"))
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_homeConsumtion" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices and 0 <= int(msg.payload) <= 1 ):
                    writetoconfig(shconfigfile,'smarthomedevices','device_homeConsumtion_'+str(devicenumb), msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_homeConsumtion", msg.payload.decode("utf-8"), qos=0, retain=True)
                else:
                    print( "invalid payload for topic '" + msg.topic + "': " + msg.payload.decode("utf-8"))
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_measurePortSdm" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices and 0 <= int(msg.payload) <= 9999 ):
                    writetoconfig(shconfigfile,'smarthomedevices','device_measurePortSdm_'+str(devicenumb), msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_measurePortSdm", msg.payload.decode("utf-8"), qos=0, retain=True)
                else:
                    print( "invalid payload for topic '" + msg.topic + "': " + msg.payload.decode("utf-8"))
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_startupDetection" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices and 0 <= int(msg.payload) <= 1 ):
                    writetoconfig(shconfigfile,'smarthomedevices','device_startupdetection_'+str(devicenumb), msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_startupDetection", msg.payload.decode("utf-8"), qos=0, retain=True)
                else:
                    print( "invalid payload for topic '" + msg.topic + "': " + msg.payload.decode("utf-8"))
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_standbyPower" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices and 0 <= int(msg.payload) <= 1000 ):
                    writetoconfig(shconfigfile,'smarthomedevices','device_standbypower_'+str(devicenumb), msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_standbyPower", msg.payload.decode("utf-8"), qos=0, retain=True)
                else:
                    print( "invalid payload for topic '" + msg.topic + "': " + msg.payload.decode("utf-8"))
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_standbyDuration" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices and 0 <= int(msg.payload) <= 86400 ):
                    writetoconfig(shconfigfile,'smarthomedevices','device_standbyduration_'+str(devicenumb), msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_standbyDuration", msg.payload.decode("utf-8"), qos=0, retain=True)
                else:
                    print( "invalid payload for topic '" + msg.topic + "': " + msg.payload.decode("utf-8"))
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_startupMulDetection" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices and 0 <= int(msg.payload) <= 1 ):
                    writetoconfig(shconfigfile,'smarthomedevices','device_startupMulDetection_'+str(devicenumb), msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_startupMulDetection", msg.payload.decode("utf-8"), qos=0, retain=True)
                else:
                    print( "invalid payload for topic '" + msg.topic + "': " + msg.payload.decode("utf-8"))
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_measuresmaage" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices and 0 <= int(msg.payload) <= 1000 ):
                    writetoconfig(shconfigfile,'smarthomedevices','device_measuresmaage_'+str(devicenumb), msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_measuresmaage", msg.payload.decode("utf-8"), qos=0, retain=True)
                else:
                    print( "invalid payload for topic '" + msg.topic + "': " + msg.payload.decode("utf-8"))
            if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_measuresmaser" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= numberOfSupportedDevices):
                    writetoconfig(shconfigfile,'smarthomedevices','device_measuresmaser_'+str(devicenumb), msg.payload.decode("utf-8"))
                    client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_measuresmaser", msg.payload.decode("utf-8"), qos=0, retain=True)
                else:
                    print( "invalid payload for topic '" + msg.topic + "': " + msg.payload.decode("utf-8"))
            if (msg.topic == "openWB/config/set/SmartHome/maxBatteryPower"):
                if (0 <= int(msg.payload) <= 10000):
                    f = open('/var/www/html/openWB/ramdisk/smarthomehandlermaxbatterypower', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    client.publish("openWB/config/get/SmartHome/maxBatteryPower", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/SmartHome/logLevel"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 2):
                    f = open('/var/www/html/openWB/ramdisk/smarthomehandlerloglevel', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    client.publish("openWB/config/get/SmartHome/logLevel", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (( "openWB/config/set/lp" in msg.topic) and ("stopchargeafterdisc" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= 8 and 0 <= int(msg.payload) <= 1):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "stopchargeafterdisclp" + str(devicenumb) + "=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/lp/" + str(devicenumb) + "/stopchargeafterdisc", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (( "openWB/config/set/sofort/lp" in msg.topic) and ("current" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= 8 and 6 <= int(msg.payload) <= 32):
                    client.publish("openWB/config/get/sofort/lp/"+str(devicenumb)+"/current", msg.payload.decode("utf-8"), qos=0, retain=True)
                    f = open('/var/www/html/openWB/ramdisk/lp'+str(devicenumb)+'sofortll', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (( "openWB/set/lp" in msg.topic) and ("manualSoc" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= 2 and 0 <= int(msg.payload) <= 100):
                    client.publish("openWB/lp/"+str(devicenumb)+"/manualSoc", msg.payload.decode("utf-8"), qos=0, retain=True)
                    f = open('/var/www/html/openWB/ramdisk/manual_soc_lp'+str(devicenumb), 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    client.publish("openWB/lp/"+str(devicenumb)+"/%Soc", msg.payload.decode("utf-8"), qos=0, retain=True)
                    if ( int(devicenumb) == 1 ):
                        socFile = '/var/www/html/openWB/ramdisk/soc'
                    elif ( int(devicenumb) == 2 ):
                        socFile = '/var/www/html/openWB/ramdisk/soc1'
                    f = open(socFile, 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (( "openWB/config/set/sofort/lp" in msg.topic) and ("energyToCharge" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= 8 and 0 <= int(msg.payload) <= 100):
                    if ( int(devicenumb) == 1):
                        sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "lademkwh=", msg.payload.decode("utf-8")]
                        subprocess.run(sendcommand)
                    if (int(devicenumb) == 2):
                        sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "lademkwhs1=", msg.payload.decode("utf-8")]
                        subprocess.run(sendcommand)
                    if (int(devicenumb) == 3):
                        sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "lademkwhs2=", msg.payload.decode("utf-8")]
                        subprocess.run(sendcommand)
                    if (int(devicenumb) >= 4):
                        sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "lademkwhlp"+str(devicenumb)+"=", msg.payload.decode("utf-8")]
                        subprocess.run(sendcommand)
                    client.publish("openWB/config/get/sofort/lp/"+str(devicenumb)+"/energyToCharge", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (( "openWB/config/set/sofort/lp" in msg.topic) and ("resetEnergyToCharge" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= 8 and int(msg.payload) == 1):
                    if ( int(devicenumb) == 1):
                        f = open('/var/www/html/openWB/ramdisk/aktgeladen', 'w')
                        f.write("0")
                        f.close()
                        f = open('/var/www/html/openWB/ramdisk/gelrlp1', 'w')
                        f.write("0")
                        f.close()
                    if (int(devicenumb) == 2):
                        f = open('/var/www/html/openWB/ramdisk/aktgeladens1', 'w')
                        f.write("0")
                        f.close()
                        f = open('/var/www/html/openWB/ramdisk/gelrlp2', 'w')
                        f.write("0")
                        f.close()
                    if (int(devicenumb) == 3):
                        f = open('/var/www/html/openWB/ramdisk/aktgeladens2', 'w')
                        f.write("0")
                        f.close()
                        f = open('/var/www/html/openWB/ramdisk/gelrlp3', 'w')
                        f.write("0")
                        f.close()
                    if (int(devicenumb) >= 4):
                        f = open('/var/www/html/openWB/ramdisk/aktgeladenlp'+str(devicenumb), 'w')
                        f.write("0")
                        f.close()
                        f = open('/var/www/html/openWB/ramdisk/gelrlp'+str(devicenumb), 'w')
                        f.write("0")
                        f.close()
            if (( "openWB/config/set/sofort/lp" in msg.topic) and ("socToChargeTo" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 1 <= int(devicenumb) <= 2 and 0 <= int(msg.payload) <= 100):
                    client.publish("openWB/config/get/sofort/lp/"+str(devicenumb)+"/socToChargeTo", msg.payload.decode("utf-8"), qos=0, retain=True)
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "sofortsoclp"+str(devicenumb)+"=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
            if (( "openWB/config/set/sofort/lp" in msg.topic) and ("chargeLimitation" in msg.topic)):
                devicenumb=re.sub(r'\D', '', msg.topic)
                if ( 3 <= int(devicenumb) <= 8 and 0 <= int(msg.payload) <= 1):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "msmoduslp"+str(devicenumb)+"=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    time.sleep(0.4)
                    if (int(msg.payload) == 1):
                        sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "lademstatlp"+str(devicenumb)+"=", "1"]
                        subprocess.run(sendcommand)
                        client.publish("openWB/lp/5/boolDirectModeChargekWh", msg.payload.decode("utf-8"), qos=0, retain=True)
                    else:
                        sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "lademstatlp"+str(devicenumb)+"=", "0"]
                        subprocess.run(sendcommand)
                        client.publish("openWB/lp/5/boolDirectModeChargekWh", "0", qos=0, retain=True)
                    client.publish("openWB/config/get/sofort/lp/"+str(devicenumb)+"/chargeLimitation", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/minFeedinPowerBeforeStart"):
                if (int(msg.payload) >= -100000 and int(msg.payload) <= 100000):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "mindestuberschuss=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/minFeedinPowerBeforeStart", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/maxPowerConsumptionBeforeStop"):
                if (int(msg.payload) >= -100000 and int(msg.payload) <= 100000):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "abschaltuberschuss=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/maxPowerConsumptionBeforeStop", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/stopDelay"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 10000):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "abschaltverzoegerung=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/stopDelay", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/startDelay"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 100000):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "einschaltverzoegerung=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/startDelay", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/minCurrentMinPv"):
                if (int(msg.payload) >= 6 and int(msg.payload) <= 16):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "minimalampv=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/minCurrentMinPv", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/lp/1/maxSoc"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 100):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "stopchargepvpercentagelp1=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/lp/1/maxSoc", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/lp/2/maxSoc"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 100):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "stopchargepvpercentagelp2=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/lp/2/maxSoc", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/lp/1/socLimitation"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 1):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "stopchargepvatpercentlp1=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/lp/1/socLimitation", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/lp/2/socLimitation"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 1):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "stopchargepvatpercentlp2=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/lp/2/socLimitation", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/lp/1/minCurrent"):
                if (int(msg.payload) >= 6 and int(msg.payload) <= 16):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "minimalapv=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/lp/1/minCurrent", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/lp/2/minCurrent"):
                if (int(msg.payload) >= 6 and int(msg.payload) <= 16):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "minimalalp2pv=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/lp/2/minCurrent", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (( "openWB/set/pv" in msg.topic) and ("faultState" in msg.topic)):
                devicenumb = int(re.sub(r'\D', '', msg.topic))
                if ( (1 <= devicenumb <= 2) and (0 <= int(msg.payload) <= 2) ):
                    client.publish("openWB/pv/"+str(devicenumb)+"/faultState", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (( "openWB/set/pv" in msg.topic) and ("faultStr" in msg.topic)):
                devicenumb = int(re.sub(r'\D', '', msg.topic))
                if (1 <= devicenumb <= 2):
                    client.publish("openWB/pv/"+str(devicenumb)+"/faultStr", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/u1p3p/standbyPhases"):
                if (int(msg.payload) >= 1 and int(msg.payload) <= 3):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "u1p3pstandby=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/u1p3p/standbyPhases", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/u1p3p/sofortPhases"):
                if (int(msg.payload) >= 1 and int(msg.payload) <= 3):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "u1p3psofort=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/u1p3p/sofortPhases", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/u1p3p/nachtPhases"):
                if (int(msg.payload) >= 1 and int(msg.payload) <= 3):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "u1p3pnl=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/u1p3p/nachtPhases", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/u1p3p/minundpvPhases"):
                if (int(msg.payload) >= 1 and int(msg.payload) <= 3):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "u1p3pminundpv=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/u1p3p/minundpvPhases", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/u1p3p/nurpvPhases"):
                if (int(msg.payload) >= 1 and int(msg.payload) <= 3):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "u1p3pnurpv=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/u1p3p/nurpvPhases", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/u1p3p/isConfigured"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 1):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "u1p3paktiv=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/u1p3p/isConfigured", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/global/minEVSECurrentAllowed"):
                if (int(msg.payload) >= 6 and int(msg.payload) <= 32):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "minimalstromstaerke=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/global/minEVSECurrentAllowed", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/global/maxEVSECurrentAllowed"):
                if (int(msg.payload) >= 6 and int(msg.payload) <= 32):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "maximalstromstaerke=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/global/maxEVSECurrentAllowed", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/global/dataProtectionAcknoledged"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 2):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "datenschutzack=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/global/dataProtectionAcknoledged", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/lp/1/minSocAlwaysToChargeTo"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 80):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "minnurpvsoclp1=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/lp/1/minSocAlwaysToChargeTo", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/lp/1/maxSocToChargeTo"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 101):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "maxnurpvsoclp1=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/lp/1/maxSocToChargeTo", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/lp/1/minSocAlwaysToChargeToCurrent"):
                if (int(msg.payload) >= 6 and int(msg.payload) <= 32):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "minnurpvsocll=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/lp/1/minSocAlwaysToChargeToCurrent", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/chargeSubmode"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 2):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "pvbezugeinspeisung=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/chargeSubmode", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/regulationPoint"):
                if (int(msg.payload) >= -300000 and int(msg.payload) <= 300000):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "offsetpv=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/regulationPoint", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/boolShowPriorityIconInTheme"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 1):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "speicherpvui=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/boolShowPriorityIconInTheme", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/minBatteryChargePowerAtEvPriority"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 90000):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "speichermaxwatt=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/minBatteryChargePowerAtEvPriority", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/minBatteryDischargeSocAtBattPriority"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 101):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "speichersocnurpv=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/minBatteryDischargeSocAtBattPriority", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/batteryDischargePowerAtBattPriority"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 90000):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "speicherwattnurpv=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/batteryDischargePowerAtBattPriority", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/socStartChargeAtMinPv"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 101):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "speichersocminpv=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/socStartChargeAtMinPv", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/socStopChargeAtMinPv"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 101):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "speichersochystminpv=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/socStopChargeAtMinPv", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/boolAdaptiveCharging"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 1):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "adaptpv=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/boolAdaptiveCharging", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/adaptiveChargingFactor"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 100):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "adaptfaktor=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/adaptiveChargingFactor", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/nurpv70dynact"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 1):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "nurpv70dynact=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/nurpv70dynact", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/nurpv70dynw"):
                if (int(msg.payload) >= 2000 and int(msg.payload) <= 50000):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "nurpv70dynw=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/nurpv70dynw", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/set/system/GetRemoteSupport"):
                if ( 5 <= len(msg.payload.decode("utf-8")) <=50 ):
                    f = open('/var/www/html/openWB/ramdisk/remotetoken', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    getsupport = ["/var/www/html/openWB/runs/initremote.sh"]
                    subprocess.run(getsupport)
            if (msg.topic == "openWB/set/hook/HookControl"):
                if (int(msg.payload) >= 0 and int(msg.payload) <=30):
                    hookmsg=msg.payload.decode("utf-8")
                    hooknmb=hookmsg[1:2]
                    hookact=hookmsg[0:1]
                    sendhook = ["/var/www/html/openWB/runs/hookcontrol.sh", hookmsg]
                    subprocess.run(sendhook)
                    client.publish("openWB/hook/"+hooknmb+"/BoolHookStatus", hookact, qos=0, retain=True)
            if (msg.topic == "openWB/config/set/display/displaysleep"):
                if (int(msg.payload) >= 10 and int(msg.payload) <= 1800):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "displaysleep=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/display/displaysleep", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/display/displaypincode"):
                if (int(msg.payload) >= 1000 and int(msg.payload) <= 99999999):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "displaypincode=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    # ! intentionally not publishing PIN code via MQTT !
            if (msg.topic == "openWB/config/set/slave/MinimumAdjustmentInterval"):
                if (int(msg.payload) >= 10 and int(msg.payload) <= 300):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "slaveModeMinimumAdjustmentInterval=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/slave/MinimumAdjustmentInterval", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/slave/SlowRamping"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 1):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "slaveModeSlowRamping=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/slave/SlowRamping", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/slave/StandardSocketInstalled"):
                if (int(msg.payload) >= 0 and int(msg.payload) <=1):
                    standardSocketInstalled=msg.payload.decode("utf-8")
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "standardSocketInstalled=", standardSocketInstalled]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/slave/StandardSocketInstalled", standardSocketInstalled, qos=0, retain=True)
            if (msg.topic == "openWB/config/set/slave/UseLastChargingPhase"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 1):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "slaveModeUseLastChargingPhase=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/slave/UseLastChargingPhase", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/set/configure/AllowedTotalCurrentPerPhase"):
                if (float(msg.payload) >= 0 and float(msg.payload) <= 200):
                    f = open('/var/www/html/openWB/ramdisk/AllowedTotalCurrentPerPhase', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    setTopicCleared = True
            if (msg.topic == "openWB/config/set/slave/SocketApproved"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 2):
                    f = open('/var/www/html/openWB/ramdisk/socketApproved', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    client.publish("openWB/config/get/slave/SocketApproved", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/set/configure/AllowedPeakPower"):
                if (float(msg.payload) >= 0 and float(msg.payload) <= 300000):
                    f = open('/var/www/html/openWB/ramdisk/AllowedPeakPower', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    setTopicCleared = True
            if (msg.topic == "openWB/set/configure/FixedChargeCurrentCp1"):
                if (int(msg.payload) >= -1 and int(msg.payload) <= 32):
                    f = open('/var/www/html/openWB/ramdisk/FixedChargeCurrentCp1', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    setTopicCleared = True
            if (msg.topic == "openWB/set/configure/FixedChargeCurrentCp2"):
                if (int(msg.payload) >= -1 and int(msg.payload) <= 32):
                    f = open('/var/www/html/openWB/ramdisk/FixedChargeCurrentCp2', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    setTopicCleared = True
            if (msg.topic == "openWB/set/configure/SlaveModeAllowedLoadImbalance"):
                if (float(msg.payload) >= 0 and float(msg.payload) <= 200):
                    f = open('/var/www/html/openWB/ramdisk/SlaveModeAllowedLoadImbalance', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    setTopicCleared = True
            if (msg.topic == "openWB/set/configure/AllowedRfidsForSocket"):
                f = open('/var/www/html/openWB/ramdisk/AllowedRfidsForSocket', 'w')
                f.write(msg.payload.decode("utf-8"))
                f.close()
                setTopicCleared = True
            if (msg.topic == "openWB/set/configure/AllowedRfidsForLp1"):
                f = open('/var/www/html/openWB/ramdisk/AllowedRfidsForLp1', 'w')
                f.write(msg.payload.decode("utf-8"))
                f.close()
                setTopicCleared = True
            if (msg.topic == "openWB/set/configure/AllowedRfidsForLp2"):
                f = open('/var/www/html/openWB/ramdisk/AllowedRfidsForLp2', 'w')
                f.write(msg.payload.decode("utf-8"))
                f.close()
                setTopicCleared = True
            if (msg.topic == "openWB/set/configure/LastControllerPublish"):
                f = open('/var/www/html/openWB/ramdisk/LastControllerPublish', 'w')
                f.write(msg.payload.decode("utf-8"))
                f.close()
                setTopicCleared = True
            if (msg.topic == "openWB/set/configure/TotalPower"):
                if (float(msg.payload) >= 0 and float(msg.payload) <=300000):
                    f = open('/var/www/html/openWB/ramdisk/TotalPower', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    setTopicCleared = True
            if (msg.topic == "openWB/set/configure/TotalCurrentConsumptionOnL1"):
                if (float(msg.payload) >= 0 and float(msg.payload) <=200):
                    f = open('/var/www/html/openWB/ramdisk/TotalCurrentConsumptionOnL1', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    setTopicCleared = True
            if (msg.topic == "openWB/set/configure/TotalCurrentConsumptionOnL2"):
                if (float(msg.payload) >= 0 and float(msg.payload) <=200):
                    f = open('/var/www/html/openWB/ramdisk/TotalCurrentConsumptionOnL2', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    setTopicCleared = True
            if (msg.topic == "openWB/set/configure/TotalCurrentConsumptionOnL3"):
                if (float(msg.payload) >= 0 and float(msg.payload) <=200):
                    f = open('/var/www/html/openWB/ramdisk/TotalCurrentConsumptionOnL3', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    setTopicCleared = True
            if (msg.topic == "openWB/set/configure/ChargingVehiclesOnL1"):
                if (int(msg.payload) >= 0 and int(msg.payload) <=200):
                    f = open('/var/www/html/openWB/ramdisk/ChargingVehiclesOnL1', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    setTopicCleared = True
            if (msg.topic == "openWB/set/configure/ChargingVehiclesOnL2"):
                if (int(msg.payload) >= 0 and int(msg.payload) <=200):
                    f = open('/var/www/html/openWB/ramdisk/ChargingVehiclesOnL2', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    setTopicCleared = True
            if (msg.topic == "openWB/set/configure/ChargingVehiclesOnL3"):
                if (int(msg.payload) >= 0 and int(msg.payload) <=200):
                    f = open('/var/www/html/openWB/ramdisk/ChargingVehiclesOnL3', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    setTopicCleared = True
            if (msg.topic == "openWB/config/set/global/rfidConfigured"):
                if (int(msg.payload) >= 0 and int(msg.payload) <=1):
                    rfidMode=msg.payload.decode("utf-8")
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "rfidakt=", rfidMode]
                    subprocess.run(sendcommand)
                    client.publish("openWB/global/rfidConfigured", rfidMode, qos=0, retain=True)
            if (msg.topic == "openWB/config/set/global/slaveMode"):
                if (int(msg.payload) >= 0 and int(msg.payload) <=1):
                    slaveMode=msg.payload.decode("utf-8")
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "slavemode=", slaveMode]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/global/slaveMode", slaveMode, qos=0, retain=True)
            if (msg.topic == "openWB/config/set/global/lp/1/cpInterrupt"):
                if (int(msg.payload) >= 0 and int(msg.payload) <=1):
                    einbeziehen=msg.payload.decode("utf-8")
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "cpunterbrechunglp1=", einbeziehen]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/global/lp/1/cpInterrupt", einbeziehen, qos=0, retain=True)
            if (msg.topic == "openWB/config/set/global/lp/2/cpInterrupt"):
                if (int(msg.payload) >= 0 and int(msg.payload) <=1):
                    einbeziehen=msg.payload.decode("utf-8")
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "cpunterbrechunglp2=", einbeziehen]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/global/lp/2/cpInterrupt", einbeziehen, qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/priorityModeEVBattery"):
                if (int(msg.payload) >= 0 and int(msg.payload) <=1):
                    einbeziehen=msg.payload.decode("utf-8")
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "speicherpveinbeziehen=", einbeziehen]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/priorityModeEVBattery", einbeziehen, qos=0, retain=True)
            if (msg.topic == "openWB/set/graph/LiveGraphDuration"):
                if (int(msg.payload) >= 20 and int(msg.payload) <=120):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "livegraph=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
            if (msg.topic == "openWB/set/system/SimulateRFID"):
                if len(str(msg.payload.decode("utf-8"))) >= 1 and bool(re.match(namenumballowed, msg.payload.decode("utf-8"))):
                    f = open('/var/www/html/openWB/ramdisk/readtag', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/system/PerformUpdate"):
                if (int(msg.payload) == 1):
                    client.publish("openWB/set/system/PerformUpdate", "0", qos=0, retain=True)
                    setTopicCleared = True
                    subprocess.run("/var/www/html/openWB/runs/update.sh")
            if (msg.topic == "openWB/set/system/SendDebug"):
                if ( 20 <= len(msg.payload.decode("utf-8")) <=1000 ):
                    f = open('/var/www/html/openWB/ramdisk/debuguser', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    client.publish("openWB/set/system/SendDebug", "0", qos=0, retain=True)
                    setTopicCleared = True
                    subprocess.run("/var/www/html/openWB/runs/senddebuginit.sh")
            if (msg.topic == "openWB/set/system/reloadDisplay"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 1):
                    client.publish("openWB/system/reloadDisplay", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/releaseTrain"):
                if ( msg.payload.decode("utf-8") == "stable17" or msg.payload.decode("utf-8") == "master" or msg.payload.decode("utf-8") == "beta" or msg.payload.decode("utf-8").startswith("yc/")):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "releasetrain=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
            if (msg.topic == "openWB/set/graph/RequestLiveGraph"):
                if (int(msg.payload) == 1):
                    subprocess.run("/var/www/html/openWB/runs/sendlivegraphdata.sh")
                else:
                    client.publish("openWB/system/LiveGraphData", "empty", qos=0, retain=True)
                setTopicCleared = True
            if (msg.topic == "openWB/set/graph/RequestLLiveGraph"):
                if (int(msg.payload) == 1):
                    subprocess.run("/var/www/html/openWB/runs/sendllivegraphdata.sh")
                else:
                    client.publish("openWB/system/1alllivevalues", "empty", qos=0, retain=True)
                    client.publish("openWB/system/2alllivevalues", "empty", qos=0, retain=True)
                    client.publish("openWB/system/3alllivevalues", "empty", qos=0, retain=True)
                    client.publish("openWB/system/4alllivevalues", "empty", qos=0, retain=True)
                    client.publish("openWB/system/5alllivevalues", "empty", qos=0, retain=True)
                    client.publish("openWB/system/6alllivevalues", "empty", qos=0, retain=True)
                    client.publish("openWB/system/7alllivevalues", "empty", qos=0, retain=True)
                    client.publish("openWB/system/8alllivevalues", "empty", qos=0, retain=True)
                    client.publish("openWB/system/9alllivevalues", "empty", qos=0, retain=True)
                    client.publish("openWB/system/10alllivevalues", "empty", qos=0, retain=True)
                    client.publish("openWB/system/11alllivevalues", "empty", qos=0, retain=True)
                    client.publish("openWB/system/12alllivevalues", "empty", qos=0, retain=True)
                    client.publish("openWB/system/13alllivevalues", "empty", qos=0, retain=True)
                    client.publish("openWB/system/14alllivevalues", "empty", qos=0, retain=True)
                    client.publish("openWB/system/15alllivevalues", "empty", qos=0, retain=True)
                    client.publish("openWB/system/16alllivevalues", "empty", qos=0, retain=True)
                setTopicCleared = True
            if (msg.topic == "openWB/set/graph/RequestDayGraph"):
                if (int(msg.payload) >= 1 and int(msg.payload) <= 20501231):
                    sendcommand = ["/var/www/html/openWB/runs/senddaygraphdata.sh", msg.payload]
                    subprocess.run(sendcommand)
                else:
                    client.publish("openWB/system/DayGraphData1", "empty", qos=0, retain=True)
                    client.publish("openWB/system/DayGraphData2", "empty", qos=0, retain=True)
                    client.publish("openWB/system/DayGraphData3", "empty", qos=0, retain=True)
                    client.publish("openWB/system/DayGraphData4", "empty", qos=0, retain=True)
                    client.publish("openWB/system/DayGraphData5", "empty", qos=0, retain=True)
                    client.publish("openWB/system/DayGraphData6", "empty", qos=0, retain=True)
                    client.publish("openWB/system/DayGraphData7", "empty", qos=0, retain=True)
                    client.publish("openWB/system/DayGraphData8", "empty", qos=0, retain=True)
                    client.publish("openWB/system/DayGraphData9", "empty", qos=0, retain=True)
                    client.publish("openWB/system/DayGraphData10", "empty", qos=0, retain=True)
                    client.publish("openWB/system/DayGraphData11", "empty", qos=0, retain=True)
                    client.publish("openWB/system/DayGraphData12", "empty", qos=0, retain=True)
                setTopicCleared = True
            if (msg.topic == "openWB/set/graph/RequestMonthGraph"):
                if (int(msg.payload) >= 1 and int(msg.payload) <= 205012):
                    sendcommand = ["/var/www/html/openWB/runs/sendmonthgraphdata.sh", msg.payload]
                    subprocess.run(sendcommand)
                else:
                    client.publish("openWB/system/MonthGraphData1", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphData2", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphData3", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphData4", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphData5", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphData6", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphData7", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphData8", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphData9", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphData10", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphData11", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphData12", "empty", qos=0, retain=True)
                setTopicCleared = True
            if (msg.topic == "openWB/set/graph/RequestMonthGraphv1"):
                if (int(msg.payload) >= 1 and int(msg.payload) <= 205012):
                    sendcommand = ["/var/www/html/openWB/runs/sendmonthgraphdatav1.sh", msg.payload]
                    subprocess.run(sendcommand)
                else:
                    client.publish("openWB/system/MonthGraphDatan1", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphDatan2", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphDatan3", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphDatan4", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphDatan5", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphDatan6", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphDatan7", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphDatan8", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphDatan9", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphDatan10", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphDatan11", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphDatan12", "empty", qos=0, retain=True)
                setTopicCleared = True
            if (msg.topic == "openWB/set/graph/RequestYearGraph"):
                if (int(msg.payload) >= 1 and int(msg.payload) <= 2050):
                    sendcommand = ["/var/www/html/openWB/runs/sendyeargraphdata.sh", msg.payload]
                    subprocess.run(sendcommand)
                else:
                    client.publish("openWB/system/YearGraphData1", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphData2", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphData3", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphData4", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphData5", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphData6", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphData7", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphData8", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphData9", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphData10", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphData11", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphData12", "empty", qos=0, retain=True)
                setTopicCleared = True
            if (msg.topic == "openWB/set/graph/RequestYearGraphv1"):
                if (int(msg.payload) >= 1 and int(msg.payload) <= 2050):
                    sendcommand = ["/var/www/html/openWB/runs/sendyeargraphdatav1.sh", msg.payload]
                    subprocess.run(sendcommand)
                else:
                    client.publish("openWB/system/YearGraphDatan1", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphDatan2", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphDatan3", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphDatan4", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphDatan5", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphDatan6", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphDatan7", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphDatan8", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphDatan9", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphDatan10", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphDatan11", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphDatan12", "empty", qos=0, retain=True)
                setTopicCleared = True
            if (msg.topic == "openWB/set/system/debug/RequestDebugInfo"):
                if (int(msg.payload) == 1):
                    sendcommand = ["/var/www/html/openWB/runs/sendmqttdebug.sh"]
                    subprocess.run(sendcommand)
                setTopicCleared = True
            if (msg.topic == "openWB/set/graph/RequestMonthLadelog"):
                if (int(msg.payload) >= 1 and int(msg.payload) <= 205012):
                    sendcommand = ["/var/www/html/openWB/runs/sendladelog.sh", msg.payload]
                    subprocess.run(sendcommand)
                else:
                    client.publish("openWB/system/MonthLadelogData1", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthLadelogData2", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthLadelogData3", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthLadelogData4", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthLadelogData5", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthLadelogData6", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthLadelogData7", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthLadelogData8", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthLadelogData9", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthLadelogData10", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthLadelogData11", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthLadelogData12", "empty", qos=0, retain=True)
                setTopicCleared = True
            if (msg.topic == "openWB/set/pv/NurPV70Status"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 1):
                    client.publish("openWB/pv/bool70PVDynStatus", msg.payload.decode("utf-8"), qos=0, retain=True)
                    f = open('/var/www/html/openWB/ramdisk/nurpv70dynstatus', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/RenewMQTT"):
                if (int(msg.payload) == 1):
                    client.publish("openWB/set/RenewMQTT", "0", qos=0, retain=True)
                    setTopicCleared = True
                    f = open('/var/www/html/openWB/ramdisk/renewmqtt', 'w')
                    f.write("1")
                    f.close()
            if (msg.topic == "openWB/set/ChargeMode"):
                if (int(msg.payload) >= 0 and int(msg.payload) <=4):
                    f = open('/var/www/html/openWB/ramdisk/lademodus', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    client.publish("openWB/global/ChargeMode", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/sofort/lp/1/chargeLimitation"):
                if (int(msg.payload) >= 0 and int(msg.payload) <=2):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "msmoduslp1=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    if (int(msg.payload) == 1):
                        client.publish("openWB/lp/1/boolDirectModeChargekWh", msg.payload.decode("utf-8"), qos=0, retain=True)
                    else:
                        client.publish("openWB/lp/1/boolDirectModeChargekWh", "0", qos=0, retain=True)
                    if (int(msg.payload) == 2):
                        client.publish("openWB/lp/1/boolDirectChargeModeSoc", "1", qos=0, retain=True)
                    else:
                        client.publish("openWB/lp/1/boolDirectChargeModeSoc", "0", qos=0, retain=True)
                    client.publish("openWB/config/get/sofort/lp/1/chargeLimitation", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/sofort/lp/2/chargeLimitation"):
                if (int(msg.payload) >= 0 and int(msg.payload) <=2):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "msmoduslp2=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    if (int(msg.payload) == 1):
                        client.publish("openWB/lp/2/boolDirectModeChargekWh", msg.payload.decode("utf-8"), qos=0, retain=True)
                    else:
                        client.publish("openWB/lp/2/boolDirectModeChargekWh", "0", qos=0, retain=True)
                    if (int(msg.payload) == 2):
                        client.publish("openWB/lp/2/boolDirectChargeModeSoc", "1", qos=0, retain=True)
                    else:
                        client.publish("openWB/lp/2/boolDirectChargeModeSoc", "0", qos=0, retain=True)
                    client.publish("openWB/config/get/sofort/lp/2/chargeLimitation", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/set/lp/1/DirectChargeSubMode"):
                if (int(msg.payload) == 0):
                    replaceAll("lademstat=",msg.payload.decode("utf-8"))
                    replaceAll("sofortsocstatlp1=",msg.payload.decode("utf-8"))
                if (int(msg.payload) == 1):
                    replaceAll("lademstat=",msg.payload.decode("utf-8"))
                    replaceAll("sofortsocstatlp1=","0")
                if (int(msg.payload) == 2):
                    replaceAll("lademstat=","0")
                    replaceAll("sofortsocstatlp1=","1")
            if (msg.topic == "openWB/set/lp/2/DirectChargeSubMode"):
                if (int(msg.payload) == 0):
                    replaceAll("lademstats1=",msg.payload.decode("utf-8"))
                    replaceAll("sofortsocstatlp2=",msg.payload.decode("utf-8"))
                if (int(msg.payload) == 1):
                    replaceAll("lademstats1=",msg.payload.decode("utf-8"))
                    replaceAll("sofortsocstatlp2=","0")
                if (int(msg.payload) == 2):
                    replaceAll("lademstats1=","0")
                    replaceAll("sofortsocstatlp2=","1")
            if (msg.topic == "openWB/set/lp/3/DirectChargeSubMode"):
                if (int(msg.payload) == 0):
                    replaceAll("lademstats2=",msg.payload.decode("utf-8"))
                    #replaceAll("sofortsocstatlp2=",msg.payload.decode("utf-8"))
                if (int(msg.payload) == 1):
                    replaceAll("lademstats2=",msg.payload.decode("utf-8"))
                    #replaceAll("sofortsocstatlp2=","0")
                #if (int(msg.payload) == 2):
                #    replaceAll("lademstats1=","0")
                #    replaceAll("sofortsocstatlp2=","1")
            if (msg.topic == "openWB/set/lp/4/DirectChargeSubMode"):
                if (int(msg.payload) == 0):
                    replaceAll("lademstatlp4=",msg.payload.decode("utf-8"))
                if (int(msg.payload) == 1):
                    replaceAll("lademstatlp4=",msg.payload.decode("utf-8"))
            if (msg.topic == "openWB/set/lp/5/DirectChargeSubMode"):
                if (int(msg.payload) == 0):
                    replaceAll("lademstatlp5=",msg.payload.decode("utf-8"))
                if (int(msg.payload) == 1):
                    replaceAll("lademstatlp5=",msg.payload.decode("utf-8"))
            if (msg.topic == "openWB/set/lp/6/DirectChargeSubMode"):
                if (int(msg.payload) == 0):
                    replaceAll("lademstatlp6=",msg.payload.decode("utf-8"))
                if (int(msg.payload) == 1):
                    replaceAll("lademstatlp6=",msg.payload.decode("utf-8"))
            if (msg.topic == "openWB/set/lp/7/DirectChargeSubMode"):
                if (int(msg.payload) == 0):
                    replaceAll("lademstatlp7=",msg.payload.decode("utf-8"))
                if (int(msg.payload) == 1):
                    replaceAll("lademstatlp7=",msg.payload.decode("utf-8"))
            if (msg.topic == "openWB/set/lp/8/DirectChargeSubMode"):
                if (int(msg.payload) == 0):
                    replaceAll("lademstatlp8=",msg.payload.decode("utf-8"))
                if (int(msg.payload) == 1):
                    replaceAll("lademstatlp8=",msg.payload.decode("utf-8"))
            if (msg.topic == "openWB/set/isss/ClearRfid"):
                if (int(msg.payload) > 0 and int(msg.payload) <=1):
                    f = open('/var/www/html/openWB/ramdisk/readtag', 'w')
                    f.write("0")
                    f.close()
            if (msg.topic == "openWB/set/isss/Current"):
                if (float(msg.payload) >= 0 and float(msg.payload) <=32):
                    f = open('/var/www/html/openWB/ramdisk/llsoll', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/isss/Lp2Current"):
                if (float(msg.payload) >= 0 and float(msg.payload) <=32):
                    f = open('/var/www/html/openWB/ramdisk/llsolls1', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/isss/U1p3p"):
                if (int(msg.payload) >= 0 and int(msg.payload) <=5):
                    f = open('/var/www/html/openWB/ramdisk/u1p3pstat', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/isss/U1p3pLp2"):
                 if (int(msg.payload) >= 0 and int(msg.payload) <=5):
                     f = open('/var/www/html/openWB/ramdisk/u1p3plp2stat', 'w')
                     f.write(msg.payload.decode("utf-8"))
                     f.close()
            if (msg.topic == "openWB/set/isss/Cpulp1"):
                if (int(msg.payload) >= 0 and int(msg.payload) <=5):
                    f = open('/var/www/html/openWB/ramdisk/extcpulp1', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/isss/heartbeat"):
                if (int(msg.payload) >= -1 and int(msg.payload) <=5):
                    f = open('/var/www/html/openWB/ramdisk/heartbeat', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/isss/parentWB"):
                f = open('/var/www/html/openWB/ramdisk/parentWB', 'w')
                f.write(msg.payload.decode("utf-8"))
                f.close()
                client.publish("openWB/system/parentWB", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/set/isss/parentCPlp1"):
                client.publish("openWB/system/parentCPlp1", msg.payload.decode("utf-8"), qos=0, retain=True)
                f = open('/var/www/html/openWB/ramdisk/parentCPlp1', 'w')
                f.write(msg.payload.decode("utf-8"))
                f.close()
            if (msg.topic == "openWB/set/isss/parentCPlp2"):
                client.publish("openWB/system/parentCPlp2", msg.payload.decode("utf-8"), qos=0, retain=True)
                f = open('/var/www/html/openWB/ramdisk/parentCPlp2', 'w')
                f.write(msg.payload.decode("utf-8"))
                f.close()
            if (msg.topic == "openWB/set/awattar/MaxPriceForCharging"):
                if (float(msg.payload) >= -50 and float(msg.payload) <=50):
                    f = open('/var/www/html/openWB/ramdisk/etprovidermaxprice', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/houseBattery/W"):
                if (float(msg.payload) >= -30000 and float(msg.payload) <= 30000):
                    f = open('/var/www/html/openWB/ramdisk/speicherleistung', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/houseBattery/WhImported"):
                if (float(msg.payload) >= 0 and float(msg.payload) <= 9000000):
                    f = open('/var/www/html/openWB/ramdisk/speicherikwh', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/houseBattery/WhExported"):
                if (float(msg.payload) >= 0 and float(msg.payload) <= 9000000):
                    f = open('/var/www/html/openWB/ramdisk/speicherekwh', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/houseBattery/%Soc"):
                if (float(msg.payload) >= 0 and float(msg.payload) <= 100):
                    f = open('/var/www/html/openWB/ramdisk/speichersoc', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/houseBattery/faultState"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 2):
                    client.publish("openWB/housebattery/faultState", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/set/houseBattery/faultStr"):
                client.publish("openWB/housebattery/faultStr", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/set/evu/W"):
                if (float(msg.payload) >= -100000 and float(msg.payload) <= 100000):
                    f = open('/var/www/html/openWB/ramdisk/wattbezug', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/evu/APhase1"):
                if (float(msg.payload) >= -1000 and float(msg.payload) <= 1000):
                    f = open('/var/www/html/openWB/ramdisk/bezuga1', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/evu/APhase2"):
                if (float(msg.payload) >= -1000 and float(msg.payload) <= 1000):
                    f = open('/var/www/html/openWB/ramdisk/bezuga2', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/evu/APhase3"):
                if (float(msg.payload) >= -1000 and float(msg.payload) <= 1000):
                    f = open('/var/www/html/openWB/ramdisk/bezuga3', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/evu/VPhase1"):
                if (float(msg.payload) >= -1000 and float(msg.payload) <= 1000):
                    f = open('/var/www/html/openWB/ramdisk/evuv1', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/evu/VPhase2"):
                if (float(msg.payload) >= -1000 and float(msg.payload) <= 1000):
                    f = open('/var/www/html/openWB/ramdisk/evuv2', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/evu/VPhase3"):
                if (float(msg.payload) >= -1000 and float(msg.payload) <= 1000):
                    f = open('/var/www/html/openWB/ramdisk/evuv3', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/evu/HzFrequenz"):
                if (float(msg.payload) >= 0 and float(msg.payload) <= 80):
                    f = open('/var/www/html/openWB/ramdisk/evuhz', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/evu/WhImported"):
                if (float(msg.payload) >= 0 and float(msg.payload) <= 10000000000):
                    f = open('/var/www/html/openWB/ramdisk/bezugkwh', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/evu/WhExported"):
                if (float(msg.payload) >= 0 and float(msg.payload) <= 10000000000):
                    f = open('/var/www/html/openWB/ramdisk/einspeisungkwh', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/evu/faultState"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 2):
                    client.publish("openWB/evu/faultState", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/set/evu/faultStr"):
                client.publish("openWB/evu/faultStr", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/set/lp/1/%Soc"):
                if (float(msg.payload) >= 0 and float(msg.payload) <= 100):
                    f = open('/var/www/html/openWB/ramdisk/soc', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/lp/2/%Soc"):
                if (float(msg.payload) >= 0 and float(msg.payload) <= 100):
                    f = open('/var/www/html/openWB/ramdisk/soc1', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/pv/1/WhCounter"):
                if (float(msg.payload) >= 0 and float(msg.payload) <= 10000000000):
                    f = open('/var/www/html/openWB/ramdisk/pvkwh', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/pv/1/W"):
                if (float(msg.payload) >= -10000000 and float(msg.payload) <= 100000000):
                    if (float(msg.payload) > 1):
                        pvwatt=int(float(msg.payload.decode("utf-8"))) * -1
                    else:
                        pvwatt=int(float(msg.payload.decode("utf-8")))
                    f = open('/var/www/html/openWB/ramdisk/pvwatt', 'w')
                    f.write(str(pvwatt))
                    f.close()
            if (msg.topic == "openWB/set/pv/2/WhCounter"):
                if (float(msg.payload) >= 0 and float(msg.payload) <= 10000000000):
                    f = open('/var/www/html/openWB/ramdisk/pv2kwh', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/pv/2/W"):
                if (float(msg.payload) >= -10000000 and float(msg.payload) <= 100000000):
                    if (float(msg.payload) > 1):
                        pvwatt=int(float(msg.payload.decode("utf-8"))) * -1
                    else:
                        pvwatt=int(float(msg.payload.decode("utf-8")))
                    f = open('/var/www/html/openWB/ramdisk/pv2watt', 'w')
                    f.write(str(pvwatt))
                    f.close()
            if (msg.topic == "openWB/set/lp/1/AutolockStatus"):
                if (int(msg.payload) >= 0 and int(msg.payload) <=3):
                    f = open('/var/www/html/openWB/ramdisk/autolockstatuslp1', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    client.publish("openWB/lp/1/AutolockStatus", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/set/lp/2/AutolockStatus"):
                if (int(msg.payload) >= 0 and int(msg.payload) <=3):
                    f = open('/var/www/html/openWB/ramdisk/autolockstatuslp2', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/lp/3/AutolockStatus"):
                if (int(msg.payload) >= 0 and int(msg.payload) <=3):
                    f = open('/var/www/html/openWB/ramdisk/autolockstatuslp3', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/lp/4/AutolockStatus"):
                if (int(msg.payload) >= 0 and int(msg.payload) <=3):
                    f = open('/var/www/html/openWB/ramdisk/autolockstatuslp4', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/lp/5/AutolockStatus"):
                if (int(msg.payload) >= 0 and int(msg.payload) <=3):
                    f = open('/var/www/html/openWB/ramdisk/autolockstatuslp5', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/lp/6/AutolockStatus"):
                if (int(msg.payload) >= 0 and int(msg.payload) <=3):
                    f = open('/var/www/html/openWB/ramdisk/autolockstatuslp6', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/lp/7/AutolockStatus"):
                if (int(msg.payload) >= 0 and int(msg.payload) <=3):
                    f = open('/var/www/html/openWB/ramdisk/autolockstatuslp7', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/lp/8/AutolockStatus"):
                if (int(msg.payload) >= 0 and int(msg.payload) <=3):
                    f = open('/var/www/html/openWB/ramdisk/autolockstatuslp8', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (( "openWB/set/lp" in msg.topic) and ("faultState" in msg.topic)):
                devicenumb = int(re.sub(r'\D', '', msg.topic))
                if ( (1 <= devicenumb <= 8) and (0 <= int(msg.payload) <= 2) ):
                    client.publish("openWB/lp/"+str(devicenumb)+"/faultState", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (( "openWB/set/lp" in msg.topic) and ("faultStr" in msg.topic)):
                devicenumb = int(re.sub(r'\D', '', msg.topic))
                if (1 <= devicenumb <= 8):
                    client.publish("openWB/lp/"+str(devicenumb)+"/faultStr", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (( "openWB/set/lp" in msg.topic) and ("socFaultState" in msg.topic)):
                devicenumb = int(re.sub(r'\D', '', msg.topic))
                if ( (1 <= devicenumb <= 2) and (0 <= int(msg.payload) <= 2) ):
                    client.publish("openWB/lp/"+str(devicenumb)+"/socFaultState", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (( "openWB/set/lp" in msg.topic) and ("socFaultStr" in msg.topic)):
                devicenumb = int(re.sub(r'\D', '', msg.topic))
                if (1 <= devicenumb <= 2):
                    client.publish("openWB/lp/"+str(devicenumb)+"/socFaultStr", msg.payload.decode("utf-8"), qos=0, retain=True)

            # Topics for Mqtt-EVSE module
            # ToDo: check if Mqtt-EVSE module is selected!
            # llmodule = getConfigValue("evsecon")
            if (( "openWB/set/lp" in msg.topic) and ("plugStat" in msg.topic)):
                devicenumb = int(re.sub(r'\D', '', msg.topic))
                if ( (1 <= devicenumb <= 3) and (0 <= int(msg.payload) <= 1) ):
                    plugstat=int(msg.payload.decode("utf-8"))
                    if ( devicenumb == 1 ):
                        filename = "plugstat"
                    elif ( devicenumb == 2 ):
                        filename = "plugstats1"
                    elif ( devicenumb == 3 ):
                        filename = "plugstatlp3"
                    f = open('/var/www/html/openWB/ramdisk/'+str(filename), 'w')
                    f.write(str(plugstat))
                    f.close()
            if (( "openWB/set/lp" in msg.topic) and ("chargeStat" in msg.topic)):
                devicenumb = int(re.sub(r'\D', '', msg.topic))
                if ( (1 <= devicenumb <= 3) and (0 <= int(msg.payload) <= 1) ):
                    chargestat=int(msg.payload.decode("utf-8"))
                    if ( devicenumb == 1 ):
                        filename = "chargestat"
                    elif ( devicenumb == 2 ):
                        filename = "chargestats1"
                    elif ( devicenumb == 3 ):
                        filename = "chargestatlp3"
                    f = open('/var/www/html/openWB/ramdisk/'+str(filename), 'w')
                    f.write(str(chargestat))
                    f.close()

            # Topics for Mqtt-LL module
            # ToDo: check if Mqtt-LL module is selected!
            # llmodule = getConfigValue("ladeleistungsmodul")
            if (( "openWB/set/lp" in msg.topic) and ("/W" in msg.topic)):
                devicenumb = int(re.sub(r'\D', '', msg.topic))
                if ( (1 <= devicenumb <= 3) and (0 <= int(msg.payload) <= 100000) ):
                    llaktuell=int(msg.payload.decode("utf-8"))
                    if ( devicenumb == 1 ):
                        filename = "llaktuell"
                    elif ( devicenumb == 2 ):
                        filename = "llaktuells1"
                    elif ( devicenumb == 3 ):
                        filename = "llaktuells2"
                    f = open('/var/www/html/openWB/ramdisk/'+str(filename), 'w')
                    f.write(str(llaktuell))
                    f.close()
            if (( "openWB/set/lp" in msg.topic) and ("kWhCounter" in msg.topic)):
                devicenumb = int(re.sub(r'\D', '', msg.topic))
                if ( (1 <= devicenumb <= 3) and (0 <= float(msg.payload) <= 10000000000) ):
                    if ( devicenumb == 1 ):
                        filename = "llkwh"
                    elif ( devicenumb == 2 ):
                        filename = "llkwhs1"
                    elif ( devicenumb == 3 ):
                        filename = "llkwhs2"
                    f = open('/var/www/html/openWB/ramdisk/'+str(filename), 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (( "openWB/set/lp" in msg.topic) and ("VPhase1" in msg.topic)):
                devicenumb = int(re.sub(r'\D.', '', msg.topic))
                if ( (1 <= devicenumb <= 3) and (0 <= float(msg.payload) <= 300) ):
                    if ( devicenumb == 1 ):
                        filename = "llv1"
                    elif ( devicenumb == 2 ):
                        filename = "llvs11"
                    elif ( devicenumb == 3 ):
                        filename = "llvs21"
                    f = open('/var/www/html/openWB/ramdisk/'+str(filename), 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (( "openWB/set/lp" in msg.topic) and ("VPhase2" in msg.topic)):
                devicenumb = int(re.sub(r'\D.', '', msg.topic))
                if ( (1 <= devicenumb <= 3) and (0 <= float(msg.payload) <= 300) ):
                    if ( devicenumb == 1 ):
                        filename = "llv2"
                    elif ( devicenumb == 2 ):
                        filename = "llvs12"
                    elif ( devicenumb == 3 ):
                        filename = "llvs22"
                    f = open('/var/www/html/openWB/ramdisk/'+str(filename), 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (( "openWB/set/lp" in msg.topic) and ("VPhase3" in msg.topic)):
                devicenumb = int(re.sub(r'\D.', '', msg.topic))
                if ( (1 <= devicenumb <= 3) and (0 <= float(msg.payload) <= 300) ):
                    if ( devicenumb == 1 ):
                        filename = "llv3"
                    elif ( devicenumb == 2 ):
                        filename = "llvs13"
                    elif ( devicenumb == 3 ):
                        filename = "llvs23"
                    f = open('/var/www/html/openWB/ramdisk/'+str(filename), 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (( "openWB/set/lp" in msg.topic) and ("APhase1" in msg.topic)):
                devicenumb = int(re.sub(r'\D.', '', msg.topic))
                if ( (1 <= devicenumb <= 3) and (0 <= float(msg.payload) <= 3000) ):
                    if ( devicenumb == 1 ):
                        filename = "lla1"
                    elif ( devicenumb == 2 ):
                        filename = "llas11"
                    elif ( devicenumb == 3 ):
                        filename = "llas21"
                    f = open('/var/www/html/openWB/ramdisk/'+str(filename), 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (( "openWB/set/lp" in msg.topic) and ("APhase2" in msg.topic)):
                devicenumb = int(re.sub(r'\D.', '', msg.topic))
                if ( (1 <= devicenumb <= 3) and (0 <= float(msg.payload) <= 3000) ):
                    if ( devicenumb == 1 ):
                        filename = "lla2"
                    elif ( devicenumb == 2 ):
                        filename = "llas12"
                    elif ( devicenumb == 3 ):
                        filename = "llas22"
                    f = open('/var/www/html/openWB/ramdisk/'+str(filename), 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (( "openWB/set/lp" in msg.topic) and ("APhase3" in msg.topic)):
                devicenumb = int(re.sub(r'\D.', '', msg.topic))
                if ( (1 <= devicenumb <= 3) and (0 <= float(msg.payload) <= 3000) ):
                    if ( devicenumb == 1 ):
                        filename = "lla3"
                    elif ( devicenumb == 2 ):
                        filename = "llas13"
                    elif ( devicenumb == 3 ):
                        filename = "llas23"
                    f = open('/var/www/html/openWB/ramdisk/'+str(filename), 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (( "openWB/set/lp" in msg.topic) and ("HzFrequenz" in msg.topic)):
                devicenumb = int(re.sub(r'\D', '', msg.topic))
                if ( (1 <= devicenumb <= 3) and (0 <= float(msg.payload) <= 80) ):
                    if ( devicenumb == 1 ):
                        filename = "llhz"
                    elif ( devicenumb == 2 ):
                        filename = "llhzs1"
                    elif ( devicenumb == 3 ):
                        filename = "llhzs2"
                    f = open('/var/www/html/openWB/ramdisk/'+str(filename), 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()

            # clear all set topics if not already done
            if ( not(setTopicCleared) ):
                client.publish(msg.topic, "", qos=0, retain=True)

        finally:
            lock.release()

client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker_ip, 1883)
client.loop_forever()
client.disconnect()
