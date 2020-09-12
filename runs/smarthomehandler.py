#!/usr/bin/python3
import paho.mqtt.client as mqtt
import time
import configparser
import urllib.request
import json
import os
import argparse
import re
import getopt
os.chdir('/var/www/html/openWB')
config = configparser.ConfigParser()
config.read('/var/www/html/openWB/smarthome.ini')
loglevel=2
DeviceValues = { }
DeviceTempValues = { }
DeviceCounters = { }
for i in range(0, 10):
    DeviceTempValues.update({'oldw'+str(i) : '2'})
    DeviceTempValues.update({'oldwh'+str(i) : '2'})
    DeviceTempValues.update({'oldtemp'+str(i) : '2'})
    DeviceTempValues.update({'oldtime'+str(i) : '2'})
    DeviceTempValues.update({'oldrelais'+str(i) : '2'})
    DeviceValues.update({ str(i)+"runningtime" : int(0)})
    DeviceValues.update( {str(i)+"WHImported_tmp" : int(0)})


global numberOfDevices
def logDebug(level, msg):
    if (int(level) >= int(loglevel)):
        file = open('/var/www/html/openWB/ramdisk/smarthome.log', 'a')
        if (int(level) == 0):
            file.write(time.ctime() + ': ' + str(msg)+ '\n')
        if (int(level) == 1):
            file.write(time.ctime() + ': ' + str(msg)+ '\n')
        if (int(level) == 2):
            file.write(time.ctime() + ': ' + str('\x1b[6;30;42m' + msg + '\x1b[0m')+ '\n')
        file.close()
def simcount(watt2, pref, importfn, exportfn, nummer):
    # emulate import  export
    seconds2= time.time()
    watt1=0
    seconds1=0.0
    if os.path.isfile('/var/www/html/openWB/ramdisk/'+pref+'sec0'): 
        f = open('/var/www/html/openWB/ramdisk/'+pref+'sec0', 'r')
        seconds1=float(f.read())
        f.close()
        f = open('/var/www/html/openWB/ramdisk/'+pref+'wh0', 'r')
        watt1=int(f.read())
        f.close()
        f = open('/var/www/html/openWB/ramdisk/'+pref+'watt0pos', 'r')
        wattposh=int(f.read())
        f.close()
        f = open('/var/www/html/openWB/ramdisk/'+pref+'watt0neg', 'r')
        wattnegh=int(f.read())
        f.close()
        f = open('/var/www/html/openWB/ramdisk/'+pref+'sec0', 'w')
        value1 = "%22.6f" % seconds2
        f.write(str(value1))
        f.close()
        f = open('/var/www/html/openWB/ramdisk/'+pref+'wh0', 'w')
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
        f = open('/var/www/html/openWB/ramdisk/'+pref+'watt0pos', 'w')
        f.write(str(wattposh))
        f.close()
        DeviceValues.update( {str(nummer) + "wpos" : wattposh})
        f = open('/var/www/html/openWB/ramdisk/'+pref+'watt0neg', 'w')
        f.write(str(wattnegh))
        f.close()
        f = open('/var/www/html/openWB/ramdisk/'+ importfn,'w')
        #    f = open('/var/www/html/openWB/ramdisk/speicherikwh', 'w')
        DeviceValues.update( {str(nummer) + "wh" : round(wattposkh, 2)})
        f.write(str(round(wattposkh, 2)))
        f.close()
        f = open('/var/www/html/openWB/ramdisk/' +exportfn , 'w')
        #   f = open('/var/www/html/openWB/ramdisk/speicherekwh', 'w')
        f.write(str(wattnegkh))
        f.close()
    else: 
        f = open('/var/www/html/openWB/ramdisk/'+pref+'sec0', 'w')
        value1 = "%22.6f" % seconds2
        f.write(str(value1))
        f.close()
        f = open('/var/www/html/openWB/ramdisk/'+pref+'wh0', 'w')
        f.write(str(watt2))
        f.close()

