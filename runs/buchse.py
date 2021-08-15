#!/usr/bin/python
#import argparse
import paho.mqtt.client as mqtt
import sys
import os
import time
import struct
import RPi.GPIO as GPIO
from pymodbus.client.sync import ModbusSerialClient

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(37, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(29, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
# GPIOs for socket
GPIO.setup(23, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)

DeviceValues = { }
Values = { }

# values LP1
DeviceValues.update({'lp1voltage1' : str(5)})
DeviceValues.update({'lp1voltage2' : str(5)})
DeviceValues.update({'lp1voltage3' : str(5)})
DeviceValues.update({'lp1lla1' : str(5)})
DeviceValues.update({'lp1lla2' : str(5)})
DeviceValues.update({'lp1lla3' : str(5)})
DeviceValues.update({'lp1llkwh' : str(5)})
DeviceValues.update({'lp1watt' : str(5)})
DeviceValues.update({'lp1chargestat' : str(5)})
DeviceValues.update({'lp1plugstat' : str(5)})
DeviceValues.update({'lp1readerror' : str(0)})
Values.update({'lp1plugstat' : str(5)})
Values.update({'lp1chargestat' : str(5)})
Values.update({'lp1evsell' : str(1)})

# check for "openWB Buchse"
try:
    with open('/home/pi/ppbuchse', 'r') as value:
        pp = int(value.read())
except:
    pp = 32
# here we always have a socket
buchseconfigured = 1

os.chdir('/var/www/html/openWB')

# guess USB/modbus device name
try:
    f = open('/dev/ttyUSB0')
    seradd = "/dev/ttyUSB0"
    f.close()
except:
    seradd = "/dev/serial0"

loglevel = 1
MaxEvseError = 5
sdmid = 105
actorstat = 0
evsefailure = 0
llmeterconfiglp1 = 0

# connect with USB/modbus device
client = ModbusSerialClient(method = "rtu", port=seradd, baudrate=9600, stopbits=1, bytesize=8, timeout=1)

# handling of all logging statements
def logDebug(level, msg): 
    if (int(level) >= int(loglevel)): 
        file = open('/var/www/html/openWB/ramdisk/buchse.log', 'a') 
        if (int(level) == 0): 
            file.write(time.ctime() + ': ' + str(msg)+ '\n')
        if (int(level) == 1): 
            file.write(time.ctime() + ': ' + str(msg)+ '\n')
        if (int(level) == 2): 
            file.write(time.ctime() + ': ' + str('\x1b[6;30;42m' + msg + '\x1b[0m')+ '\n')
        file.close()

# read all meter values and publish to mqtt broker
def getmeter():
    global evsefailure
    global client
    global llmeterconfiglp1
    if ( llmeterconfiglp1 == 0 ):
        logDebug("2", "Erkenne verbauten Zaehler.")
        #check sdm
        try:
            resp = client.read_input_registers(0x00,2, unit=105)
            voltage = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
            if int(voltage) > 20:
                llmeterconfiglp1=105
                sdmid=105
                logDebug("2", "SDM Zaehler erkannt")
        except:
            pass
        #check b23
        try:
            resp = client.read_holding_registers(0x5B00,2, unit=201)
            voltage = resp.registers[1]
            if int(voltage) > 20:
                llmeterconfiglp1=201
                sdmid=201
                logDebug("2", "B23 Zaehler erkannt")
        except:
            pass
    else:
        sdmid=llmeterconfiglp1
    try:
        if sdmid < 200:
            resp = client.read_input_registers(0x0C,2, unit=sdmid)
            lp1llw1 = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
            lp1llw1 = int(lp1llw1)
            resp = client.read_input_registers(0x0E,2, unit=sdmid)
            lp1llw2 = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
            lp1llw2 = int(lp1llw2)
            resp = client.read_input_registers(0x10,2, unit=sdmid)
            lp1llw3 = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
            lp1llw3 = int(lp1llw3)
            lp1llg= lp1llw1 + lp1llw2 + lp1llw3
            if lp1llg < 10:
                lp1llg = 0
            f = open('/var/www/html/openWB/ramdisk/llaktuell', 'w')
            f.write(str(lp1llg))
            f.close()
            resp = client.read_input_registers(0x00,2, unit=sdmid)
            voltage = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
            lp1voltage1 = float("%.1f" % voltage)
            f = open('/var/www/html/openWB/ramdisk/llv1', 'w')
            f.write(str(lp1voltage1))
            f.close()
            resp = client.read_input_registers(0x06,2, unit=sdmid)
            lp1lla1 = float(struct.unpack('>f',struct.pack('>HH',*resp.registers))[0])
            lp1lla1 = float("%.1f" % lp1lla1)
            f = open('/var/www/html/openWB/ramdisk/lla1', 'w')
            f.write(str(lp1lla1))
            f.close()
            resp = client.read_input_registers(0x08,2, unit=sdmid)
            lp1lla2 = float(struct.unpack('>f',struct.pack('>HH',*resp.registers))[0])
            lp1lla2 = float("%.1f" % lp1lla2)
            f = open('/var/www/html/openWB/ramdisk/lla2', 'w')
            f.write(str(lp1lla2))
            f.close()
            resp = client.read_input_registers(0x0A,2, unit=sdmid)
            lp1lla3 = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
            lp1lla3 = float("%.1f" % lp1lla3)
            f = open('/var/www/html/openWB/ramdisk/lla3', 'w')
            f.write(str(lp1lla3))
            f.close()
            resp = client.read_input_registers(0x0156,2, unit=sdmid)
            lp1llkwh = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
            lp1llkwh = float("%.3f" % lp1llkwh)
            f = open('/var/www/html/openWB/ramdisk/llkwh', 'w')
            f.write(str(lp1llkwh))
            f.close()
            resp = client.read_input_registers(0x02,2, unit=sdmid)
            voltage = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
            lp1voltage2 = float("%.1f" % voltage)
            f = open('/var/www/html/openWB/ramdisk/llv2', 'w')
            f.write(str(lp1voltage2))
            f.close() 
            resp = client.read_input_registers(0x04,2, unit=sdmid)
            voltage = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
            lp1voltage3 = float("%.1f" % voltage)
            f = open('/var/www/html/openWB/ramdisk/llv3', 'w')
            f.write(str(lp1voltage3))
            f.close()
            resp = client.read_input_registers(0x46,2, unit=sdmid)
            hz = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
            hz = float("%.2f" % hz)
            f = open('/var/www/html/openWB/ramdisk/llhz', 'w')
            f.write(str(hz))
            f.close()
        else:
            #llkwh
            resp = client.read_holding_registers(0x5000,4, unit=sdmid)
            lp1llkwh = struct.unpack('>Q',struct.pack('>HHHH',*resp.registers))[0]/100
            f = open('/var/www/html/openWB/ramdisk/llkwh', 'w')
            f.write(str(lp1llkwh))
            f.close()
            #Voltage
            resp = client.read_holding_registers(0x5B00,2, unit=sdmid)
            voltage = resp.registers[1]
            lp1voltage1 = float(voltage) / 10
            f = open('/var/www/html/openWB/ramdisk/llv1', 'w')
            f.write(str(lp1voltage1))
            f.close()
            resp = client.read_holding_registers(0x5B02,2, unit=sdmid)
            lp1voltage2 = resp.registers[1]
            lp1voltage2 = float(lp1voltage2) / 10
            f = open('/var/www/html/openWB/ramdisk/llv2', 'w')
            f.write(str(lp1voltage2))
            f.close()
            resp = client.read_holding_registers(0x5B04,2, unit=sdmid)
            voltage = resp.registers[1]
            lp1voltage3 = float(voltage) / 10
            f = open('/var/www/html/openWB/ramdisk/llv3', 'w')
            f.write(str(lp1voltage3))
            f.close()
            #Ampere 
            resp = client.read_holding_registers(0x5B0C,2, unit=sdmid)
            amp = resp.registers[1]
            lp1lla1 = float(amp) / 100
            f = open('/var/www/html/openWB/ramdisk/lla1', 'w')
            f.write(str(lp1lla1))
            f.close()
            resp = client.read_holding_registers(0x5B0E,2, unit=sdmid)
            amp = resp.registers[1]
            lp1lla2 = float(amp) / 100
            f = open('/var/www/html/openWB/ramdisk/lla2', 'w')
            f.write(str(lp1lla2))
            f.close()
            resp = client.read_holding_registers(0x5B10,2, unit=sdmid)
            amp = resp.registers[1]
            lp1lla3 = float(amp) / 100
            f = open('/var/www/html/openWB/ramdisk/lla3', 'w')
            f.write(str(lp1lla3))
            f.close()

            #Gesamt watt 
            resp = client.read_holding_registers(0x5B14,2, unit=sdmid)
            lp1llg = int(struct.unpack('>i',struct.pack('>HH',*resp.registers))[0]/100)
            #if final < 15: 
            #    final = 0 
            f = open('/var/www/html/openWB/ramdisk/llaktuell', 'w')
            f.write(str(lp1llg))
            f.close()
            #LL Hz 
            resp = client.read_holding_registers(0x5B2C,2, unit=sdmid)
            hz = float(resp.registers[0]) / 100
            f = open('/var/www/html/openWB/ramdisk/llhz', 'w')
            f.write(str(hz))
            f.close()

        try:
            time.sleep(0.1)
            rq = client.read_holding_registers(1000,1,unit=1)
            lp1ll = rq.registers[0]
            evsefailure = 0
        except:
            lp1ll = 0
            evsefailure = 1
        try:
            time.sleep(0.1)
            rq = client.read_holding_registers(1002,1,unit=1)
            lp1var = rq.registers[0]
            evsefailure = 0
            DeviceValues.update({'lp1readerror' : str(0)})
        except Exception as e:
            DeviceValues.update({'lp1readerror' : str(int(DeviceValues['lp1readerror'])+1)})
            logDebug("2", "Fehler:" + str(e))
            lp1var = 5
            evsefailure = 1
        if ( lp1var == 5 and int(DeviceValues['lp1readerror']) > MaxEvseError ):
            logDebug("2", "Anhaltender Fehler beim Auslesen der EVSE von lp1! (" + str(DeviceValues['lp1readerror']) + ")" )
            logDebug("2", "Plugstat und Chargestat werden zurückgesetzt.")
            Values.update({'lp1plugstat' : 0})
            Values.update({'lp1chargestat' : 0})
        elif ( lp1var == 1):
            Values.update({'lp1plugstat' : 0})
            Values.update({'lp1chargestat' : 0})
        elif ( lp1var == 2):
            Values.update({'lp1plugstat' : 1})
            Values.update({'lp1chargestat' : 0})
        elif ( lp1var == 3 and lp1ll > 0 ):
            Values.update({'lp1plugstat' : 1})
            Values.update({'lp1chargestat' : 1})
        elif ( lp1var == 3 and lp1ll == 0 ):
            Values.update({'lp1plugstat' : 1})
            Values.update({'lp1chargestat' : 0})
        f = open('/var/www/html/openWB/ramdisk/plugstat', 'w')
        f.write(str(Values["lp1plugstat"]))
        f.close()
        f = open('/var/www/html/openWB/ramdisk/chargestat', 'w')
        f.write(str(Values["lp1chargestat"]))
        f.close()
        Values.update({'lp1evsell' : lp1ll})
        logDebug("0", "EVSE lp1plugstat: " + str(lp1var) + " EVSE lp1LL: " + str(lp1ll))

        # CLI args not used here
        # parser = argparse.ArgumentParser(description='openWB MQTT Publisher')
        # parser.add_argument('--qos', '-q', metavar='qos', type=int, help='The QOS setting', default=0)
        # parser.add_argument('--retain', '-r', dest='retain', action='store_true', help='If true, retain this publish')
        # parser.set_defaults(retain=False)
        # args = parser.parse_args()
        mclient = mqtt.Client("openWB-buchse-bulkpublisher-" + str(os.getpid()))
        mclient.connect("localhost")
        mclient.loop(timeout=2.0)
        for key in DeviceValues:
            if ( "lp1watt" in key):
                if ( DeviceValues[str(key)] != str(lp1llg)):
                    mclient.publish("openWB/lp/1/W", payload=str(lp1llg), qos=0, retain=True)
                    mclient.loop(timeout=2.0)
                    DeviceValues.update({'lp1watt' : str(lp1llg)})
            if ( "lp1voltage1" in key):
                if ( DeviceValues[str(key)] != str(lp1voltage1)):
                    mclient.publish("openWB/lp/1/VPhase1", payload=str(lp1voltage1), qos=0, retain=True)
                    mclient.loop(timeout=2.0)
                    DeviceValues.update({'lp1voltage1' : str(lp1voltage1)})
            if ( "lp1voltage2" in key):
                if ( DeviceValues[str(key)] != str(lp1voltage2)):
                    mclient.publish("openWB/lp/1/VPhase2", payload=str(lp1voltage2), qos=0, retain=True)
                    mclient.loop(timeout=2.0)
                    DeviceValues.update({'lp1voltage2' : str(lp1voltage2)})
            if ( "lp1voltage3" in key):
                if ( DeviceValues[str(key)] != str(lp1voltage3)):
                    mclient.publish("openWB/lp/1/VPhase3", payload=str(lp1voltage3), qos=0, retain=True)
                    mclient.loop(timeout=2.0)
                    DeviceValues.update({'lp1voltage3' : str(lp1voltage3)})
            if ( "lp1lla1" in key):
                if ( DeviceValues[str(key)] != str(lp1lla1)):
                    mclient.publish("openWB/lp/1/APhase1", payload=str(lp1lla1), qos=0, retain=True)
                    mclient.loop(timeout=2.0)
                    DeviceValues.update({'lp1lla1' : str(lp1lla1)})
            if ( "lp1lla2" in key):
                if ( DeviceValues[str(key)] != str(lp1lla2)):
                    mclient.publish("openWB/lp/1/APhase2", payload=str(lp1lla2), qos=0, retain=True)
                    mclient.loop(timeout=2.0)
                    DeviceValues.update({'lp1lla2' : str(lp1lla2)})
            if ( "lp1lla3" in key):
                if ( DeviceValues[str(key)] != str(lp1lla3)):
                    mclient.publish("openWB/lp/1/APhase3", payload=str(lp1lla3), qos=0, retain=True)
                    mclient.loop(timeout=2.0)
                    DeviceValues.update({'lp1lla3' : str(lp1lla3)})
            if ( "lp1llkwh" in key):
                if ( DeviceValues[str(key)] != str(lp1llkwh)):
                    mclient.publish("openWB/lp/1/kWhCounter", payload=str(lp1llkwh), qos=0, retain=True)
                    mclient.loop(timeout=2.0)
                    DeviceValues.update({'lp1llkwh' : str(lp1llkwh)})
            if ( "lp1plugstat" in key):
                if ( DeviceValues[str(key)] != Values["lp1plugstat"]):
                    mclient.publish("openWB/lp/1/boolPlugStat", payload=Values["lp1plugstat"], qos=0, retain=True)
                    mclient.loop(timeout=2.0)
                    DeviceValues.update({'lp1plugstat' : Values["lp1plugstat"]})
            if ( "lp1chargestat" in key):
                if ( DeviceValues[str(key)] != Values["lp1chargestat"]):
                    mclient.publish("openWB/lp/1/boolChargeStat", payload=Values["lp1chargestat"], qos=0, retain=True)
                    mclient.loop(timeout=2.0)
                    DeviceValues.update({'lp1chargestat' : Values["lp1chargestat"]})
        mclient.disconnect()
    except Exception as e:
        logDebug("2", "Get meter Fehler:" + str(e))
        pass

# crontol of socket lock
# GPIO 23: control direction of lock motor
# GPIO 26: power to lock motor
def controlact(action):
    if action == "auf":
        GPIO.output(23, GPIO.LOW)
        GPIO.output(26, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(26, GPIO.LOW)
        logDebug("1", "Aktor auf")
    if action == "zu":
        GPIO.output(23, GPIO.HIGH)
        GPIO.output(26, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(26, GPIO.LOW)
        logDebug("1", "Aktor zu")

# get all values to control our chargepoint
def loadregelvars():
    global actorstat
    global lp1solla
    global u1p3pstat
    global u1p3ptmpstat
    global evsefailure

    try:
        if GPIO.input(19) == False:
            actorstat=1
        if GPIO.input(19) == True:
            actorstat=0
    except:
        actorstat = 0
        pass
    try:
        with open('ramdisk/llsoll', 'r') as value:
            lp1solla = int(value.read())
    except:
        pass
        lp1solla = 0
    logDebug("0", "LL Soll: " + str(lp1solla) + " ActorStatus: " + str(actorstat))
    if ( buchseconfigured == 1 ):
        if ( evsefailure == 0 ):
            if ( Values["lp1plugstat"] == 1):
                if ( actorstat == 0 ):
                    controlact("zu")
            if ( Values["lp1plugstat"] == 0):
                if ( actorstat == 1 ):
                    writelp1evse(0)
                    controlact("auf")
            if ( actorstat == 1 ):
                if ( Values["lp1evsell"] != lp1solla and Values["lp1plugstat"] == 1 ):
                    writelp1evse(lp1solla)
            else:
                if ( Values["lp1evsell"] != 0 ):
                    writelp1evse(0)
    else:
        if ( Values["lp1evsell"] != lp1solla ):
            writelp1evse(lp1solla)
    try:
        with open('ramdisk/u1p3pstat', 'r') as value:
            u1p3ptmpstat = int(value.read())
    except:
        pass
        u1p3ptmpstat = 3
    try:
        u1p3pstat
    except:
        u1p3pstat = 3
    if ( u1p3pstat != u1p3ptmpstat ):
        if ( u1p3ptmpstat == 1 ):
            GPIO.output(22, GPIO.HIGH)
            GPIO.output(29, GPIO.HIGH)
            GPIO.output(11, GPIO.HIGH)
            time.sleep(2)
            GPIO.output(29, GPIO.LOW)
            GPIO.output(11, GPIO.LOW)
            time.sleep(5)
            GPIO.output(22, GPIO.LOW)
            time.sleep(1)
        if ( u1p3ptmpstat == 3 ):
            GPIO.output(22, GPIO.HIGH)
            GPIO.output(37, GPIO.HIGH)
            GPIO.output(13, GPIO.HIGH)
            time.sleep(2)
            GPIO.output(37, GPIO.LOW)
            GPIO.output(13, GPIO.LOW)
            time.sleep(5)
            GPIO.output(22, GPIO.LOW)
            time.sleep(1)
        u1p3pstat = u1p3ptmpstat

def writelp1evse(lla):
    if (lla > pp):
        lla=pp
    client.write_registers(1000, lla, unit=1)
    logDebug("1", "Write to EVSE lp1 " + str(lla))

while True:
    getmeter()
    loadregelvars()
    time.sleep(1)
