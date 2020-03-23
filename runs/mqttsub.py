import paho.mqtt.client as mqtt
from subprocess import Popen
import os
import sys
import subprocess
import time
import fileinput
from datetime import datetime
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

def getserial():
    # Extract serial from cpuinfo file
    with open('/proc/cpuinfo','r') as f:
        for line in f:
            if line[0:6] == 'Serial':
                return line[10:26]
        return "0000000000000000"

mqtt_broker_ip = "localhost"
client = mqtt.Client("openWB-mqttsub-" + getserial())

# connect to broker and subscribe to set topics
def on_connect(client, userdata, flags, rc):
    #subscribe to all set topics
    client.subscribe("openWB/set/#", 2)

# handle each set topic
def on_message(client, userdata, msg):
    if (msg.topic == "openWB/set/configure/AllowedTotalCurrentPerPhase"):
        if (float(msg.payload) >= 0 and float(msg.payload) <=200):
            f = open('/var/www/html/openWB/ramdisk/AllowedTotalCurrentPerPhase', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
    if (msg.topic == "openWB/set/configure/AllowedRfidsForLp1"):
        f = open('/var/www/html/openWB/ramdisk/AllowedRfidsForLp1', 'w')
        f.write(msg.payload.decode("utf-8"))
        f.close()
    if (msg.topic == "openWB/set/configure/TotalCurrentConsumptionOnL1"):
        if (float(msg.payload) >= 0 and float(msg.payload) <=200):
            f = open('/var/www/html/openWB/ramdisk/TotalCurrentConsumptionOnL1', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
    if (msg.topic == "openWB/set/configure/ChargingVehiclesOnL1"):
        if (int(msg.payload) >= 0 and int(msg.payload) <=200):
            f = open('/var/www/html/openWB/ramdisk/ChargingVehiclesOnL1', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
    if (msg.topic == "openWB/set/system/ChangeVar"):
        if msg.payload:
            splitvar=msg.payload.decode("utf-8").split("=", 1)
            sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", splitvar[0], splitvar[1]]
            subprocess.Popen(sendcommand)
            client.publish("openWB/set/system/ChangeVar", "", qos=0, retain=True)
    if (msg.topic == "openWB/set/system/GetVar"):
        if msg.payload:
            with open('/var/www/html/openWB/openwb.conf') as f:
                datafile = f.readlines()
            for line in datafile:
                if msg.payload.decode("utf-8") in line:
                    if "pass" not in line:
                        client.publish("openWB/set/system/AskedVar", line, qos=0, retain=True)
            client.publish("openWB/set/system/GetVar", "", qos=0, retain=True)  
    if (msg.topic == "openWB/set/system/PerformUpdate"):
        if (int(msg.payload) == 1):
            client.publish("openWB/set/system/PerformUpdate", "0", qos=0, retain=True)
            subprocess.Popen("/var/www/html/openWB/runs/update.sh");
    if (msg.topic == "openWB/set/system/SendDebug"):
        if (int(msg.payload) == 1):
            client.publish("openWB/set/system/SendDebug", "0", qos=0, retain=True)
            subprocess.Popen("/var/www/html/openWB/runs/senddebuginit.sh");
    if (msg.topic == "openWB/set/graph/RequestLiveGraph"):
        if (int(msg.payload) == 1):
            subprocess.Popen("/var/www/html/openWB/runs/sendlivegraphdata.sh")
        else:
            client.publish("openWB/system/LiveGraphData", "empty", qos=0, retain=True)
    if (msg.topic == "openWB/set/graph/RequestDayGraph"):
        if (int(msg.payload) >= 1 and int(msg.payload) <= 20501231):
            sendcommand = ["/var/www/html/openWB/runs/senddaygraphdata.sh", msg.payload]
            subprocess.Popen(sendcommand)
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
    if (msg.topic == "openWB/set/graph/RequestMonthGraph"):
        if (int(msg.payload) >= 1 and int(msg.payload) <= 205012):
            sendcommand = ["/var/www/html/openWB/runs/sendmonthgraphdata.sh", msg.payload]
            subprocess.Popen(sendcommand)
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
    if (msg.topic == "openWB/set/RenewMQTT"):
        if (int(msg.payload) == 1):
            client.publish("openWB/set/RenewMQTT", "0", qos=0, retain=True)
            #time.sleep(0.5)
            #subprocess.Popen("/var/www/html/openWB/runs/renewmqtt.sh")
            f = open('/var/www/html/openWB/ramdisk/renewmqtt', 'w')
            f.write("1")
            f.close()
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
    if (msg.topic == "openWB/set/awattar/MaxPriceForCharging"):
        if (float(msg.payload) >= -8 and float(msg.payload) <=50):
            f = open('/var/www/html/openWB/ramdisk/awattarmaxprice', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
    if (msg.topic == "openWB/set/HouseBattery/W"):
        if (float(msg.payload) >= -30000 and float(msg.payload) <= 30000):
            f = open('/var/www/html/openWB/ramdisk/speicherleistung', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
    if (msg.topic == "openWB/set/HouseBattery/WhImported"):
        if (float(msg.payload) >= 0 and float(msg.payload) <= 9000000):
            f = open('/var/www/html/openWB/ramdisk/speicherikwh', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
    if (msg.topic == "openWB/set/HouseBattery/WhExported"):
        if (float(msg.payload) >= 0 and float(msg.payload) <= 9000000):
            f = open('/var/www/html/openWB/ramdisk/speicherekwh', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
    if (msg.topic == "openWB/set/HouseBattery/%Soc"):
        if (float(msg.payload) >= 0 and float(msg.payload) <= 100):
            f = open('/var/www/html/openWB/ramdisk/speichersoc', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
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
    if (msg.topic == "openWB/set/pv/WhCounter"):
        if (float(msg.payload) >= 0 and float(msg.payload) <= 10000000000):
            f = open('/var/www/html/openWB/ramdisk/pvkwh', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
    if (msg.topic == "openWB/set/pv/W"):
        if (float(msg.payload) >= -10000000 and float(msg.payload) <= 100000000):
            if (float(msg.payload) > 1):
                pvwatt=int(msg.payload.decode("utf-8")) * -1
            else:
                pvwatt=int(msg.payload.decode("utf-8"))
            f = open('/var/www/html/openWB/ramdisk/pvwatt', 'w')
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


    theTime = datetime.now()
    timestamp = theTime.strftime(format = "%Y-%m-%d %H:%M:%S")
    file = open('/var/www/html/openWB/ramdisk/mqtt.log', 'a')
    sys.stdout = file
    print(timestamp + " Topic: " + msg.topic + "\nMessage: " + str(msg.payload.decode("utf-8")))
    file.close()

client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker_ip, 1883)
client.loop_forever()
client.disconnect()