def publishmqtt(case):
    parser = argparse.ArgumentParser(description='openWB MQTT Publisher')
    parser.add_argument('--qos', '-q', metavar='qos', type=int, help='The QOS setting', default=0)
    parser.add_argument('--retain', '-r', dest='retain', action='store_true', help='If true, retain this publish')
    parser.set_defaults(retain=False)
    args = parser.parse_args()
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
                DeviceTempValues.update({'oldtime'+str(nummer) : DeviceValues[str(key)]})
        if ( "temp" in key):
            nummer = str(list(filter(str.isdigit, key))[0])
            if ( DeviceValues[str(key)] != DeviceTempValues['oldtemp' + str(nummer)]):   
                sensor = str(list(filter(str.isdigit, key))[1])
                client.publish("openWB/SmartHome/Devices/"+str(nummer)+"/TemperatureSensor"+str(sensor), payload=DeviceValues[str(key)], qos=0, retain=True)
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
            client.publish("openWB/SmartHome/Devices/"+str(nummer)+"/WHImported_temp", payload=DeviceValues[str(key)], qos=0, retain=True)
            client.loop(timeout=2.0)
    client.disconnect()

# Lese aus der Ramdisk Regelrelevante Werte ein
def loadregelvars():
    global uberschuss
    global speicherleistung
    global speichersoc
    global speichervorhanden
    global loglevel
    global reread
    global wattbezug
    try:
        with open('ramdisk/wattbezug', 'r') as value:
            wattbezug = int(float(value.read())) * -1
        with open('ramdisk/speichervorhanden', 'r') as value:
            speichervorhanden = int(value.read())
        if ( speichervorhanden == 1):
            with open('ramdisk/speicherleistung', 'r') as value:
                speicherleistung = int(float(value.read()))
                uberschuss = wattbezug + speicherleistung
            with open('ramdisk/speichersoc', 'r') as value:
                speichersoc = int(float(value.read()))
        else:
            speicherleistung = 0
            speichersoc = 100
            uberschuss = wattbezug
    except Exception as e:
        logDebug("2", "Fehler beim Auslesen der Ramdisk: " + str(e))
        wattbezug = 0
        uberschuss = 0
        speichervorhanden = 0
        speicherleistung = 0
        speichersoc = 0
    try:
        with open('ramdisk/smarthomehandlerloglevel', 'r') as value:
            loglevel = int(value.read())
    except:
            loglevel=2
            f = open('/var/www/html/openWB/ramdisk/smarthomehandlerloglevel', 'w')
            f.write(str(2))
            f.close()

    try:
        with open('ramdisk/rereadsmarthomedevices', 'r') as value:
            reread = int(value.read())
    except:
        reread = 1
        config.read('/var/www/html/openWB/smarthome.ini')
    if ( reread == 1):
        config.read('/var/www/html/openWB/smarthome.ini')
        f = open('/var/www/html/openWB/ramdisk/rereadsmarthomedevices', 'w')
        f.write(str(0))
        f.close()
        logDebug("2", "Config reRead")



    for i in range(1, 10):
        try:
            with open('ramdisk/smarthome_device_manual_' + str(i), 'r') as value:
                DeviceValues.update( {str(i) + "manual": int(value.read())}) 
        except:
            DeviceValues.update( {str(i) + "manual": 0})
    for i in range(1, 10):
        try:
            with open('ramdisk/smarthome_device_manual_control_' + str(i), 'r') as value:
                DeviceValues.update( {str(i) + "manualmodevar": int(value.read())}) 
        except:
            DeviceValues.update( {str(i) + "manualmodevar": 2})
    logDebug("0", "Wattbezug: " + str(wattbezug) + " Uberschuss: " + str(uberschuss) + " Speicherleistung: " + str(speicherleistung) + " SpeicherSoC: " + str(speichersoc))

def on_connect(client, userdata, flags, rc):
    client.subscribe("openWB/SmartHome/#", 2)
def on_message(client, userdata, msg):
    if (( "openWB/SmartHome/Device" in msg.topic) and ("WHImported_temp" in msg.topic)):
        devicenumb=re.sub('\D', '', msg.topic)
        if ( 1 <= int(devicenumb) <= 10 ):
            DeviceValues.update( {str(devicenumb)+"WHImported_tmp": int(msg.payload)})
    if (( "openWB/SmartHome/Device" in msg.topic) and ("RunningTimeToday" in msg.topic)):
        devicenumb=re.sub('\D', '', msg.topic)
        if ( 1 <= int(devicenumb) <= 10 ):
            DeviceValues.update( {str(devicenumb)+"runningtime": int(msg.payload)})


client = mqtt.Client("openWB-mqttsmarthome")

