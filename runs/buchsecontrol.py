#!/usr/bin/python
import sys
import os 
import time 
import getopt 
import socket 
import struct 
import binascii 
import RPi.GPIO as GPIO
os.chdir('/var/www/html/openWB')
seradd = "/dev/ttyserial0" 
sdmiid=5
Values = { }
actorstat=0
loglevel=0
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
from pymodbus.client.sync import ModbusSerialClient 
client = ModbusSerialClient(method = "rtu", port=seradd, baudrate=9600, 
        stopbits=1, bytesize=8, timeout=1)
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
def getmeter():
    try:
        resp = client.read_input_registers(0x0C,2, unit=sdmid)
        llw1 = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
        llw1 = int(llw1)
        resp = client.read_input_registers(0x0E,2, unit=sdmid)
        llw2 = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
        llw2 = int(llw2)
        resp = client.read_input_registers(0x10,2, unit=sdmid)
        llw3 = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
        llw3 = int(llw3)
        llg= llw1 + llw2 + llw3
        if llg < 10:
            llg = 0
        f = open('/var/www/html/openWB/ramdisk/llaktuell', 'w')
        f.write(str(llg))
        f.close()
        resp = client.read_input_registers(0x00,2, unit=sdmid)
        voltage = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
        voltage = float("%.1f" % voltage)
        f = open('/var/www/html/openWB/ramdisk/llv1', 'w')
        f.write(str(voltage))
        f.close()
        resp = client.read_input_registers(0x06,2, unit=sdmid)
        lla1 = float(struct.unpack('>f',struct.pack('>HH',*resp.registers))[0])
        lla1 = float("%.1f" % lla1)
        f = open('/var/www/html/openWB/ramdisk/lla1', 'w')
        f.write(str(lla1))
        f.close()
        resp = client.read_input_registers(0x08,2, unit=sdmid)
        lla2 = float(struct.unpack('>f',struct.pack('>HH',*resp.registers))[0])
        lla2 = float("%.1f" % lla2)
        f = open('/var/www/html/openWB/ramdisk/lla2', 'w')
        f.write(str(lla2))
        f.close()
        resp = client.read_input_registers(0x0A,2, unit=sdmid)
        lla3 = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
        lla3 = float("%.1f" % lla3)
        f = open('/var/www/html/openWB/ramdisk/lla3', 'w')
        f.write(str(lla3))
        f.close()
        resp = client.read_input_registers(0x0156,2, unit=sdmid)
        llkwh = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
        llkwh = float("%.3f" % llkwh)
        f = open('/var/www/html/openWB/ramdisk/llkwh', 'w')
        f.write(str(llkwh))
        f.close()
        resp = client.read_input_registers(0x02,2, unit=sdmid)
        voltage = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
        voltage = float("%.1f" % voltage)
        f = open('/var/www/html/openWB/ramdisk/llv2', 'w')
        f.write(str(voltage))
        f.close() 
        resp = client.read_input_registers(0x04,2, unit=sdmid)
        voltage = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
        voltage = float("%.1f" % voltage)
        f = open('/var/www/html/openWB/ramdisk/llv3', 'w')
        f.write(str(voltage))
        f.close()
        resp = client.read_input_registers(0x46,2, unit=sdmid)
        hz = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
        hz = float("%.2f" % hz)
        f = open('/var/www/html/openWB/ramdisk/llhz', 'w')
        f.write(str(hz))
        f.close()
    except:
        pass
def controlact(action):
    if action == "auf":
        GPIO.output(11, GPIO.LOW)
        GPIO.output(7, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(7, GPIO.LOW)
        logDebug("1", "Aktor auf")
    if action == "zu":
        GPIO.output(11, GPIO.HIGH)
        GPIO.output(7, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(7, GPIO.LOW)
        logDebug("1", "Aktor zu")

def getplugstat():
    try:
        rq = client.read_holding_registers(1002,1,unit=1) 
        var = rq.registers[0]
    except:
        var = 5
    if ( var == 5 ):
        Values.update({'plugstat' : 0})
        Values.update({'chargestat' : 0})
    elif ( var == 1):
        Values.update({'plugstat' : 0})
        Values.update({'chargestat' : 0})
    elif ( var == 2):
        Values.update({'plugstat' : 1})
        Values.update({'chargestat' : 0})
    elif ( var == 3):
        Values.update({'plugstat' : 1})
        Values.update({'chargestat' : 2})
    try:
        rq = client.read_holding_registers(1000,1,unit=1) 
        ll = rq.registers[0]
    except:
        ll = 0
    Values.update({'evsell' : ll})
    logDebug("0", "EVSE plugstat: " + str(var) + " EVSE LL: " + str(ll))
def loadregelvars():
    global actorstat
    global solla
    try:
        with open('ramdisk/buchsestatus', 'r') as value:
            actorstat = int(value.read())
    except:
        actorstat = 0
        pass
    try:
        with open('ramdisk/llsoll', 'r') as value:
            solla = int(value.read())
    except:
        pass
        solla = 0
    logDebug("0", "LL Soll: " + str(solla) + " ActorStatus: " + str(actorstat))
    
def writeevse(lla):
    client.write_registers(1000, lla, unit=1)
    logDebug("1", "Write to EVSE" + str(lla))
def conditions():
    if ( Values["plugstat"] == 1):
        if ( actorstat == 0 ):
            controlact("zu")
    if ( Values["plugstat"] == 0):
        if ( actorstat == 1 ):
            controlact("auf")
    if ( actorstat == 1 ):
        if ( Values["evsell"] != solla ):
            writeevse(solla)
    else:
        if ( Values["evsell"] != 0 ):
            writeevse(0)

while True:
    getplugstat()
    loadregelvars()
    getmeter()
    conditions()
    time.sleep(2)
