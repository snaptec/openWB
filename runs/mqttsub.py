import paho.mqtt.client as mqtt
from subprocess import Popen
import os
import sys
import subprocess
import time
import fileinput
from datetime import datetime
import configparser
import re
global inaction
inaction=0
config = configparser.ConfigParser()
shconfigfile='/var/www/html/openWB/smarthome.ini'
config.read(shconfigfile)

for i in range(1,11):
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

    if (( "openWB/set/lp" in msg.topic) and ("ChargePointEnabled" in msg.topic)):
        devicenumb=re.sub('\D', '', msg.topic)
        if ( 1 <= int(devicenumb) <= 8 and 0 <= int(msg.payload) <= 1):
            f = open('/var/www/html/openWB/ramdisk/lp'+str(devicenumb)+'enabled', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
            client.publish("openWB/lp/"+str(devicenumb)+"/ChargePointEnabled", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/set/lp/"+str(devicenumb)+"/ChargePointEnabled", "", qos=0, retain=True)

    if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_configured" in msg.topic)):
        devicenumb=re.sub('\D', '', msg.topic)
        if ( 1 <= int(devicenumb) <= 10 and 0 <= int(msg.payload) <= 1):
            writetoconfig(shconfigfile,'smarthomedevices','device_configured_'+str(devicenumb),msg.payload.decode("utf-8"))
            client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_configured", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/SmartHome/Devices/"+str(devicenumb)+"/device_configured", "", qos=0, retain=True)
    if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_ip" in msg.topic)):
        devicenumb=re.sub('\D', '', msg.topic)
        if ( 1 <= int(devicenumb) <= 10 and len(str(msg.payload)) > 6 and bool(re.match(ipallowed, msg.payload.decode("utf-8")))):
            writetoconfig(shconfigfile,'smarthomedevices','device_ip_'+str(devicenumb), msg.payload.decode("utf-8"))
            client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_ip", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/SmartHome/Devices/"+str(devicenumb)+"/device_ip", "", qos=0, retain=True)
    if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_name" in msg.topic)):
        devicenumb=re.sub('\D', '', msg.topic)
        if ( 1 <= int(devicenumb) <= 10 and  3 <= len(str(msg.payload)) <= 12 and bool(re.match(nameallowed, msg.payload.decode("utf-8")))):
            writetoconfig(shconfigfile,'smarthomedevices','device_name_'+str(devicenumb), msg.payload.decode("utf-8"))
            client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_name", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/SmartHome/Devices/"+str(devicenumb)+"/device_name", "", qos=0, retain=True)
    if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_type" in msg.topic)):
        devicenumb=re.sub('\D', '', msg.topic)
        if ( 1 <= int(devicenumb) <= 10 and len(str(msg.payload)) > 6):
            if ( msg.payload.decode("utf-8") == "tasmota" or msg.payload.decode("utf-8") == "shelly"):
                writetoconfig(shconfigfile,'smarthomedevices','device_type_'+str(devicenumb), msg.payload.decode("utf-8"))
                client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_type", msg.payload.decode("utf-8"), qos=0, retain=True)
                client.publish("openWB/config/set/SmartHome/Devices/"+str(devicenumb)+"/device_type", "", qos=0, retain=True)
    if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_temperatur_configured" in msg.topic)):
        devicenumb=re.sub('\D', '', msg.topic)
        if ( 1 <= int(devicenumb) <= 10 and 0 <= int(msg.payload) <= 3):
            writetoconfig(shconfigfile,'smarthomedevices','device_temperatur_configured_'+str(devicenumb), msg.payload.decode("utf-8"))
            client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_temperatur_configured", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/SmartHome/Devices/"+str(devicenumb)+"/device_temperatur_configured", "", qos=0, retain=True)
    if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_einschaltschwelle" in msg.topic)):
        devicenumb=re.sub('\D', '', msg.topic)
        if ( 1 <= int(devicenumb) <= 10 and -100000 <= int(msg.payload) <= 100000):
            writetoconfig(shconfigfile,'smarthomedevices','device_einschaltschwelle_'+str(devicenumb), msg.payload.decode("utf-8"))
            client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_einschaltschwelle", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/SmartHome/Devices/"+str(devicenumb)+"/device_einschaltschwelle", "", qos=0, retain=True)
    if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_ausschaltschwelle" in msg.topic)):
        devicenumb=re.sub('\D', '', msg.topic)
        if ( 1 <= int(devicenumb) <= 10 and -100000 <= int(msg.payload) <= 100000):
            writetoconfig(shconfigfile,'smarthomedevices','device_ausschaltschwelle_'+str(devicenumb), msg.payload.decode("utf-8"))
            client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_ausschaltschwelle", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/SmartHome/Devices/"+str(devicenumb)+"/device_ausschaltschwelle", "", qos=0, retain=True)
    if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_ausschaltverzoegerung" in msg.topic)):
        devicenumb=re.sub('\D', '', msg.topic)
        if ( 1 <= int(devicenumb) <= 10 and 0 <= int(msg.payload) <= 10000):
            writetoconfig(shconfigfile,'smarthomedevices','device_ausschaltverzoegerung_'+str(devicenumb), msg.payload.decode("utf-8"))
            client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_ausschaltverzoegerung", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/SmartHome/Devices/"+str(devicenumb)+"/device_ausschaltverzoegerung", "", qos=0, retain=True)
    if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_einschaltverzoegerung" in msg.topic)):
        devicenumb=re.sub('\D', '', msg.topic)
        if ( 1 <= int(devicenumb) <= 10 and 0 <= int(msg.payload) <= 100000):
            writetoconfig(shconfigfile,'smarthomedevices','device_einschaltverzoegerung_'+str(devicenumb), msg.payload.decode("utf-8"))
            client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_einschaltverzoegerung", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/SmartHome/Devices/"+str(devicenumb)+"/device_einschaltverzoegerung", "", qos=0, retain=True)
    if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_speichersocbeforestop" in msg.topic)):
        devicenumb=re.sub('\D', '', msg.topic)
        if ( 1 <= int(devicenumb) <= 10 and 0 <= int(msg.payload) <= 100):
            writetoconfig(shconfigfile,'smarthomedevices','device_speichersocbeforestop_'+str(devicenumb), msg.payload.decode("utf-8"))
            client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_speichersocbeforestop", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/SmartHome/Devices/"+str(devicenumb)+"/device_speichersocbeforestop", "", qos=0, retain=True)
    if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_maxeinschaltdauer" in msg.topic)):
        devicenumb=re.sub('\D', '', msg.topic)
        if ( 1 <= int(devicenumb) <= 10 and 0 <= int(msg.payload) <= 100000):
            writetoconfig(shconfigfile,'smarthomedevices','device_maxeinschaltdauer_'+str(devicenumb), msg.payload.decode("utf-8"))
            client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_maxeinschaltdauer", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/SmartHome/Devices/"+str(devicenumb)+"/device_maxeinschaltdauer", "", qos=0, retain=True)
    if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_mineinschaltdauer" in msg.topic)):
        devicenumb=re.sub('\D', '', msg.topic)
        if ( 1 <= int(devicenumb) <= 10 and 0 <= int(msg.payload) <= 100000):
            writetoconfig(shconfigfile,'smarthomedevices','device_mineinschaltdauer_'+str(devicenumb), msg.payload.decode("utf-8"))
            client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_mineinschaltdauer", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/SmartHome/Devices/"+str(devicenumb)+"/device_mineinschaltdauer", "", qos=0, retain=True)
    if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("device_manual_control" in msg.topic)):
        devicenumb=re.sub('\D', '', msg.topic)
        if ( 1 <= int(devicenumb) <= 10 and 0 <= int(msg.payload) <= 1):
            client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/device_manual_control", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/SmartHome/Devices/"+str(devicenumb)+"/device_manual_control", "", qos=0, retain=True)
            f = open('/var/www/html/openWB/ramdisk/smarthome_device_manual_control_'+str(devicenumb), 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
    if (( "openWB/config/set/SmartHome/Device" in msg.topic) and ("mode" in msg.topic)):
        devicenumb=re.sub('\D', '', msg.topic)
        if ( 1 <= int(devicenumb) <= 10 and 0 <= int(msg.payload) <= 1):
            client.publish("openWB/config/get/SmartHome/Devices/"+str(devicenumb)+"/mode", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/SmartHome/Devices/"+str(devicenumb)+"/mode", "", qos=0, retain=True)
            f = open('/var/www/html/openWB/ramdisk/smarthome_device_manual_'+str(devicenumb), 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
    if (( "openWB/config/set/sofort/lp" in msg.topic) and ("current" in msg.topic)):
        devicenumb=re.sub('\D', '', msg.topic)
        if ( 1 <= int(devicenumb) <= 8 and 6 <= int(msg.payload) <= 32):
            client.publish("openWB/config/get/sofort/lp/"+str(devicenumb)+"/current", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/sofort/lp/"+str(devicenumb)+"/current", "", qos=0, retain=True)
            f = open('/var/www/html/openWB/ramdisk/lp'+str(devicenumb)+'sofortll', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
    if (( "openWB/config/set/sofort/lp" in msg.topic) and ("energyToCharge" in msg.topic)):
        devicenumb=re.sub('\D', '', msg.topic)
        if ( 1 <= int(devicenumb) <= 8 and 0 <= int(msg.payload) <= 100):
            if ( int(devicenumb) == 1):
                sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "lademkwh=", msg.payload.decode("utf-8")]
                subprocess.Popen(sendcommand)
            if (int(devicenumb) == 2):
                sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "lademkwhs1=", msg.payload.decode("utf-8")]
                subprocess.Popen(sendcommand)
            if (int(devicenumb) == 3):
                sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "lademkwhs2=", msg.payload.decode("utf-8")]
                subprocess.Popen(sendcommand)
            if (int(devicenumb) >= 4):
                sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "lademkwhlp"+str(devicenumb)+"=", msg.payload.decode("utf-8")]
                subprocess.Popen(sendcommand)

            client.publish("openWB/config/get/sofort/lp/"+str(devicenumb)+"/energyToCharge", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/sofort/lp/"+str(devicenumb)+"/energyToCharge", "", qos=0, retain=True)
    if (( "openWB/config/set/sofort/lp" in msg.topic) and ("resetEnergyToCharge" in msg.topic)):
        devicenumb=re.sub('\D', '', msg.topic)
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
            client.publish("openWB/config/set/sofort/lp/"+str(devicenumb)+"/resetEnergyToCharge", "", qos=0, retain=True)
    if (( "openWB/config/set/sofort/lp" in msg.topic) and ("socToChargeTo" in msg.topic)):
        devicenumb=re.sub('\D', '', msg.topic)
        if ( 1 <= int(devicenumb) <= 2 and 0 <= int(msg.payload) <= 100):
            client.publish("openWB/config/get/sofort/lp/"+str(devicenumb)+"/socToChargeTo", msg.payload.decode("utf-8"), qos=0, retain=True)
            sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "sofortsoclp"+str(devicenumb)+"=", msg.payload.decode("utf-8")]
            subprocess.Popen(sendcommand)
            client.publish("openWB/config/set/sofort/lp/"+str(devicenumb)+"/socToChargeTo", "", qos=0, retain=True)
    if (( "openWB/config/set/sofort/lp" in msg.topic) and ("chargeLimitation" in msg.topic)):
        devicenumb=re.sub('\D', '', msg.topic)
        if ( 3 <= int(devicenumb) <= 8 and 0 <= int(msg.payload) <= 1):
            sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "msmoduslp"+str(devicenumb)+"=", msg.payload.decode("utf-8")]
            subprocess.Popen(sendcommand)
            time.sleep(0.4)
            if (int(msg.payload) == 1):
                sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "lademstatlp"+str(devicenumb)+"=", "1"]
                subprocess.Popen(sendcommand)
                client.publish("openWB/lp/5/boolDirectModeChargekWh", msg.payload.decode("utf-8"), qos=0, retain=True)
            else:
                sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "lademstatlp"+str(devicenumb)+"=", "0"]
                subprocess.Popen(sendcommand)
                client.publish("openWB/lp/5/boolDirectModeChargekWh", "0", qos=0, retain=True)

            client.publish("openWB/config/get/sofort/lp/"+str(devicenumb)+"/chargeLimitation", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/sofort/lp/"+str(devicenumb)+"/chargeLimitation", "", qos=0, retain=True)


    if (msg.topic == "openWB/config/set/pv/minFeedinPowerBeforeStart"):
        if (int(msg.payload) >= -100000 and int(msg.payload) <= 100000):
            sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "mindestuberschuss=", msg.payload.decode("utf-8")]
            subprocess.Popen(sendcommand)
            client.publish("openWB/config/get/pv/minFeedinPowerBeforeStart", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/pv/minFeedinPowerBeforeStart", "", qos=0, retain=True)
    if (msg.topic == "openWB/config/set/pv/maxPowerConsumptionBeforeStop"):
        if (int(msg.payload) >= -100000 and int(msg.payload) <= 100000):
            sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "abschaltuberschuss=", msg.payload.decode("utf-8")]
            subprocess.Popen(sendcommand)
            client.publish("openWB/config/get/pv/maxPowerConsumptionBeforeStop", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/pv/maxPowerConsumptionBeforeStop", "", qos=0, retain=True)
    if (msg.topic == "openWB/config/set/pv/stopDelay"):
        if (int(msg.payload) >= 0 and int(msg.payload) <= 10000):
            sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "abschaltverzoegerung=", msg.payload.decode("utf-8")]
            subprocess.Popen(sendcommand)
            client.publish("openWB/config/get/pv/stopDelay", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/pv/stopDelay", "", qos=0, retain=True)
    if (msg.topic == "openWB/config/set/pv/startDelay"):
        if (int(msg.payload) >= 0 and int(msg.payload) <= 100000):
            sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "einschaltverzoegerung=", msg.payload.decode("utf-8")]
            subprocess.Popen(sendcommand)
            client.publish("openWB/config/get/pv/startDelay", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/pv/startDelay", "", qos=0, retain=True)
    if (msg.topic == "openWB/config/set/pv/minCurrentMinPv"):
        if (int(msg.payload) >= 6 and int(msg.payload) <= 16):
            sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "minimalampv=", msg.payload.decode("utf-8")]
            subprocess.Popen(sendcommand)
            client.publish("openWB/config/get/pv/minCurrentMinPv", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/pv/minCurrentMinPv", "", qos=0, retain=True)
    if (msg.topic == "openWB/config/set/pv/lp/1/maxSoc"):
        if (int(msg.payload) >= 0 and int(msg.payload) <= 100):
            sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "stopchargepvpercentagelp1=", msg.payload.decode("utf-8")]
            subprocess.Popen(sendcommand)
            client.publish("openWB/config/get/pv/lp/1/maxSoc", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/pv/lp/1/maxSoc", "", qos=0, retain=True)
    if (msg.topic == "openWB/config/set/pv/lp/2/maxSoc"):
        if (int(msg.payload) >= 0 and int(msg.payload) <= 100):
            sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "stopchargepvpercentagelp2=", msg.payload.decode("utf-8")]
            subprocess.Popen(sendcommand)
            client.publish("openWB/config/get/pv/lp/2/maxSoc", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/pv/lp/2/maxSoc", "", qos=0, retain=True)
    if (msg.topic == "openWB/config/set/pv/lp/1/socLimitation"):
        if (int(msg.payload) >= 0 and int(msg.payload) <= 1):
            sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "stopchargepvatpercentlp1=", msg.payload.decode("utf-8")]
            subprocess.Popen(sendcommand)
            client.publish("openWB/config/get/pv/lp/1/socLimitation", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/pv/lp/1/socLimitation", "", qos=0, retain=True)
    if (msg.topic == "openWB/config/set/pv/lp/2/socLimitation"):
        if (int(msg.payload) >= 0 and int(msg.payload) <= 1):
            sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "stopchargepvatpercentlp2=", msg.payload.decode("utf-8")]
            subprocess.Popen(sendcommand)
            client.publish("openWB/config/get/pv/lp/2/socLimitation", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/pv/lp/2/socLimitation", "", qos=0, retain=True)

    if (msg.topic == "openWB/config/set/pv/lp/1/minCurrent"):
        if (int(msg.payload) >= 6 and int(msg.payload) <= 16):
            sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "minimalapv=", msg.payload.decode("utf-8")]
            subprocess.Popen(sendcommand)
            client.publish("openWB/config/get/pv/lp/1/minCurrent", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/pv/lp/1/minCurrent", "", qos=0, retain=True)
    if (msg.topic == "openWB/config/set/pv/lp/2/minCurrent"):
        if (int(msg.payload) >= 6 and int(msg.payload) <= 16):
            sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "minimalalp2mpv=", msg.payload.decode("utf-8")]
            subprocess.Popen(sendcommand)
            client.publish("openWB/config/get/pv/lp/2/minCurrent", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/pv/lp/2/minCurrent", "", qos=0, retain=True)
    if (msg.topic == "openWB/config/set/global/minEVSECurrentAllowed"):
        if (int(msg.payload) >= 6 and int(msg.payload) <= 32):
            sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "minimalstromstaerke=", msg.payload.decode("utf-8")]
            subprocess.Popen(sendcommand)
            client.publish("openWB/config/get/global/minEVSECurrentAllowed", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/global/minEVSECurrentAllowed", "", qos=0, retain=True)
    if (msg.topic == "openWB/config/set/global/maxEVSECurrentAllowed"):
        if (int(msg.payload) >= 6 and int(msg.payload) <= 32):
            sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "maximalstromstaerke=", msg.payload.decode("utf-8")]
            subprocess.Popen(sendcommand)
            client.publish("openWB/config/get/global/maxEVSECurrentAllowed", msg.payload.decode("utf-8"), qos=0, retain=True)
    if (msg.topic == "openWB/config/set/pv/lp/1/minSocAlwaysToChargeTo"):
        if (int(msg.payload) >= 0 and int(msg.payload) <= 80):
            sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "minnurpvsoclp1=", msg.payload.decode("utf-8")]
            subprocess.Popen(sendcommand)
            client.publish("openWB/config/get/pv/lp/1/minSocAlwaysToChargeTo", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/pv/lp/1/minSocAlwaysToChargeTo", "", qos=0, retain=True)
    if (msg.topic == "openWB/config/set/pv/lp/1/maxSocToChargeTo"):
        if (int(msg.payload) >= 0 and int(msg.payload) <= 101):
            sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "maxnurpvsoclp1=", msg.payload.decode("utf-8")]
            subprocess.Popen(sendcommand)
            client.publish("openWB/config/get/pv/lp/1/maxSocToChargeTo", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/pv/lp/1/maxSocToChargeTo", "", qos=0, retain=True)
    if (msg.topic == "openWB/config/set/pv/lp/1/minSocAlwaysToChargeToCurrent"):
        if (int(msg.payload) >= 6 and int(msg.payload) <= 32):
            sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "minnurpvsocll=", msg.payload.decode("utf-8")]
            subprocess.Popen(sendcommand)
            client.publish("openWB/config/get/pv/lp/1/minSocAlwaysToChargeToCurrent", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/pv/lp/1/minSocAlwaysToChargeToCurrent", "", qos=0, retain=True)
    if (msg.topic == "openWB/config/set/pv/chargeSubmode"):
        if (int(msg.payload) >= 0 and int(msg.payload) <= 2):
            sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "pvbezugeinspeisung=", msg.payload.decode("utf-8")]
            subprocess.Popen(sendcommand)
            client.publish("openWB/config/get/pv/chargeSubmode", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/pv/chargeSubmode", "", qos=0, retain=True)
    if (msg.topic == "openWB/config/set/pv/regulationPoint"):
        if (int(msg.payload) >= -300000 and int(msg.payload) <= 300000):
            sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "offsetpv=", msg.payload.decode("utf-8")]
            subprocess.Popen(sendcommand)
            client.publish("openWB/config/get/pv/regulationPoint", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/pv/regulationPoint", "", qos=0, retain=True)
    if (msg.topic == "openWB/config/set/pv/boolShowPriorityIconInTheme"):
        if (int(msg.payload) >= 0 and int(msg.payload) <= 1):
            sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "speicherpvui=", msg.payload.decode("utf-8")]
            subprocess.Popen(sendcommand)
            client.publish("openWB/config/get/pv/boolShowPriorityIconInTheme", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/pv/boolShowPriorityIconInTheme", "", qos=0, retain=True)
    if (msg.topic == "openWB/config/set/pv/minBatteryChargePowerAtEvPriority"):
        if (int(msg.payload) >= 0 and int(msg.payload) <= 90000):
            sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "speichermaxwatt=", msg.payload.decode("utf-8")]
            subprocess.Popen(sendcommand)
            client.publish("openWB/config/get/pv/minBatteryChargePowerAtEvPriority", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/pv/minBatteryChargePowerAtEvPriority", "", qos=0, retain=True)
    if (msg.topic == "openWB/config/set/pv/minBatteryDischargeSocAtBattPriority"):
        if (int(msg.payload) >= 0 and int(msg.payload) <= 101):
            sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "speichersocnurpv=", msg.payload.decode("utf-8")]
            subprocess.Popen(sendcommand)
            client.publish("openWB/config/get/pv/minBatteryDischargeSocAtBattPriority", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/pv/minBatteryDischargeSocAtBattPriority", "", qos=0, retain=True)
    if (msg.topic == "openWB/config/set/pv/batteryDischargePowerAtBattPriority"):
        if (int(msg.payload) >= 0 and int(msg.payload) <= 90000):
            sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "speicherwattnurpv=", msg.payload.decode("utf-8")]
            subprocess.Popen(sendcommand)
            client.publish("openWB/config/get/pv/batteryDischargePowerAtBattPriority", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/pv/batteryDischargePowerAtBattPriority", "", qos=0, retain=True)
    if (msg.topic == "openWB/config/set/pv/socStartChargeAtMinPv"):
        if (int(msg.payload) >= 0 and int(msg.payload) <= 101):
            sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "speichersocminpv=", msg.payload.decode("utf-8")]
            subprocess.Popen(sendcommand)
            client.publish("openWB/config/get/pv/socStartChargeAtMinPv", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/pv/socStartChargeAtMinPv", "", qos=0, retain=True)
    if (msg.topic == "openWB/config/set/pv/socStopChargeAtMinPv"):
        if (int(msg.payload) >= 0 and int(msg.payload) <= 101):
            sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "speichersochystminpv=", msg.payload.decode("utf-8")]
            subprocess.Popen(sendcommand)
            client.publish("openWB/config/get/pv/socStopChargeAtMinPv", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/pv/socStopChargeAtMinPv", "", qos=0, retain=True)
    if (msg.topic == "openWB/config/set/pv/boolAdaptiveCharging"):
        if (int(msg.payload) >= 0 and int(msg.payload) <= 1):
            sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "adaptpv=", msg.payload.decode("utf-8")]
            subprocess.Popen(sendcommand)
            client.publish("openWB/config/get/pv/boolAdaptiveCharging", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/pv/boolAdaptiveCharging", "", qos=0, retain=True)
    if (msg.topic == "openWB/config/set/pv/adaptiveChargingFactor"):
        if (int(msg.payload) >= 0 and int(msg.payload) <= 100):
            sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "adaptfaktor=", msg.payload.decode("utf-8")]
            subprocess.Popen(sendcommand)
            client.publish("openWB/config/get/pv/adaptiveChargingFactor", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/pv/adaptiveChargingFactor", "", qos=0, retain=True)
    if (msg.topic == "openWB/config/set/pv/nurpv70dynact"):
        if (int(msg.payload) >= 0 and int(msg.payload) <= 1):
            sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "nurpv70dynact=", msg.payload.decode("utf-8")]
            subprocess.Popen(sendcommand)
            client.publish("openWB/config/get/pv/nurpv70dynact", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/pv/nurpv70dynact", "", qos=0, retain=True)
    if (msg.topic == "openWB/config/set/pv/nurpv70dynw"):
        if (int(msg.payload) >= 2000 and int(msg.payload) <= 50000):
            sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "nurpv70dynw=", msg.payload.decode("utf-8")]
            subprocess.Popen(sendcommand)
            client.publish("openWB/config/get/pv/nurpv70dynw", msg.payload.decode("utf-8"), qos=0, retain=True)
            client.publish("openWB/config/set/pv/nurpv70dynw", "", qos=0, retain=True)




    if (msg.topic == "openWB/set/system/topicSender"):
        if len(msg.payload) >= 3 and len(msg.payload) <=100:

            client.publish("openWB/set/system/topicSender", "", qos=0, retain=True)
    if (msg.topic == "openWB/set/system/GetRemoteSupport"):
        if len(msg.payload) >= 5 and len(msg.payload) <=30:
            token=msg.payload.decode("utf-8")
            getsupport = ["/var/www/html/openWB/runs/startremotesupport.sh", token]
            subprocess.Popen(getsupport)
            client.publish("openWB/set/system/GetRemoteSupport", "", qos=0, retain=True)
    if (msg.topic == "openWB/set/hook/HookControl"):
        if (int(msg.payload) >= 0 and int(msg.payload) <=30):
            hookmsg=msg.payload.decode("utf-8")
            hooknmb=hookmsg[1:2]
            hookact=hookmsg[0:1]
            sendhook = ["/var/www/html/openWB/runs/hookcontrol.sh", hookmsg]
            subprocess.Popen(sendhook)
            client.publish("openWB/set/hook/HookControl", "", qos=0, retain=True)
            client.publish("openWB/hook/"+hooknmb+"/BoolHookStatus", hookact, qos=0, retain=True)




    if (msg.topic == "openWB/config/set/slave/MinimumAdjustmentInterval"):
        if (int(msg.payload) >= 10 and int(msg.payload) <= 300):
            sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "slaveModeMinimumAdjustmentInterval=", msg.payload.decode("utf-8")]
            subprocess.Popen(sendcommand)
            client.publish("openWB/config/get/slave/MinimumAdjustmentInterval", msg.payload.decode("utf-8"), qos=0, retain=True)
    if (msg.topic == "openWB/config/set/slave/SlowRamping"):
        if (int(msg.payload) >= 0 and int(msg.payload) <= 1):
            sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "slaveModeSlowRamping=", msg.payload.decode("utf-8")]
            subprocess.Popen(sendcommand)
            client.publish("openWB/config/get/slave/SlowRamping", msg.payload.decode("utf-8"), qos=0, retain=True)
    if (msg.topic == "openWB/config/set/slave/UseLastChargingPhase"):
        if (int(msg.payload) >= 0 and int(msg.payload) <= 1):
            sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "slaveModeUseLastChargingPhase=", msg.payload.decode("utf-8")]
            subprocess.Popen(sendcommand)
            client.publish("openWB/config/get/slave/UseLastChargingPhase", msg.payload.decode("utf-8"), qos=0, retain=True)
    if (msg.topic == "openWB/set/configure/AllowedTotalCurrentPerPhase"):
        if (float(msg.payload) >= 0 and float(msg.payload) <=200):
            f = open('/var/www/html/openWB/ramdisk/AllowedTotalCurrentPerPhase', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
    if (msg.topic == "openWB/set/configure/AllowedPeakPower"):
        if (float(msg.payload) >= 0 and float(msg.payload) <=300000):
            f = open('/var/www/html/openWB/ramdisk/AllowedPeakPower', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
    if (msg.topic == "openWB/set/configure/FixedChargeCurrentCp1"):
        if (int(msg.payload) >= -1 and int(msg.payload) <=32):
            f = open('/var/www/html/openWB/ramdisk/FixedChargeCurrentCp1', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
    if (msg.topic == "openWB/set/configure/FixedChargeCurrentCp2"):
        if (int(msg.payload) >= -1 and int(msg.payload) <=32):
            f = open('/var/www/html/openWB/ramdisk/FixedChargeCurrentCp2', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
    if (msg.topic == "openWB/set/configure/SlaveModeAllowedLoadImbalance"):
        if (float(msg.payload) >= 0 and float(msg.payload) <=200):
            f = open('/var/www/html/openWB/ramdisk/SlaveModeAllowedLoadImbalance', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
    if (msg.topic == "openWB/set/configure/AllowedRfidsForLp1"):
        f = open('/var/www/html/openWB/ramdisk/AllowedRfidsForLp1', 'w')
        f.write(msg.payload.decode("utf-8"))
        f.close()
    if (msg.topic == "openWB/set/configure/AllowedRfidsForLp2"):
        f = open('/var/www/html/openWB/ramdisk/AllowedRfidsForLp2', 'w')
        f.write(msg.payload.decode("utf-8"))
        f.close()
    if (msg.topic == "openWB/set/configure/LastControllerPublish"):
        f = open('/var/www/html/openWB/ramdisk/LastControllerPublish', 'w')
        f.write(msg.payload.decode("utf-8"))
        f.close()
    if (msg.topic == "openWB/set/configure/TotalPower"):
        if (float(msg.payload) >= 0 and float(msg.payload) <=300000):
            f = open('/var/www/html/openWB/ramdisk/TotalPower', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
    if (msg.topic == "openWB/set/configure/TotalCurrentConsumptionOnL1"):
        if (float(msg.payload) >= 0 and float(msg.payload) <=200):
            f = open('/var/www/html/openWB/ramdisk/TotalCurrentConsumptionOnL1', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
    if (msg.topic == "openWB/set/configure/TotalCurrentConsumptionOnL2"):
        if (float(msg.payload) >= 0 and float(msg.payload) <=200):
            f = open('/var/www/html/openWB/ramdisk/TotalCurrentConsumptionOnL2', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
    if (msg.topic == "openWB/set/configure/TotalCurrentConsumptionOnL3"):
        if (float(msg.payload) >= 0 and float(msg.payload) <=200):
            f = open('/var/www/html/openWB/ramdisk/TotalCurrentConsumptionOnL3', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
    if (msg.topic == "openWB/set/configure/ChargingVehiclesOnL1"):
        if (int(msg.payload) >= 0 and int(msg.payload) <=200):
            f = open('/var/www/html/openWB/ramdisk/ChargingVehiclesOnL1', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
    if (msg.topic == "openWB/set/configure/ChargingVehiclesOnL2"):
        if (int(msg.payload) >= 0 and int(msg.payload) <=200):
            f = open('/var/www/html/openWB/ramdisk/ChargingVehiclesOnL2', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
    if (msg.topic == "openWB/set/configure/ChargingVehiclesOnL3"):
        if (int(msg.payload) >= 0 and int(msg.payload) <=200):
            f = open('/var/www/html/openWB/ramdisk/ChargingVehiclesOnL3', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()




    if (msg.topic == "openWB/config/set/pv/priorityModeEVBattery"):
        if (int(msg.payload) >= 0 and int(msg.payload) <=1):
            einbeziehen=msg.payload.decode("utf-8")
            sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "speicherpveinbeziehen=", einbeziehen]
            subprocess.Popen(sendcommand)
            client.publish("openWB/config/get/pv/priorityModeEVBattery", einbeziehen, qos=0, retain=True)
            client.publish("openWB/config/set/pv/priorityModeEVBattery", "", qos=0, retain=True)
    if (msg.topic == "openWB/set/graph/LiveGraphDuration"):
        if (int(msg.payload) >= 20 and int(msg.payload) <=120):
            sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "livegraph=", msg.payload.decode("utf-8")]
            subprocess.Popen(sendcommand)
            client.publish("openWB/set/graph/LiveGraphDuration", "", qos=0, retain=True)
    if (msg.topic == "openWB/set/system/SimulateRFID"):
        if len(str(msg.payload)) >= 1 and bool(re.match(namenumballowed, msg.payload.decode("utf-8"))):
            f = open('/var/www/html/openWB/ramdisk/readtag', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
            client.publish("openWB/set/system/SimulateRFID", "", qos=0, retain=True)
    if (msg.topic == "openWB/set/system/PerformUpdate"):
        if (int(msg.payload) == 1):
            client.publish("openWB/set/system/PerformUpdate", "0", qos=0, retain=True)
            subprocess.Popen("/var/www/html/openWB/runs/update.sh")
    if (msg.topic == "openWB/set/system/SendDebug"):
        if (int(msg.payload) == 1):
            client.publish("openWB/set/system/SendDebug", "0", qos=0, retain=True)
            subprocess.Popen("/var/www/html/openWB/runs/senddebuginit.sh")
    if (msg.topic == "openWB/config/set/releaseTrain"):
        if ( msg.payload.decode("utf-8") == "stable17" or msg.payload.decode("utf-8") == "master" or msg.payload.decode("utf-8") == "beta" or msg.payload.decode("utf-8").startswith("yc/")):
            sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "releasetrain=", msg.payload.decode("utf-8")]
            subprocess.Popen(sendcommand)
            client.publish("openWB/config/set/releaseTrain", "", qos=0, retain=True)
    if (msg.topic == "openWB/set/graph/RequestLiveGraph"):
        if (int(msg.payload) == 1):
            subprocess.Popen("/var/www/html/openWB/runs/sendlivegraphdata.sh")
        else:
            client.publish("openWB/system/LiveGraphData", "empty", qos=0, retain=True)
    if (msg.topic == "openWB/set/graph/RequestLLiveGraph"):
        if (int(msg.payload) == 1):
            subprocess.Popen("/var/www/html/openWB/runs/sendllivegraphdata.sh")
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
    if (msg.topic == "openWB/set/system/debug/RequestDebugInfo"):
        if (int(msg.payload) == 1):
            sendcommand = ["/var/www/html/openWB/runs/sendmqttdebug.sh"]
            subprocess.Popen(sendcommand)
    if (msg.topic == "openWB/set/graph/RequestMonthLadelog"):
        if (int(msg.payload) >= 1 and int(msg.payload) <= 205012):
            sendcommand = ["/var/www/html/openWB/runs/sendladelog.sh", msg.payload]
            subprocess.Popen(sendcommand)
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
    if (msg.topic == "openWB/set/pv/NurPV70Status"):
        if (int(msg.payload) >= 0 and int(msg.payload) <= 1):
            client.publish("openWB/pv/bool70PVDynStatus", msg.payload.decode("utf-8"), qos=0, retain=True)
            f = open('/var/www/html/openWB/ramdisk/nurpv70dynstatus', 'w')
            f.write(msg.payload.decode("utf-8"))
            f.close()
            client.publish("openWB/set/pv/NurPV70Status", "", qos=0, retain=True)
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
    if (msg.topic == "openWB/config/set/sofort/lp/1/chargeLimitation"):
        if (int(msg.payload) >= 0 and int(msg.payload) <=2):
            sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "msmoduslp1=", msg.payload.decode("utf-8")]
            subprocess.Popen(sendcommand)
            if (int(msg.payload) == 1):
                client.publish("openWB/lp/1/boolDirectModeChargekWh", msg.payload.decode("utf-8"), qos=0, retain=True)
            else:
                client.publish("openWB/lp/1/boolDirectModeChargekWh", "0", qos=0, retain=True)
            if (int(msg.payload) == 2):
                client.publish("openWB/lp/1/boolDirectChargeModeSoc", "1", qos=0, retain=True)
            else:
                client.publish("openWB/lp/1/boolDirectChargeModeSoc", "0", qos=0, retain=True)
            client.publish("openWB/config/set/sofort/lp/1/chargeLimitation", " ", qos=0, retain=True)
            client.publish("openWB/config/get/sofort/lp/1/chargeLimitation", msg.payload.decode("utf-8"), qos=0, retain=True)
    if (msg.topic == "openWB/config/set/sofort/lp/2/chargeLimitation"):
        if (int(msg.payload) >= 0 and int(msg.payload) <=2):
            sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "msmoduslp2=", msg.payload.decode("utf-8")]
            subprocess.Popen(sendcommand)
            if (int(msg.payload) == 1):
                client.publish("openWB/lp/2/boolDirectModeChargekWh", msg.payload.decode("utf-8"), qos=0, retain=True)
            else:
                client.publish("openWB/lp/2/boolDirectModeChargekWh", "0", qos=0, retain=True)
            if (int(msg.payload) == 2):
                client.publish("openWB/lp/2/boolDirectChargeModeSoc", "1", qos=0, retain=True)
            else:
                client.publish("openWB/lp/2/boolDirectChargeModeSoc", "0", qos=0, retain=True)
            client.publish("openWB/config/set/sofort/lp/2/chargeLimitation", " ", qos=0, retain=True)
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

    if (len(msg.payload) >= 1):
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