client.on_connect = on_connect
client.on_message = on_message
startTime = time.time()
waitTime = 3
client.connect("localhost")
while True:
    client.loop()
    client.subscribe("openWB/SmartHome/#", 2)
    elapsedTime = time.time() - startTime
    if elapsedTime > waitTime:
        client.disconnect()
        break
# Auslesen des Smarthome Devices (Watt und/oder Temperatur)
def getdevicevalues():
    DeviceList = [config.get('smarthomedevices', 'device_configured_1'), config.get('smarthomedevices', 'device_configured_2'), config.get('smarthomedevices', 'device_configured_3'), config.get('smarthomedevices', 'device_configured_4'), config.get('smarthomedevices', 'device_configured_5'), config.get('smarthomedevices', 'device_configured_6'), config.get('smarthomedevices', 'device_configured_7'), config.get('smarthomedevices', 'device_configured_8'), config.get('smarthomedevices', 'device_configured_9'), config.get('smarthomedevices', 'device_configured_10')] 
    numberOfDevices = 0
    for n in DeviceList:
        numberOfDevices += 1
        if ( n == "1" ):
            if ( config.get('smarthomedevices', 'device_type_'+str(numberOfDevices)) == "shelly"):
                try:
                    answer = json.loads(str(urllib.request.urlopen("http://"+config.get('smarthomedevices', 'device_ip_'+str(numberOfDevices))+"/status", timeout=3).read().decode("utf-8")))
                    watt = int(answer['meters'][0]['power'])
                    relais = int(answer['relays'][0]['ison'])
                    try:
                        anzahltemp = int(config.get('smarthomedevices', 'device_temperatur_configured_'+str(numberOfDevices)))
                        if ( anzahltemp > 0):
                            for i in range(anzahltemp):
                                temp = str(answer['ext_temperature'][str(i)]['tC'])
                                DeviceValues.update( {str(numberOfDevices) + "temp" + str(i) : temp })
                                f = open('/var/www/html/openWB/ramdisk/device' + str(numberOfDevices) + '_temp'+ str(i), 'w')
                                f.write(str(temp))
                                f.close()
                    except:
                        pass
                    DeviceValues.update( {str(numberOfDevices) + "watt" : watt})
                    DeviceValues.update( {str(numberOfDevices) + "relais" : relais})
                    f = open('/var/www/html/openWB/ramdisk/device' + str(numberOfDevices) + '_watt', 'w')
                    f.write(str(watt))
                    f.close()
                    f = open('/var/www/html/openWB/ramdisk/device' + str(numberOfDevices) + '_relais', 'w')
                    f.write(str(relais))
                    f.close()
                    try:
                        with open('/var/www/html/openWB/ramdisk/smarthome_device_' + str(numberOfDevices) + 'watt0pos', 'r') as value:
                            importtemp = int(value.read())
                        simcount(watt, "smarthome_device_"+ str(numberOfDevices), "device"+ str(numberOfDevices)+"_wh" ,"device"+ str(numberOfDevices)+"_whe", str(numberOfDevices))
                        importtemp1 = int(DeviceValues[str(numberOfDevices)+"wpos"])
                    except Exception as e: 
                        importtemp = int(DeviceValues[str(numberOfDevices)+"WHImported_tmp"])
                        f = open('/var/www/html/openWB/ramdisk/smarthome_device_' + str(numberOfDevices) + 'watt0pos', 'w')
                        f.write(str(importtemp))
                        f.close()
                        f = open('/var/www/html/openWB/ramdisk/smarthome_device_' + str(numberOfDevices) + 'watt0neg', 'w')
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
                            print(str(e))
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
                    logDebug("0", "Device: " + str(numberOfDevices) + " " + str(config.get('smarthomedevices', 'device_name_'+str(numberOfDevices))) + " relais: " + str(relais)  + " aktuell: " + str(watt))
                except Exception as e:
                    DeviceValues.update( {str(numberOfDevices) : "error"})
                    logDebug("2", "Device Shelly " + str(numberOfDevices) + str(config.get('smarthomedevices', 'device_name_'+str(numberOfDevices))) + " Fehlermeldung: " + str(e)) 
            #für später...
            if ( config.get('smarthomedevices', 'device_type_'+str(numberOfDevices)) == "http"):
                watt = int(str(urllib.request.urlopen("http://"+config.get('smarthomedevices', 'device_ip_'+str(numberOfDevices)), timeout=3).read().decode("utf-8")))
                DeviceValues.update( {str(numberOfDevices) : watt})
            if ( config.get('smarthomedevices', 'device_type_'+str(numberOfDevices)) == "tasmota"):
                try:
                    answer = json.loads(str(urllib.request.urlopen("http://"+config.get('smarthomedevices', 'device_ip_'+str(numberOfDevices))+"/cm?cmnd=Status%208", timeout=3).read().decode("utf-8")))
                    watt = int(answer['StatusSNS']['ENERGY']['Power'])
                    if ( int(answer['StatusSNS']['ENERGY']['Voltage']) > 50 ):
                        relais=1
                    else:
                        relais=0
                    DeviceValues.update( {str(numberOfDevices) + "watt" : watt})
                    DeviceValues.update( {str(numberOfDevices) + "relais" : relais})
                    f = open('/var/www/html/openWB/ramdisk/device' + str(numberOfDevices) + '_watt', 'w')
                    f.write(str(watt))
                    f.close()
                    f = open('/var/www/html/openWB/ramdisk/device' + str(numberOfDevices) + '_relais', 'w')
                    f.write(str(relais))
                    f.close()
                    try:
                        with open('/var/www/html/openWB/ramdisk/smarthome_device_' + str(numberOfDevices) + 'watt0pos', 'r') as value:
                            importtemp = int(value.read())
                        simcount(watt, "smarthome_device_"+ str(numberOfDevices), "device"+ str(numberOfDevices)+"_wh" ,"device"+ str(numberOfDevices)+"_whe", str(numberOfDevices))
                        importtemp1 = int(DeviceValues[str(numberOfDevices)+"wpos"])
                    except Exception as e: 
                        importtemp = int(DeviceValues[str(numberOfDevices)+"WHImported_tmp"])
                        f = open('/var/www/html/openWB/ramdisk/smarthome_device_' + str(numberOfDevices) + 'watt0pos', 'w')
                        f.write(str(importtemp))
                        f.close()
                        f = open('/var/www/html/openWB/ramdisk/smarthome_device_' + str(numberOfDevices) + 'watt0neg', 'w')
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
                            print(str(e))
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
                    logDebug("0", "Device: " + str(numberOfDevices) + " " + str(config.get('smarthomedevices', 'device_name_'+str(numberOfDevices))) + " relais: " + str(relais)  + " aktuell: " + str(watt))
                except Exception as e:
                    DeviceValues.update( {str(numberOfDevices) : "error"})
                    logDebug("2", "Device Shelly " + str(numberOfDevices) + str(config.get('smarthomedevices', 'device_name_'+str(numberOfDevices))) + " Fehlermeldung: " + str(e)) 

    publishmqtt("1")
