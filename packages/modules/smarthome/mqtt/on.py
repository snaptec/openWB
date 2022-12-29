#!/usr/bin/python3
import sys
import os
import time
import json
import getopt
import socket
import struct
import codecs
import binascii
import paho.mqtt.client as mqtt
numberOfSupportedDevices=9 # limit number of smarthome devices
def on_connect(client, userdata, flags, rc):
    client.subscribe("openWB/SmartHome/set/Devices/#", 2)
def on_message(client, userdata, msg):
    global numberOfSupportedDevices
devicenumber=str(sys.argv[1])
ipadr=str(sys.argv[2])
uberschuss=int(sys.argv[3])
client = mqtt.Client("openWB-mqttsmarthomecust")
client.on_connect = on_connect
client.on_message = on_message
startTime = time.time()
waitTime = 2
client.connect("localhost")
while True:
    client.loop()
    elapsedTime = time.time() - startTime
    if elapsedTime > waitTime:
        break
client.publish("openWB/SmartHome/set/Devices/"+str(devicenumber)+"/ReqRelay", "1", qos=0, retain=True)
client.loop(timeout=2.0)
client.publish("openWB/SmartHome/set/Devices/"+str(devicenumber)+"/Ueberschuss", payload=str(uberschuss), qos=0, retain=True)
client.loop(timeout=2.0)
client.disconnect()
named_tuple = time.localtime() # getstruct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S mqtt on.py", named_tuple)
file_string= '/var/www/html/openWB/ramdisk/smarthome_device_' + str(devicenumber) + '_mqtt.log'
file_stringpv= '/var/www/html/openWB/ramdisk/smarthome_device_' + str(devicenumber) + '_pv'
if os.path.isfile(file_string):
   f = open( file_string , 'a')
else:
   f = open( file_string , 'w')
print ('%s devicenr %s ueberschuss %6d /ReqRelay = 1' % (time_string,devicenumber,uberschuss),file=f)
f.close()
f = open( file_stringpv , 'w')
f.write(str(1))
f.close()

