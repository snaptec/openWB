import paho.mqtt.client as mqtt
from subprocess import Popen
import os
import sys
import subprocess
import time
import fileinput
global inaction
inaction=0


def replaceAll(changeval,newval):
    global inaction
    if ( inaction == 0 ):
        inaction=1
        for line in fileinput.input('/var/www/html/openWB/openwb.conf', inplace=1):
            if line.startswith(changeval):
                line = changeval + newval + "\n"
            sys.stdout.write(line)
        time.sleep(0.1)
        inaction=0

mqtt_broker_ip = "localhost"
client = mqtt.Client() 

# connect to broker and subscribe to set topics
def on_connect(client, userdata, flags, rc):
    #subscribe to all set topics
    client.subscribe("openWB/set/#")
# handle each set topic 
def on_message(client, userdata, msg): 
    if (msg.topic == "openWB/set/ChargeMode"):
        if (int(msg.payload) >= 0 and int(msg.payload) <=4):
            f = open('/var/www/html/openWB/ramdisk/lademodus', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
            client.publish("openWB/global/ChargeMode", msg.payload.decode("utf-8"), qos=0, retain=True)
    if (msg.topic == "openWB/set/lp1/ChargePointEnabled"):
        if (int(msg.payload) >= 0 and int(msg.payload) <=1):
            f = open('/var/www/html/openWB/ramdisk/lp1enabled', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
            client.publish("openWB/lp/1/ChargePointEnabled", msg.payload.decode("utf-8"), qos=0, retain=True)
    if (msg.topic == "openWB/set/lp2/ChargePointEnabled"):
        if (int(msg.payload) >= 0 and int(msg.payload) <=1):
            f = open('/var/www/html/openWB/ramdisk/lp2enabled', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
            client.publish("openWB/lp/2/ChargePointEnabled", msg.payload.decode("utf-8"), qos=0, retain=True)
    if (msg.topic == "openWB/set/lp3/ChargePointEnabled"):
        if (int(msg.payload) >= 0 and int(msg.payload) <=1):
            f = open('/var/www/html/openWB/ramdisk/lp3enabled', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
            client.publish("openWB/lp/3/ChargePointEnabled", msg.payload.decode("utf-8"), qos=0, retain=True)
    if (msg.topic == "openWB/set/lp4/ChargePointEnabled"):
        if (int(msg.payload) >= 0 and int(msg.payload) <=1):
            f = open('/var/www/html/openWB/ramdisk/lp4enabled', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
            client.publish("openWB/lp/4/ChargePointEnabled", msg.payload.decode("utf-8"), qos=0, retain=True)
    if (msg.topic == "openWB/set/lp5/ChargePointEnabled"):
        if (int(msg.payload) >= 0 and int(msg.payload) <=1):
            f = open('/var/www/html/openWB/ramdisk/lp5enabled', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
            client.publish("openWB/lp/5/ChargePointEnabled", msg.payload.decode("utf-8"), qos=0, retain=True)
    if (msg.topic == "openWB/set/lp6/ChargePointEnabled"):
        if (int(msg.payload) >= 0 and int(msg.payload) <=1):
            f = open('/var/www/html/openWB/ramdisk/lp6enabled', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
            client.publish("openWB/lp/6/ChargePointEnabled", msg.payload.decode("utf-8"), qos=0, retain=True)
    if (msg.topic == "openWB/set/lp7/ChargePointEnabled"):
        if (int(msg.payload) >= 0 and int(msg.payload) <=1):
            f = open('/var/www/html/openWB/ramdisk/lp7enabled', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
            client.publish("openWB/lp/7/ChargePointEnabled", msg.payload.decode("utf-8"), qos=0, retain=True)
    if (msg.topic == "openWB/set/lp8/ChargePointEnabled"):
        if (int(msg.payload) >= 0 and int(msg.payload) <=1):
            f = open('/var/www/html/openWB/ramdisk/lp8enabled', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
            client.publish("openWB/lp/8/ChargePointEnabled", msg.payload.decode("utf-8"), qos=0, retain=True)
    if (msg.topic == "openWB/set/lp1/DirectChargeAmps"):
        if (int(msg.payload) >= 6 and int(msg.payload) <=32):
            f = open('/var/www/html/openWB/ramdisk/lp1sofortll', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
            client.publish("openWB/lp/1/ADirectModeAmps", msg.payload.decode("utf-8"), qos=0, retain=True)
    if (msg.topic == "openWB/set/lp2/DirectChargeAmps"):
        if (int(msg.payload) >= 6 and int(msg.payload) <=32):
            f = open('/var/www/html/openWB/ramdisk/lp2sofortll', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
            client.publish("openWB/lp/2/ADirectModeAmps", msg.payload.decode("utf-8"), qos=0, retain=True)
    if (msg.topic == "openWB/set/lp3/DirectChargeAmps"):
        if (int(msg.payload) >= 6 and int(msg.payload) <=32):
            f = open('/var/www/html/openWB/ramdisk/lp3sofortll', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
            client.publish("openWB/lp/3/ADirectModeAmps", msg.payload.decode("utf-8"), qos=0, retain=True)
    if (msg.topic == "openWB/set/lp4/DirectChargeAmps"):
        if (int(msg.payload) >= 6 and int(msg.payload) <=32):
            f = open('/var/www/html/openWB/ramdisk/lp4sofortll', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
            client.publish("openWB/lp/4/ADirectModeAmps", msg.payload.decode("utf-8"), qos=0, retain=True)
    if (msg.topic == "openWB/set/lp5/DirectChargeAmps"):
        if (int(msg.payload) >= 6 and int(msg.payload) <=32):
            f = open('/var/www/html/openWB/ramdisk/lp5sofortll', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
            client.publish("openWB/lp/5/ADirectModeAmps", msg.payload.decode("utf-8"), qos=0, retain=True)
    if (msg.topic == "openWB/set/lp8/DirectChargeAmps"):
        if (int(msg.payload) >= 6 and int(msg.payload) <=32):
            f = open('/var/www/html/openWB/ramdisk/lp8sofortll', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
            client.publish("openWB/lp/8/ADirectModeAmps", msg.payload.decode("utf-8"), qos=0, retain=True)
    if (msg.topic == "openWB/set/lp6/DirectChargeAmps"):
        if (int(msg.payload) >= 6 and int(msg.payload) <=32):
            f = open('/var/www/html/openWB/ramdisk/lp6sofortll', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
            client.publish("openWB/lp/6/ADirectModeAmps", msg.payload.decode("utf-8"), qos=0, retain=True)
    if (msg.topic == "openWB/set/lp7/DirectChargeAmps"):
        if (int(msg.payload) >= 6 and int(msg.payload) <=32):
            f = open('/var/www/html/openWB/ramdisk/lp7sofortll', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
            client.publish("openWB/lp/7/ADirectModeAmps", msg.payload.decode("utf-8"), qos=0, retain=True)
    if (msg.topic == "openWB/set/lp1/boolResetDirectCharge"):
        if (int(msg.payload) == 1):
            f = open('/var/www/html/openWB/ramdisk/aktgeladen', 'w')
            f.write("0")
            f.close()
            f = open('/var/www/html/openWB/ramdisk/gelrlp1', 'w')
            f.write("0")
            f.close()
            client.publish("openWB/set/lp1/boolResetDirectCharge", "0", qos=0, retain=True)
    if (msg.topic == "openWB/set/lp2/ResetDirectCharge"):
        if (int(msg.payload) == 1):
            f = open('/var/www/html/openWB/ramdisk/aktgeladens1', 'w')
            f.write("0")
            f.close()
            f = open('/var/www/html/openWB/ramdisk/gelrlp2', 'w')
            f.write("0")
            f.close()
            client.publish("openWB/set/lp2/boolResetDirectCharge", "0", qos=0, retain=True)
    if (msg.topic == "openWB/set/lp3/ResetDirectCharge"):
        if (int(msg.payload) == 1):
            f = open('/var/www/html/openWB/ramdisk/aktgeladens2', 'w')
            f.write("0")
            f.close()
            f = open('/var/www/html/openWB/ramdisk/gelrlp3', 'w')
            f.write("0")
            f.close()
            client.publish("openWB/set/lp2/boolResetDirectCharge", "0", qos=0, retain=True)
    if (msg.topic == "openWB/set/lp4/ResetDirectCharge"):
        if (int(msg.payload) == 1):
            f = open('/var/www/html/openWB/ramdisk/aktgeladenlp4', 'w')
            f.write("0")
            f.close()
            f = open('/var/www/html/openWB/ramdisk/gelrlp4', 'w')
            f.write("0")
            f.close()
            client.publish("openWB/set/lp4/boolResetDirectCharge", "0", qos=0, retain=True)
    if (msg.topic == "openWB/set/lp5/ResetDirectCharge"):
        if (int(msg.payload) == 1):
            f = open('/var/www/html/openWB/ramdisk/aktgeladenlp5', 'w')
            f.write("0")
            f.close()
            f = open('/var/www/html/openWB/ramdisk/gelrlp5', 'w')
            f.write("0")
            f.close()
            client.publish("openWB/set/lp5/boolResetDirectCharge", "0", qos=0, retain=True)
    if (msg.topic == "openWB/set/lp6/ResetDirectCharge"):
        if (int(msg.payload) == 1):
            f = open('/var/www/html/openWB/ramdisk/aktgeladenlp6', 'w')
            f.write("0")
            f.close()
            f = open('/var/www/html/openWB/ramdisk/gelrlp6', 'w')
            f.write("0")
            f.close()
            client.publish("openWB/set/lp6/boolResetDirectCharge", "0", qos=0, retain=True)
    if (msg.topic == "openWB/set/lp7/ResetDirectCharge"):
        if (int(msg.payload) == 1):
            f = open('/var/www/html/openWB/ramdisk/aktgeladenlp7', 'w')
            f.write("0")
            f.close()
            f = open('/var/www/html/openWB/ramdisk/gelrlp7', 'w')
            f.write("0")
            f.close()
            client.publish("openWB/set/lp7/boolResetDirectCharge", "0", qos=0, retain=True)
    if (msg.topic == "openWB/set/lp8/ResetDirectCharge"):
        if (int(msg.payload) == 1):
            f = open('/var/www/html/openWB/ramdisk/aktgeladenlp8', 'w')
            f.write("0")
            f.close()
            f = open('/var/www/html/openWB/ramdisk/gelrlp8', 'w')
            f.write("0")
            f.close()
            client.publish("openWB/set/lp4/boolResetDirectCharge", "0", qos=0, retain=True)
    if (msg.topic == "openWB/set/lp1/kWhDirectChargeToCharge"):
        if (int(msg.payload) >= 0 and int(msg.payload) <=100):
            replaceAll("lademkwh=",msg.payload.decode("utf-8"))
    if (msg.topic == "openWB/set/lp2/kWhDirectChargeToCharge"):
        if (int(msg.payload) >= 0 and int(msg.payload) <=100):
            replaceAll("lademkwhs1=",msg.payload.decode("utf-8"))
    if (msg.topic == "openWB/set/lp3/kWhDirectChargeToCharge"):
        if (int(msg.payload) >= 0 and int(msg.payload) <=100):
            replaceAll("lademkwhs2=",msg.payload.decode("utf-8"))
    if (msg.topic == "openWB/set/lp4/kWhDirectChargeToCharge"):
        if (int(msg.payload) >= 0 and int(msg.payload) <=100):
            replaceAll("lademkwhlp4=",msg.payload.decode("utf-8"))
    if (msg.topic == "openWB/set/lp5/kWhDirectChargeToCharge"):
        if (int(msg.payload) >= 0 and int(msg.payload) <=100):
            replaceAll("lademkwhlp5=",msg.payload.decode("utf-8"))

    if (msg.topic == "openWB/set/lp6/kWhDirectChargeToCharge"):
        if (int(msg.payload) >= 0 and int(msg.payload) <=100):
            replaceAll("lademkwhlp6=",msg.payload.decode("utf-8"))

    if (msg.topic == "openWB/set/lp7/kWhDirectChargeToCharge"):
        if (int(msg.payload) >= 0 and int(msg.payload) <=100):
            replaceAll("lademkwhlp7=",msg.payload.decode("utf-8"))

    if (msg.topic == "openWB/set/lp8/kWhDirectChargeToCharge"):
        if (int(msg.payload) >= 0 and int(msg.payload) <=100):
            replaceAll("lademkwhlp8=",msg.payload.decode("utf-8"))

    if (msg.topic == "openWB/set/lp1/DirectChargeSubMode"):
        if (int(msg.payload) == 0):
            replaceAll("lademstat=",msg.payload.decode("utf-8"))
            replaceAll("sofortsocstatlp1=",msg.payload.decode("utf-8"))
        if (int(msg.payload) == 1):
            replaceAll("lademstat=",msg.payload.decode("utf-8"))
            replaceAll("sofortsocstatlp1=","0")
        if (int(msg.payload) == 2):
            replaceAll("lademstat=","0")
            replaceAll("sofortsocstatlp1=","1")
    if (msg.topic == "openWB/set/lp2/DirectChargeSubMode"):
        if (int(msg.payload) == 0):
            replaceAll("lademstats1=",msg.payload.decode("utf-8"))
            replaceAll("sofortsocstatlp2=",msg.payload.decode("utf-8"))
        if (int(msg.payload) == 1):
            replaceAll("lademstats1=",msg.payload.decode("utf-8"))
            replaceAll("sofortsocstatlp2=","0")
        if (int(msg.payload) == 2):
            replaceAll("lademstats1=","0")
            replaceAll("sofortsocstatlp2=","1")
    if (msg.topic == "openWB/set/lp3/DirectChargeSubMode"):
        if (int(msg.payload) == 0):
            replaceAll("lademstats2=",msg.payload.decode("utf-8"))
            #replaceAll("sofortsocstatlp2=",msg.payload.decode("utf-8"))
        if (int(msg.payload) == 1):
            replaceAll("lademstats2=",msg.payload.decode("utf-8"))
            #replaceAll("sofortsocstatlp2=","0")
        #if (int(msg.payload) == 2):
        #    replaceAll("lademstats1=","0")
        #    replaceAll("sofortsocstatlp2=","1")
    if (msg.topic == "openWB/set/lp4/DirectChargeSubMode"):
        if (int(msg.payload) == 0):
            replaceAll("lademstatlp4=",msg.payload.decode("utf-8"))
        if (int(msg.payload) == 1):
            replaceAll("lademstatlp4=",msg.payload.decode("utf-8"))
    if (msg.topic == "openWB/set/lp5/DirectChargeSubMode"):
        if (int(msg.payload) == 0):
            replaceAll("lademstatlp5=",msg.payload.decode("utf-8"))
        if (int(msg.payload) == 1):
            replaceAll("lademstatlp5=",msg.payload.decode("utf-8"))
    if (msg.topic == "openWB/set/lp6/DirectChargeSubMode"):
        if (int(msg.payload) == 0):
            replaceAll("lademstatlp6=",msg.payload.decode("utf-8"))
        if (int(msg.payload) == 1):
            replaceAll("lademstatlp6=",msg.payload.decode("utf-8"))
    if (msg.topic == "openWB/set/lp7/DirectChargeSubMode"):
        if (int(msg.payload) == 0):
            replaceAll("lademstatlp7=",msg.payload.decode("utf-8"))
        if (int(msg.payload) == 1):
            replaceAll("lademstatlp7=",msg.payload.decode("utf-8"))
    if (msg.topic == "openWB/set/lp8/DirectChargeSubMode"):
        if (int(msg.payload) == 0):
            replaceAll("lademstatlp8=",msg.payload.decode("utf-8"))
        if (int(msg.payload) == 1):
            replaceAll("lademstatlp8=",msg.payload.decode("utf-8"))

    if (msg.topic == "openWB/set/lp1/DirectChargeSoc"):
        if (int(msg.payload) >= 1 and int(msg.payload) <=100):
            replaceAll("sofortsoclp1=",msg.payload.decode("utf-8"))
    if (msg.topic == "openWB/set/lp2/DirectChargeSoc"):
        if (int(msg.payload) >= 1 and int(msg.payload) <=100):
            replaceAll("sofortsoclp2=",msg.payload.decode("utf-8"))




    file = open('/var/www/html/openWB/ramdisk/mqtt.log', 'a')
    sys.stdout = file
    print("Topic: ", msg.topic + "\nMessage: " + str(msg.payload.decode("utf-8"))) 
    file.close()

client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker_ip, 1883)
client.loop_forever()
client.disconnect()