def turndevicerelais(nummer, zustand):
    if ( config.get('smarthomedevices', 'device_type_'+str(nummer)) == "shelly"):
        if ( zustand == 1):
            try:
                urllib.request.urlopen("http://"+config.get('smarthomedevices', 'device_ip_'+str(nummer))+"/relay/0?turn=on", timeout=3)
                logDebug("1", "Device: " + str(nummer) + " " + str(config.get('smarthomedevices', 'device_name_'+str(nummer))) + " angeschaltet")
                DeviceCounters.update( {str(nummer) + "eintime" : time.time()})
            except Exception as e:
                logDebug("2", "Fehler beim Einschalten von Device " + str(nummer) + " Fehlermeldung: " + str(e))
        if ( zustand == 0):
            try:
                urllib.request.urlopen("http://"+config.get('smarthomedevices', 'device_ip_'+str(nummer))+"/relay/0?turn=off", timeout=3)
                logDebug("1", "Device: " + str(nummer) + " " + str(config.get('smarthomedevices', 'device_name_'+str(nummer))) + " ausgeschaltet")
            except Exception as e:
                logDebug("2", "Fehler beim Ausschalten von Device " + str(nummer) + " Fehlermeldung: " + str(e))
    if ( config.get('smarthomedevices', 'device_type_'+str(nummer)) == "tasmota"):
        if ( zustand == 1):
            try:
                urllib.request.urlopen("http://"+config.get('smarthomedevices', 'device_ip_'+str(nummer))+"/cm?cmnd=Power%20on", timeout=3)
                logDebug("1", "Device: " + str(nummer) + " " + str(config.get('smarthomedevices', 'device_name_'+str(nummer))) + " angeschaltet")
                DeviceCounters.update( {str(nummer) + "eintime" : time.time()})
            except Exception as e:
                logDebug("2", "Fehler beim Einschalten von Device " + str(nummer) + " Fehlermeldung: " + str(e))
        if ( zustand == 0):
            try:
                urllib.request.urlopen("http://"+config.get('smarthomedevices', 'device_ip_'+str(nummer))+"/cm?cmnd=Power%20off", timeout=3)
                logDebug("1", "Device: " + str(nummer) + " " + str(config.get('smarthomedevices', 'device_name_'+str(nummer))) + " ausgeschaltet")
            except Exception as e:
                logDebug("2", "Fehler beim Ausschalten von Device " + str(nummer) + " Fehlermeldung: " + str(e))

