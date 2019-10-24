import paho.mqtt.client as mqtt
from subprocess import Popen
import os
import sys
import subprocess
import time
import fileinput



def replaceAll(changeval,newval):
        for line in fileinput.input('openwb.conf', inplace=1):
            if line.startswith(changeval):
                line = changeval + newval + "\n"
            sys.stdout.write(line)

mqtt_broker_ip = "localhost"
client = mqtt.Client() 

# connect to broker and subscribe to set topics
def on_connect(client, userdata, flags, rc):
    #subscribe to all set topics
    client.subscribe("openWB/set/#")
# handle each set topic 
def on_message(client, userdata, msg): 
    if (msg.topic == "openWB/set/lademodus"):
        if (int(msg.payload) >= 0 and int(msg.payload) <=4):
            f = open('/var/www/html/openWB/ramdisk/lademodus', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
    if (msg.topic == "openWB/set/sofortladenstromstaerkelp1"):
        if (int(msg.payload) >= 6 and int(msg.payload) <=32):
            replaceAll("sofortll=",msg.payload.decode("utf-8"))
    if (msg.topic == "openWB/set/sofortladenstromstaerkelp2"):
        if (int(msg.payload) >= 6 and int(msg.payload) <=32):
            replaceAll("sofortlls1=",msg.payload.decode("utf-8"))
    if (msg.topic == "openWB/set/sofortladenstromstaerkelp3"):
        if (int(msg.payload) >= 6 and int(msg.payload) <=32):
            replaceAll("sofortlls2=",msg.payload.decode("utf-8"))
    if (msg.topic == "openWB/set/resetsofortladenlp1"):
        if (int(msg.payload) == 1):
            f = open('/var/www/html/openWB/ramdisk/aktgeladen', 'w')
            f.write("0")
            f.close()
            f = open('/var/www/html/openWB/ramdisk/gelrlp1', 'w')
            f.write("0")
            f.close()
            client.publish("openWB/set/resetsofortladenlp1", "0", qos=0, retain=True)
    if (msg.topic == "openWB/set/resetsofortladenlp2"):
        if (int(msg.payload) == 1):
            f = open('/var/www/html/openWB/ramdisk/aktgeladens1', 'w')
            f.write("0")
            f.close()
            f = open('/var/www/html/openWB/ramdisk/gelrlp2', 'w')
            f.write("0")
            f.close()
            client.publish("openWB/set/resetsofortladenlp2", "0", qos=0, retain=True)
    if (msg.topic == "openWB/set/resetsofortladenlp3"):
        if (int(msg.payload) == 1):
            f = open('/var/www/html/openWB/ramdisk/aktgeladens2', 'w')
            f.write("0")
            f.close()
            f = open('/var/www/html/openWB/ramdisk/gelrlp3', 'w')
            f.write("0")
            f.close()
            client.publish("openWB/set/resetsofortladenlp3", "0", qos=0, retain=True)
    if (msg.topic == "openWB/set/sofortladenlademengelp1"):
        if (int(msg.payload) >= 1 and int(msg.payload) <=100):
            replaceAll("lademkwh=",msg.payload.decode("utf-8"))
    if (msg.topic == "openWB/set/sofortladenlademengelp2"):
        if (int(msg.payload) >= 1 and int(msg.payload) <=100):
            replaceAll("lademkwhs1=",msg.payload.decode("utf-8"))
    if (msg.topic == "openWB/set/sofortladenlademengelp3"):
        if (int(msg.payload) >= 1 and int(msg.payload) <=100):
            replaceAll("lademkwhs2=",msg.payload.decode("utf-8"))
    if (msg.topic == "openWB/set/sofortladenuntermoduslp1"):
        if (int(msg.payload) == 0):
            replaceAll("lademstat=",msg.payload.decode("utf-8"))
            replaceAll("sofortsocstatlp1=",msg.payload.decode("utf-8"))
        if (int(msg.payload) == 1):
            replaceAll("lademstat=",msg.payload.decode("utf-8"))
            replaceAll("sofortsocstatlp1=","0")
        if (int(msg.payload) == 2):
            replaceAll("lademstat=","0")
            replaceAll("sofortsocstatlp1=","1")
    if (msg.topic == "openWB/set/sofortladenuntermoduslp2"):
        if (int(msg.payload) == 0):
            replaceAll("lademstats1=",msg.payload.decode("utf-8"))
            replaceAll("sofortsocstatlp2=",msg.payload.decode("utf-8"))
        if (int(msg.payload) == 1):
            replaceAll("lademstats1=",msg.payload.decode("utf-8"))
            replaceAll("sofortsocstatlp2=","0")
        if (int(msg.payload) == 2):
            replaceAll("lademstats1=","0")
            replaceAll("sofortsocstatlp2=","1")
    if (msg.topic == "openWB/set/sofortladenuntermoduslp3"):
        if (int(msg.payload) == 0):
            replaceAll("lademstats2=",msg.payload.decode("utf-8"))
            #replaceAll("sofortsocstatlp2=",msg.payload.decode("utf-8"))
        if (int(msg.payload) == 1):
            replaceAll("lademstats2=",msg.payload.decode("utf-8"))
            #replaceAll("sofortsocstatlp2=","0")
        #if (int(msg.payload) == 2):
        #    replaceAll("lademstats1=","0")
        #    replaceAll("sofortsocstatlp2=","1")
    if (msg.topic == "openWB/set/sofortladensoclp1"):
        if (int(msg.payload) >= 1 and int(msg.payload) <=100):
            replaceAll("sofortsoclp1=",msg.payload.decode("utf-8"))
    if (msg.topic == "openWB/set/sofortladensoclp2"):
        if (int(msg.payload) >= 1 and int(msg.payload) <=100):
            replaceAll("sofortsoclp2=",msg.payload.decode("utf-8"))





    print("Topic: ", msg.topic + "\nMessage: " + str(msg.payload.decode("utf-8"))) 

client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker_ip, 1883)
client.loop_forever()
client.disconnect()