def conditions(nummer):
    try:
        speichersocbeforestop = int(config.get('smarthomedevices', 'device_speichersocbeforestop_'+str(nummer)))
    except:
        speichersocbeforestop = 0
    einschwelle = int(config.get('smarthomedevices', 'device_einschaltschwelle_'+str(nummer)))
    ausschwelle = int(config.get('smarthomedevices', 'device_ausschaltschwelle_'+str(nummer))) * -1
    einverz = int(config.get('smarthomedevices', 'device_einschaltverzoegerung_'+str(nummer))) * 60
    ausverz = int(config.get('smarthomedevices', 'device_ausschaltverzoegerung_'+str(nummer))) * 60
    mineinschaltdauer = int(config.get('smarthomedevices', 'device_mineinschaltdauer_'+str(nummer))) * 60
    maxeinschaltdauer = int(config.get('smarthomedevices', 'device_maxeinschaltdauer_'+str(nummer))) * 60
    name = str(config.get('smarthomedevices', 'device_name_'+str(nummer)))
    if ( maxeinschaltdauer > int(DeviceValues[str(nummer)+"runningtime"])):
        logDebug("0","Device: " + str(nummer) + " " + str(name) + " Maximale Einschaltdauer noch nicht erreicht")
    else:
        if ( DeviceValues[str(nummer)+"relais"] == 1 ):
            logDebug("1","Device: " + str(nummer) + " " + str(name) + " Maximale Einschaltdauer erreicht schalte ab")
            turndevicerelais(nummer, 0)
        else:
            logDebug("0","Device: " + str(nummer) + " " + str(name) + " Maximale Einschaltdauer erreicht bereits abgeschaltet")
        return

    if ( uberschuss > einschwelle):
        try:
            del DeviceCounters[str(nummer)+"ausverz"]
        except:
            pass
        logDebug("0","Device: " + str(nummer) + " " + str(config.get('smarthomedevices', 'device_name_'+str(nummer)))+ " Überschuss größer Einschaltschwelle")
        if ( DeviceValues[str(nummer)+"relais"] == 0 ):
            if  str(nummer)+"einverz" in DeviceCounters:
                timesince = int(time.time()) - int(DeviceCounters[str(nummer)+"einverz"])
                if ( einverz < timesince ):
                    logDebug("1","Device: " + str(nummer) + " " + str(name)  + " Einschaltverzögerung erreicht, schalte ein bei " + str(einschwelle))
                    turndevicerelais(nummer, 1)
                    del DeviceCounters[str(nummer)+"einverz"]
                else:
                    logDebug("1","Device: " + str(nummer) + " " + str(name) + " Einschaltverzögerung noch nicht erreicht. " + str(einverz) + " ist größer als " + str(timesince))
            else:
                DeviceCounters.update( {str(nummer) + "einverz" : time.time()})
                logDebug("1","Device: " + str(nummer) + " " + str(name) + " Einschaltverzögerung gestartet")
        else:
            logDebug("0","Device: " + str(nummer) + " " + str(name)+ " Einschaltverzögerung erreicht, bereits eingeschaltet")
            try:
                del DeviceCounters[str(nummer)+"einverz"]
            except:
                pass
    else:
        try:
            del DeviceCounters[str(nummer)+"einverz"]
        except:
            pass
        if ( uberschuss < ausschwelle):
            if ( speichersoc > speichersocbeforestop ):
                logDebug("0","Device: " + str(nummer) + " " + str(name)+ " SoC höher als Abschalt SoC, lasse Gerät weiterlaufen")
                return
            else:
                logDebug("0","Device: " + str(nummer) + " " + str(name)+ " SoC niedriger als Abschalt SoC, prüfe weitere Bedingungen")
            logDebug("0","Device: " + str(nummer) + " " + str(name)+ "Überschuss kleiner Ausschaltschwelle")
            if ( DeviceValues[str(nummer)+"relais"] == 1 ):
                if  str(nummer)+"ausverz" in DeviceCounters:
                    timesince = int(time.time()) - int(DeviceCounters[str(nummer)+"ausverz"])
                    if ( ausverz < timesince ):
                        if  str(nummer)+"eintime" in DeviceCounters:
                            timestart = int(time.time()) - int(DeviceCounters[str(nummer)+"eintime"])
                            if ( mineinschaltdauer < timestart):
                                logDebug("1","Device: " + str(nummer) + " " + str(name)  + " Ausschaltverzögerung & Mindesteinschaltdauer erreicht, schalte aus bei " + str(ausschwelle))
                                turndevicerelais(nummer, 0)
                                del DeviceCounters[str(nummer)+"ausverz"]
                            else:
                                logDebug("1","Device: " + str(nummer) + " " + str(name)  + " Ausschaltverzögerung erreicht, Mindesteinschaltdauer noch nicht erreicht, " + str(mineinschaltdauer) + " ist größer als " + str(timestart))
                        else:
                            logDebug("1","Device: " + str(nummer) + " " + str(name)+ " Mindesteinschaltdauer nicht bekannt, schalte aus")
                            turndevicerelais(nummer, 0)
                    else:
                        logDebug("1","Device: " + str(nummer) + " " + str(name) + " Ausschaltverzögerung noch nicht erreicht. " + str(ausverz) + " ist größer als " + str(timesince))
                else:
                    DeviceCounters.update( {str(nummer) + "ausverz" : time.time()})
                    logDebug("1","Device: " + str(nummer) + " " + str(name) + " Ausschaltverzögerung gestartet")
            else:
                logDebug("0","Device: " + str(nummer) + " " + str(name)+ " Ausschaltverzögerung erreicht, bereits ausgeschaltet")
                try:
                    del DeviceCounters[str(nummer)+"ausverz"]
                except:
                    pass
        else:
            logDebug("0","Device: " + str(nummer) + " " + str(name) + " Überschuss kleiner als Einschaltschwelle und größer als Ausschaltschwelle")
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

    hour=time.strftime("%H")
    if (int(hour) == 0):
        try:
            if (int(resetmaxeinschaltdauer) == 0):
                for i in range(0, 10):
                    DeviceValues.update({str(i) + "runningtime" : '0'})
                resetmaxeinschaltdauer=1
        except:
            resetmaxeinschaltdauer=0
    if (int(hour) == 2):
        resetmaxeinschaltdauer=0
while True:
    config.read('/var/www/html/openWB/smarthome.ini')
    loadregelvars()
    getdevicevalues()
    resetmaxeinschaltdauerfunc()
    for i in range(1,11):
        try:
            configured = config.get('smarthomedevices', 'device_configured_' + str(i))
            if (configured == "1"):
                if ( DeviceValues[str(i)+"manual"] == 1 ):
                    if ( DeviceValues[str(i)+"manualmodevar"] == 0 ):
                        if ( DeviceValues[str(i)+"relais"] == 1 ):
                            turndevicerelais(i, 0)
                    if ( DeviceValues[str(i)+"manualmodevar"] == 1 ):
                        if ( DeviceValues[str(i)+"relais"] == 0 ):
                            turndevicerelais(i, 1)
                    logDebug("0","Device: " + str(i) + " " + str(config.get('smarthomedevices', 'device_name_'+str(i))) + " manueller Modus aktiviert, führe keine Regelung durch")
                else:
                    try:
                        conditions(int(i))
                    except Exception as e:
                        logDebug("2", "Conditions Device: " + str(i) + " " + str(config.get('smarthomedevices', 'device_name_'+str(i))) + str(e))
        except Exception as e:
            logDebug("2", "Main routine Device: " + str(i) + " " + str(config.get('smarthomedevices', 'device_name_'+str(i))) + str(e))
    #conditions(2)
    #if "2eintime" in DeviceCounters:
    #    print(DeviceCounters["2eintime"])
    time.sleep(5)
    #except:
    #exit()
