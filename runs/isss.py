#!/usr/bin/python
import paho.mqtt.client as mqtt
import sys
import re
import os
import time
import struct
import RPi.GPIO as GPIO
from pymodbus.client.sync import ModbusSerialClient


# handling of all logging statements
def log_debug(level: int, msg: str) -> None:
    if level >= int(loglevel):
        with open('/var/www/html/openWB/ramdisk/isss.log', 'a') as log_file:
            if int(level) == 2:
                log_file.write(time.ctime() + ': ' + str('\x1b[6;30;42m' + msg + '\x1b[0m') + '\n')
            else:
                log_file.write(time.ctime() + ': ' + str(msg) + '\n')


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(37, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(29, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)

# GPIOs for socket
GPIO.setup(23, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)

DeviceValues = {}
Values = {}

# global values
DeviceValues.update({'rfidtag': str(5)})

# values LP1
DeviceValues.update({'lp1voltage1': str(5)})
DeviceValues.update({'lp1voltage2': str(5)})
DeviceValues.update({'lp1voltage3': str(5)})
DeviceValues.update({'lp1lla1': str(5)})
DeviceValues.update({'lp1lla2': str(5)})
DeviceValues.update({'lp1lla3': str(5)})
DeviceValues.update({'lp1llkwh': str(5)})
DeviceValues.update({'lp1watt': str(5)})
DeviceValues.update({'lp1countphasesinuse': str(5)})
DeviceValues.update({'lp1chargestat': str(5)})
DeviceValues.update({'lp1plugstat': str(5)})
DeviceValues.update({'lp1readerror': str(0)})
Values.update({'lp1plugstat': str(5)})
Values.update({'lp1chargestat': str(5)})
Values.update({'lp1evsell': str(1)})

# values LP2
DeviceValues.update({'lp2voltage1': str(5)})
DeviceValues.update({'lp2voltage2': str(5)})
DeviceValues.update({'lp2voltage3': str(5)})
DeviceValues.update({'lp2lla1': str(5)})
DeviceValues.update({'lp2lla2': str(5)})
DeviceValues.update({'lp2lla3': str(5)})
DeviceValues.update({'lp2llkwh': str(5)})
DeviceValues.update({'lp2watt': str(5)})
DeviceValues.update({'lp2countphasesinuse': str(5)})
DeviceValues.update({'lp2chargestat': str(5)})
DeviceValues.update({'lp2plugstat': str(5)})
DeviceValues.update({'lp2readerror': str(0)})
Values.update({'lp2plugstat': str(5)})
Values.update({'lp2chargestat': str(5)})
Values.update({'lp2evsell': str(1)})

# check for "openWB Buchse"
try:
    with open('/home/pi/ppbuchse', 'r') as value:
        pp = int(value.read())
        buchseconfigured = 1
except FileNotFoundError:
    pp = 32
    buchseconfigured = 0
# initialize LL meter
llmeterconfiglp1 = 0

os.chdir('/var/www/html/openWB')

# guess USB/modbus device name
try:
    with open('/dev/ttyUSB0') as device:
        seradd = "/dev/ttyUSB0"
except FileNotFoundError:
    seradd = "/dev/serial0"

try:
    with open('ramdisk/lpdaemonloglevel', 'r') as value:
        loglevel = int(value.read())
except FileNotFoundError:
    loglevel = 1

lp1evsehres = 0
lp2evsehres = 0
MaxEvseError = 5
sdmid = 105
sdm2id = 106
actorstat = 0
lp1solla = 0
u1p3pstat = None
u1p3plp2stat = None
u1p3ptmpstat = 3
u1p3plp2tmpstat = 3
evsefailure = 0
rfidtag = 0
lp1countphasesinuse = 1
lp2countphasesinuse = 2
heartbeat = 0
metercounter = 0
actcooldown = 0
actcooldowntimestamp = 0

# check for openWB DUO in slave mode
lp2installed = False
try:
    with open('ramdisk/issslp2act', 'r') as value:
        if int(value.read()) == 1:
            lp2installed = True
except (FileNotFoundError, ValueError):
    log_debug(1, "Error reading issslp2act! Guessing cp2 is not configured.")

# connect with USB/modbus device
client = ModbusSerialClient(method="rtu", port=seradd, baudrate=9600, stopbits=1, bytesize=8, timeout=1)


# read all meter values and publish to mqtt broker
def getmeter():
    global metercounter
    global evsefailure
    global client
    global lp2installed
    global llmeterconfiglp1
    global sdmid
    global sdm2id
    global lp1countphasesinuse
    global lp2countphasesinuse
    global lp1evsehres
    global lp2evsehres
    global rfidtag

    if metercounter > 0:
        metercounter = metercounter - 0.5
    if llmeterconfiglp1 == 0:
        log_debug(2, "Erkenne verbauten Zaehler.")
        # check sdm
        try:
            resp = client.read_input_registers(0x00, 2, unit=105)
            voltage = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
            if int(voltage) > 20:
                llmeterconfiglp1 = 105
                sdmid = 105
                log_debug(2, "SDM Zaehler erkannt")
        except Exception:
            pass
        # check b23
        try:
            resp = client.read_holding_registers(0x5B00, 2, unit=201)
            voltage = resp.registers[1]
            if int(voltage) > 20:
                llmeterconfiglp1 = 201
                sdmid = 201
                log_debug(2, "B23 Zaehler erkannt")
        except Exception:
            pass

    else:
        sdmid = llmeterconfiglp1
    try:
        if sdmid < 200:
            time.sleep(0.1)
            resp = client.read_input_registers(0x0C, 2, unit=sdmid)
            lp1llw1 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
            lp1llw1 = int(lp1llw1)
            resp = client.read_input_registers(0x0E, 2, unit=sdmid)
            lp1llw2 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
            lp1llw2 = int(lp1llw2)
            resp = client.read_input_registers(0x10, 2, unit=sdmid)
            lp1llw3 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
            lp1llw3 = int(lp1llw3)
            lp1llg = lp1llw1 + lp1llw2 + lp1llw3
            if lp1llg < 10:
                lp1llg = 0
            with open('/var/www/html/openWB/ramdisk/llaktuell', 'w') as ramdisk_file:
                ramdisk_file.write(str(lp1llg))
            resp = client.read_input_registers(0x00, 2, unit=sdmid)
            voltage = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
            lp1voltage1 = float("%.1f" % voltage)
            with open('/var/www/html/openWB/ramdisk/llv1', 'w') as ramdisk_file:
                ramdisk_file.write(str(lp1voltage1))
            resp = client.read_input_registers(0x06, 2, unit=sdmid)
            lp1lla1 = float(struct.unpack('>f', struct.pack('>HH', *resp.registers))[0])
            lp1lla1 = float("%.1f" % lp1lla1)
            with open('/var/www/html/openWB/ramdisk/lla1', 'w') as ramdisk_file:
                ramdisk_file.write(str(lp1lla1))
            resp = client.read_input_registers(0x08, 2, unit=sdmid)
            lp1lla2 = float(struct.unpack('>f', struct.pack('>HH', *resp.registers))[0])
            lp1lla2 = float("%.1f" % lp1lla2)
            with open('/var/www/html/openWB/ramdisk/lla2', 'w') as ramdisk_file:
                ramdisk_file.write(str(lp1lla2))
            resp = client.read_input_registers(0x0A, 2, unit=sdmid)
            lp1lla3 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
            lp1lla3 = float("%.1f" % lp1lla3)
            with open('/var/www/html/openWB/ramdisk/lla3', 'w') as ramdisk_file:
                ramdisk_file.write(str(lp1lla3))
            resp = client.read_input_registers(0x0156, 2, unit=sdmid)
            lp1llkwh = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
            lp1llkwh = float("%.3f" % lp1llkwh)
            with open('/var/www/html/openWB/ramdisk/llkwh', 'w') as ramdisk_file:
                ramdisk_file.write(str(lp1llkwh))
            resp = client.read_input_registers(0x02, 2, unit=sdmid)
            voltage = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
            lp1voltage2 = float("%.1f" % voltage)
            with open('/var/www/html/openWB/ramdisk/llv2', 'w') as ramdisk_file:
                ramdisk_file.write(str(lp1voltage2))
            resp = client.read_input_registers(0x04, 2, unit=sdmid)
            voltage = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
            lp1voltage3 = float("%.1f" % voltage)
            with open('/var/www/html/openWB/ramdisk/llv3', 'w') as ramdisk_file:
                ramdisk_file.write(str(lp1voltage3))
            resp = client.read_input_registers(0x46, 2, unit=sdmid)
            hz = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
            hz = float("%.2f" % hz)
            with open('/var/www/html/openWB/ramdisk/llhz', 'w') as ramdisk_file:
                ramdisk_file.write(str(hz))
        elif sdmid < 255:
            # llkwh
            resp = client.read_holding_registers(0x5000, 4, unit=sdmid)
            lp1llkwh = struct.unpack('>Q', struct.pack('>HHHH', *resp.registers))[0]/100
            with open('/var/www/html/openWB/ramdisk/llkwh', 'w') as ramdisk_file:
                ramdisk_file.write(str(lp1llkwh))
            # Voltage
            resp = client.read_holding_registers(0x5B00, 2, unit=sdmid)
            voltage = resp.registers[1]
            lp1voltage1 = float(voltage) / 10
            with open('/var/www/html/openWB/ramdisk/llv1', 'w') as ramdisk_file:
                ramdisk_file.write(str(lp1voltage1))
            resp = client.read_holding_registers(0x5B02, 2, unit=sdmid)
            lp1voltage2 = resp.registers[1]
            lp1voltage2 = float(lp1voltage2) / 10
            with open('/var/www/html/openWB/ramdisk/llv2', 'w') as ramdisk_file:
                ramdisk_file.write(str(lp1voltage2))
            resp = client.read_holding_registers(0x5B04, 2, unit=sdmid)
            voltage = resp.registers[1]
            lp1voltage3 = float(voltage) / 10
            with open('/var/www/html/openWB/ramdisk/llv3', 'w') as ramdisk_file:
                ramdisk_file.write(str(lp1voltage3))
            # Ampere
            resp = client.read_holding_registers(0x5B0C, 2, unit=sdmid)
            amp = resp.registers[1]
            lp1lla1 = float(amp) / 100
            with open('/var/www/html/openWB/ramdisk/lla1', 'w') as ramdisk_file:
                ramdisk_file.write(str(lp1lla1))
            resp = client.read_holding_registers(0x5B0E, 2, unit=sdmid)
            amp = resp.registers[1]
            lp1lla2 = float(amp) / 100
            with open('/var/www/html/openWB/ramdisk/lla2', 'w') as ramdisk_file:
                ramdisk_file.write(str(lp1lla2))
            resp = client.read_holding_registers(0x5B10, 2, unit=sdmid)
            amp = resp.registers[1]
            lp1lla3 = float(amp) / 100
            with open('/var/www/html/openWB/ramdisk/lla3', 'w') as ramdisk_file:
                ramdisk_file.write(str(lp1lla3))

            # Gesamt watt
            resp = client.read_holding_registers(0x5B14, 2, unit=sdmid)
            lp1llg = int(struct.unpack('>i', struct.pack('>HH', *resp.registers))[0]/100)
            with open('/var/www/html/openWB/ramdisk/llaktuell', 'w') as ramdisk_file:
                ramdisk_file.write(str(lp1llg))
            # LL Hz
            resp = client.read_holding_registers(0x5B2C, 2, unit=sdmid)
            hz = float(resp.registers[0]) / 100
            with open('/var/www/html/openWB/ramdisk/llhz', 'w') as ramdisk_file:
                ramdisk_file.write(str(hz))
        else:
            # dummy
            lp1voltage1 = 230
            lp1voltage2 = 230
            lp1voltage3 = 230
            lp1lla1 = 0
            lp1lla2 = 0
            lp1lla3 = 0
            lp1llkwh = 10
            hz = 0
            lp1llg = 0

        try:
            if lp1lla1 > 3:
                lp1countphasesinuse = 1
            if lp1lla2 > 3:
                lp1countphasesinuse = 2
            if lp1lla3 > 3:
                lp1countphasesinuse = 3
        except Exception:
            lp1countphasesinuse = 1

        if lp2installed:
            try:
                time.sleep(0.1)
                resp = client.read_input_registers(0x0C, 2, unit=sdm2id)
                lp2llw1 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
                lp2llw1 = int(lp2llw1)
                resp = client.read_input_registers(0x0E, 2, unit=sdm2id)
                lp2llw2 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
                lp2llw2 = int(lp2llw2)
                resp = client.read_input_registers(0x10, 2, unit=sdm2id)
                lp2llw3 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
                lp2llw3 = int(lp2llw3)
                lp2llg = lp2llw1 + lp2llw2 + lp2llw3
                if lp2llg < 10:
                    lp2llg = 0
                with open('/var/www/html/openWB/ramdisk/llaktuells1', 'w') as ramdisk_file:
                    ramdisk_file.write(str(lp2llg))
                resp = client.read_input_registers(0x00, 2, unit=sdm2id)
                voltage = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
                lp2voltage1 = float("%.1f" % voltage)
                with open('/var/www/html/openWB/ramdisk/llvs11', 'w') as ramdisk_file:
                    ramdisk_file.write(str(lp2voltage1))
                resp = client.read_input_registers(0x06, 2, unit=sdm2id)
                lp2lla1 = float(struct.unpack('>f', struct.pack('>HH', *resp.registers))[0])
                lp2lla1 = float("%.1f" % lp2lla1)
                with open('/var/www/html/openWB/ramdisk/llas11', 'w') as ramdisk_file:
                    ramdisk_file.write(str(lp2lla1))
                resp = client.read_input_registers(0x08, 2, unit=sdm2id)
                lp2lla2 = float(struct.unpack('>f', struct.pack('>HH', *resp.registers))[0])
                lp2lla2 = float("%.1f" % lp2lla2)
                with open('/var/www/html/openWB/ramdisk/llas12', 'w') as ramdisk_file:
                    ramdisk_file.write(str(lp2lla2))
                resp = client.read_input_registers(0x0A, 2, unit=sdm2id)
                lp2lla3 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
                lp2lla3 = float("%.1f" % lp2lla3)
                with open('/var/www/html/openWB/ramdisk/llas13', 'w') as ramdisk_file:
                    ramdisk_file.write(str(lp2lla3))
                resp = client.read_input_registers(0x0156, 2, unit=sdm2id)
                lp2llkwh = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
                lp2llkwh = float("%.3f" % lp2llkwh)
                with open('/var/www/html/openWB/ramdisk/llkwhs1', 'w') as ramdisk_file:
                    ramdisk_file.write(str(lp2llkwh))
                resp = client.read_input_registers(0x02, 2, unit=sdm2id)
                voltage = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
                lp2voltage2 = float("%.1f" % voltage)
                with open('/var/www/html/openWB/ramdisk/llvs12', 'w') as ramdisk_file:
                    ramdisk_file.write(str(lp2voltage2))
                resp = client.read_input_registers(0x04, 2, unit=sdm2id)
                voltage = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
                lp2voltage3 = float("%.1f" % voltage)
                with open('/var/www/html/openWB/ramdisk/llvs13', 'w') as ramdisk_file:
                    ramdisk_file.write(str(lp2voltage3))
                try:
                    if lp2lla1 > 3:
                        lp2countphasesinuse = 1
                    if lp2lla2 > 3:
                        lp2countphasesinuse = 2
                    if lp2lla3 > 3:
                        lp2countphasesinuse = 3
                except Exception:
                    lp2countphasesinuse = 1
                try:
                    time.sleep(0.1)
                    rq = client.read_holding_registers(1000, 1, unit=2)
                    lp2ll = rq.registers[0]
                except Exception:
                    lp2ll = 0
                try:
                    time.sleep(0.1)
                    rq = client.read_holding_registers(1002, 1, unit=2)
                    lp2var = rq.registers[0]
                    DeviceValues.update({'lp2readerror': str(0)})
                except Exception as e:
                    DeviceValues.update({'lp2readerror': str(int(DeviceValues['lp2readerror']) + 1)})
                    log_debug(2, "Fehler:" + str(e))
                    lp2var = 5
                if (lp2var == 5 and int(DeviceValues['lp2readerror']) > MaxEvseError):
                    log_debug(2, "Anhaltender Fehler beim Auslesen der EVSE von lp2! ("
                              + str(DeviceValues['lp2readerror']) + ")")
                    log_debug(2, "Plugstat und Chargestat werden zurückgesetzt.")
                    Values.update({'lp2plugstat': 0})
                    Values.update({'lp2chargestat': 0})
                elif lp2var == 1:
                    Values.update({'lp2plugstat': 0})
                    Values.update({'lp2chargestat': 0})
                elif lp2var == 2:
                    Values.update({'lp2plugstat': 1})
                    Values.update({'lp2chargestat': 0})
                elif (lp2var == 3 and lp2ll > 0):
                    Values.update({'lp2plugstat': 1})
                    Values.update({'lp2chargestat': 1})
                elif (lp2var == 3 and lp2ll == 0):
                    Values.update({'lp2plugstat': 1})
                    Values.update({'lp2chargestat': 0})
                with open('/var/www/html/openWB/ramdisk/plugstats1', 'w') as ramdisk_file:
                    ramdisk_file.write(str(Values["lp2plugstat"]))
                with open('/var/www/html/openWB/ramdisk/chargestats1', 'w') as ramdisk_file:
                    ramdisk_file.write(str(Values["lp2chargestat"]))
                Values.update({'lp2evsell': lp2ll})
                log_debug(0, "EVSE lp2plugstat: " + str(lp2var) + " EVSE lp2LL: " + str(lp2ll))
            except Exception:
                pass

        try:
            time.sleep(0.1)
            rq = client.read_holding_registers(1000, 1, unit=1)
            lp1ll = rq.registers[0]
            evsefailure = 0
        except Exception:
            lp1ll = 0
            evsefailure = 1
        try:
            time.sleep(0.1)
            rq = client.read_holding_registers(1002, 1, unit=1)
            lp1var = rq.registers[0]
            evsefailure = 0
            DeviceValues.update({'lp1readerror': str(0)})
        except Exception as e:
            DeviceValues.update({'lp1readerror': str(int(DeviceValues['lp1readerror'])+1)})
            log_debug(2, "Fehler:" + str(e))
            lp1var = 5
            evsefailure = 1
        if (lp1var == 5 and int(DeviceValues['lp1readerror']) > MaxEvseError):
            log_debug(2, "Anhaltender Fehler beim Auslesen der EVSE von lp1! ("
                      + str(DeviceValues['lp1readerror']) + ")")
            log_debug(2, "Plugstat und Chargestat werden zurückgesetzt.")
            Values.update({'lp1plugstat': 0})
            Values.update({'lp1chargestat': 0})
        elif lp1var == 1:
            Values.update({'lp1plugstat': 0})
            Values.update({'lp1chargestat': 0})
        elif lp1var == 2:
            Values.update({'lp1plugstat': 1})
            Values.update({'lp1chargestat': 0})
        elif (lp1var == 3 and lp1ll > 0):
            Values.update({'lp1plugstat': 1})
            Values.update({'lp1chargestat': 1})
        elif (lp1var == 3 and lp1ll == 0):
            Values.update({'lp1plugstat': 1})
            Values.update({'lp1chargestat': 0})
        with open('/var/www/html/openWB/ramdisk/plugstat', 'w') as ramdisk_file:
            ramdisk_file.write(str(Values["lp1plugstat"]))
        with open('/var/www/html/openWB/ramdisk/chargestat', 'w') as ramdisk_file:
            ramdisk_file.write(str(Values["lp1chargestat"]))
        Values.update({'lp1evsell': lp1ll})
        log_debug(0, "EVSE lp1plugstat: " + str(lp1var) + " EVSE lp1LL: " + str(lp1ll))
        try:
            with open('ramdisk/readtag', 'r') as ramdisk_file:
                rfidtag = str(ramdisk_file.read())
        except Exception:
            pass
        # check for parent openWB
        try:
            with open('ramdisk/parentWB', 'r') as ramdisk_file:
                parentWB = str(ramdisk_file.read().replace('\\n', '').replace('\"', ''))
            with open('ramdisk/parentCPlp1', 'r') as ramdisk_file:
                parentCPlp1 = str(int(re.sub(r'\D', '', ramdisk_file.read())))
            if lp2installed:
                with open('ramdisk/parentCPlp2', 'r') as ramdisk_file:
                    parentCPlp2 = str(int(re.sub(r'\D', '', ramdisk_file.read())))
        except Exception:
            parentWB = str("0")
            parentCPlp1 = str("0")
            parentCPlp2 = str("0")

        if parentWB != "0":
            remoteclient = mqtt.Client("openWB-isss-bulkpublisher-" + str(os.getpid()))
            remoteclient.connect(str(parentWB))
            remoteclient.loop(timeout=2.0)
        mclient = mqtt.Client("openWB-isss-bulkpublisher-" + str(os.getpid()))
        mclient.connect("localhost")
        mclient.loop(timeout=2.0)
        for key in DeviceValues:
            if "lp1watt" in key:
                if DeviceValues[str(key)] != str(lp1llg):
                    mclient.publish("openWB/lp/1/W", payload=str(lp1llg), qos=0, retain=True)
                    mclient.loop(timeout=2.0)
                    DeviceValues.update({'lp1watt': str(lp1llg)})
                if parentWB != "0":
                    remoteclient.publish("openWB/lp/"+parentCPlp1+"/W", payload=str(lp1llg), qos=0, retain=True)
                    remoteclient.publish("openWB/set/chargepoint/"+parentCPlp1+"/get/power", payload=str(lp1llg),
                                         qos=0, retain=True)
                    remoteclient.loop(timeout=2.0)
            if "lp1voltage1" in key:
                if DeviceValues[str(key)] != str(lp1voltage1):
                    mclient.publish("openWB/lp/1/VPhase1", payload=str(lp1voltage1), qos=0, retain=True)
                    mclient.loop(timeout=2.0)
                    DeviceValues.update({'lp1voltage1': str(lp1voltage1)})
                if parentWB != "0":
                    remoteclient.publish("openWB/lp/"+parentCPlp1 + "/Vphase1",
                                         payload=str(lp1voltage1), qos=0, retain=True)
                    remoteclient.publish("openWB/set/chargepoint/" + parentCPlp1+"/get/voltages", payload="["
                                         + str(lp1voltage1) + "," + str(lp1voltage2) + "," + str(lp1voltage3) + "]",
                                         qos=0, retain=True)
                    remoteclient.loop(timeout=2.0)
            if "lp1voltage2" in key:
                if DeviceValues[str(key)] != str(lp1voltage2):
                    mclient.publish("openWB/lp/1/VPhase2", payload=str(lp1voltage2), qos=0, retain=True)
                    mclient.loop(timeout=2.0)
                    DeviceValues.update({'lp1voltage2': str(lp1voltage2)})
            if "lp1voltage3" in key:
                if DeviceValues[str(key)] != str(lp1voltage3):
                    mclient.publish("openWB/lp/1/VPhase3", payload=str(lp1voltage3), qos=0, retain=True)
                    mclient.loop(timeout=2.0)
                    DeviceValues.update({'lp1voltage3': str(lp1voltage3)})
            if "lp1lla1" in key:
                if DeviceValues[str(key)] != str(lp1lla1):
                    mclient.publish("openWB/lp/1/APhase1", payload=str(lp1lla1), qos=0, retain=True)
                    mclient.loop(timeout=2.0)
                    DeviceValues.update({'lp1lla1': str(lp1lla1)})
                if parentWB != "0":
                    remoteclient.publish("openWB/lp/" + parentCPlp1 + "/Aphase1", payload=str(lp1lla1),
                                         qos=0, retain=True)
                    remoteclient.publish("openWB/set/chargepoint/" + parentCPlp1 + "/get/currents",
                                         payload="[" + str(lp1lla1) + "," + str(lp1lla2) + "," + str(lp1lla3) + "]",
                                         qos=0, retain=True)
                    remoteclient.loop(timeout=2.0)

            if "lp1lla2" in key:
                if DeviceValues[str(key)] != str(lp1lla2):
                    mclient.publish("openWB/lp/1/APhase2", payload=str(lp1lla2), qos=0, retain=True)
                    mclient.loop(timeout=2.0)
                    DeviceValues.update({'lp1lla2': str(lp1lla2)})
                if parentWB != "0":
                    remoteclient.publish("openWB/lp/"+parentCPlp1+"/Aphase2", payload=str(lp1lla2), qos=0, retain=True)
                    remoteclient.loop(timeout=2.0)

            if "lp1lla3" in key:
                if DeviceValues[str(key)] != str(lp1lla3):
                    mclient.publish("openWB/lp/1/APhase3", payload=str(lp1lla3), qos=0, retain=True)
                    mclient.loop(timeout=2.0)
                    DeviceValues.update({'lp1lla3': str(lp1lla3)})
                if parentWB != "0":
                    remoteclient.publish("openWB/lp/"+parentCPlp1+"/Aphase3", payload=str(lp1lla3), qos=0, retain=True)
                    remoteclient.loop(timeout=2.0)

            if "lp1countphasesinuse" in key:
                if DeviceValues[str(key)] != str(lp1countphasesinuse):
                    mclient.publish("openWB/lp/1/countPhasesInUse", payload=str(lp1countphasesinuse),
                                    qos=0, retain=True)
                    mclient.loop(timeout=2.0)
                    DeviceValues.update({'lp1countphasesinuse': str(lp1countphasesinuse)})
                if parentWB != "0":
                    remoteclient.publish("openWB/lp/"+parentCPlp1+"/countPhasesInUse", payload=str(lp1countphasesinuse),
                                         qos=0, retain=True)
                    remoteclient.publish("openWB/set/chargepoint/"+parentCPlp1+"/get/phases_in_use",
                                         payload=str(lp1countphasesinuse), qos=0, retain=True)
                    remoteclient.loop(timeout=2.0)
            if "lp1llkwh" in key:
                if DeviceValues[str(key)] != str(lp1llkwh):
                    mclient.publish("openWB/lp/1/kWhCounter", payload=str(lp1llkwh), qos=0, retain=True)
                    mclient.loop(timeout=2.0)
                    DeviceValues.update({'lp1llkwh': str(lp1llkwh)})
                if parentWB != "0":
                    remoteclient.publish("openWB/set/chargepoint/"+parentCPlp1+"/get/counter",
                                         payload=str(lp1llkwh*1000), qos=0, retain=True)

            if "lp1plugstat" in key:
                if DeviceValues[str(key)] != Values["lp1plugstat"]:
                    mclient.publish("openWB/lp/1/boolPlugStat", payload=Values["lp1plugstat"], qos=0, retain=True)
                    mclient.loop(timeout=2.0)
                    if int(Values["lp1plugstat"]) == "1":
                        with open('/var/www/html/openWB/ramdisk/pluggedin', 'w') as ramdisk_file:
                            ramdisk_file.write(str(Values["lp1plugstat"]))
                    DeviceValues.update({'lp1plugstat': Values["lp1plugstat"]})
                if parentWB != "0":
                    remoteclient.publish("openWB/lp/"+parentCPlp1+"/boolPlugStat", payload=Values["lp1plugstat"],
                                         qos=0, retain=True)
                    remoteclient.publish("openWB/set/chargepoint/"+parentCPlp1+"/get/plug_state",
                                         payload=Values["lp1plugstat"], qos=0, retain=True)
                    remoteclient.loop(timeout=2.0)

            if "lp1chargestat" in key:
                if DeviceValues[str(key)] != Values["lp1chargestat"]:
                    mclient.publish("openWB/lp/1/boolChargeStat", payload=Values["lp1chargestat"], qos=0, retain=True)
                    mclient.loop(timeout=2.0)
                    DeviceValues.update({'lp1chargestat': Values["lp1chargestat"]})
                if parentWB != "0":
                    remoteclient.publish("openWB/lp/"+parentCPlp1+"/boolChargeStat", payload=Values["lp1chargestat"],
                                         qos=0, retain=True)
                    remoteclient.publish("openWB/set/chargepoint/"+parentCPlp1+"/get/charge_state",
                                         payload=Values["lp1chargestat"], qos=0, retain=True)
                    remoteclient.loop(timeout=2.0)
            if "rfidtag" in key:
                if DeviceValues[str(key)] != str(rfidtag):
                    mclient.publish("openWB/lp/1/LastScannedRfidTag", payload=str(rfidtag), qos=0, retain=True)
                    mclient.loop(timeout=2.0)
                    DeviceValues.update({'rfidtag': str(rfidtag)})
                if parentWB != "0":
                    remoteclient.publish("openWB/set/chargepoint/"+parentCPlp1+"/get/rfid", payload=str(rfidtag),
                                         qos=0, retain=True)
                    remoteclient.loop(timeout=2.0)
            if lp2installed:
                if "lp2countphasesinuse" in key:
                    if DeviceValues[str(key)] != str(lp2countphasesinuse):
                        mclient.publish("openWB/lp/2/countPhasesInUse", payload=str(lp2countphasesinuse),
                                        qos=0, retain=True)
                        mclient.loop(timeout=2.0)
                        DeviceValues.update({'lp2countphasesinuse': str(lp2countphasesinuse)})
                    if parentWB != "0":
                        remoteclient.publish("openWB/lp/"+parentCPlp2+"/countPhasesInUse",
                                             payload=str(lp2countphasesinuse), qos=0, retain=True)
                        remoteclient.publish("openWB/set/chargepoint/"+parentCPlp2+"/get/phases_in_use",
                                             payload=str(lp2countphasesinuse), qos=0, retain=True)
                        remoteclient.loop(timeout=2.0)
                if "lp2watt" in key:
                    if DeviceValues[str(key)] != str(lp2llg):
                        mclient.publish("openWB/lp/2/W", payload=str(lp2llg), qos=0, retain=True)
                        mclient.loop(timeout=2.0)
                        DeviceValues.update({'lp2watt': str(lp2llg)})
                    if parentWB != "0":
                        remoteclient.publish("openWB/lp/"+parentCPlp2+"/W", payload=str(lp2llg), qos=0, retain=True)
                        remoteclient.publish("openWB/set/chargepoint/"+parentCPlp2+"/get/power",
                                             payload=str(lp2llg), qos=0, retain=True)
                        remoteclient.loop(timeout=2.0)
                if "lp2voltage1" in key:
                    if DeviceValues[str(key)] != str(lp2voltage1):
                        mclient.publish("openWB/lp/2/VPhase1", payload=str(lp2voltage1), qos=0, retain=True)
                        mclient.loop(timeout=2.0)
                        DeviceValues.update({'lp2voltage1': str(lp2voltage1)})
                    if parentWB != "0":
                        remoteclient.publish("openWB/lp/"+parentCPlp2+"/Vphase1", payload=str(lp2voltage1),
                                             qos=0, retain=True)
                        remoteclient.publish("openWB/set/chargepoint/"+parentCPlp2+"/get/voltages",
                                             payload="["+str(lp2voltage1)+","+str(lp2voltage2)+","+str(lp2voltage3)+"]",
                                             qos=0, retain=True)
                        remoteclient.loop(timeout=2.0)
                if "lp2voltage2" in key:
                    if DeviceValues[str(key)] != str(lp2voltage2):
                        mclient.publish("openWB/lp/2/VPhase2", payload=str(lp2voltage2), qos=0, retain=True)
                        mclient.loop(timeout=2.0)
                        DeviceValues.update({'lp2voltage2': str(lp2voltage2)})
                    if parentWB != "0":
                        remoteclient.publish("openWB/lp/"+parentCPlp2+"/Vphase2", payload=str(lp2voltage2),
                                             qos=0, retain=True)
                        remoteclient.loop(timeout=2.0)

                if "lp2voltage3" in key:
                    if DeviceValues[str(key)] != str(lp2voltage3):
                        mclient.publish("openWB/lp/2/VPhase3", payload=str(lp2voltage3), qos=0, retain=True)
                        mclient.loop(timeout=2.0)
                        DeviceValues.update({'lp2voltage3': str(lp2voltage3)})
                    if parentWB != "0":
                        remoteclient.publish("openWB/lp/"+parentCPlp2+"/Vphase3", payload=str(lp2voltage3),
                                             qos=0, retain=True)
                        remoteclient.loop(timeout=2.0)

                if "lp2lla1" in key:
                    if DeviceValues[str(key)] != str(lp2lla1):
                        mclient.publish("openWB/lp/2/APhase1", payload=str(lp2lla1), qos=0, retain=True)
                        mclient.loop(timeout=2.0)
                        DeviceValues.update({'lp2lla1': str(lp2lla1)})
                    if parentWB != "0":
                        remoteclient.publish("openWB/lp/"+parentCPlp2+"/Aphase1", payload=str(lp2lla1),
                                             qos=0, retain=True)
                        remoteclient.publish("openWB/set/chargepoint/"+parentCPlp2+"/get/currents",
                                             payload="["+str(lp2lla1)+","+str(lp2lla2)+","+str(lp2lla3)+"]",
                                             qos=0, retain=True)
                        remoteclient.loop(timeout=2.0)

                if "lp2lla2" in key:
                    if DeviceValues[str(key)] != str(lp2lla2):
                        mclient.publish("openWB/lp/2/APhase2", payload=str(lp2lla2), qos=0, retain=True)
                        mclient.loop(timeout=2.0)
                        DeviceValues.update({'lp2lla2': str(lp2lla2)})
                    if parentWB != "0":
                        remoteclient.publish("openWB/lp/"+parentCPlp2+"/Aphase2", payload=str(lp2lla2),
                                             qos=0, retain=True)
                        remoteclient.loop(timeout=2.0)

                if "lp2lla3" in key:
                    if DeviceValues[str(key)] != str(lp2lla3):
                        mclient.publish("openWB/lp/2/APhase3", payload=str(lp2lla3), qos=0, retain=True)
                        mclient.loop(timeout=2.0)
                        DeviceValues.update({'lp2lla3': str(lp2lla3)})
                    if parentWB != "0":
                        remoteclient.publish("openWB/lp/"+parentCPlp2+"/Aphase3", payload=str(lp2lla3),
                                             qos=0, retain=True)
                        remoteclient.loop(timeout=2.0)

                if "lp2llkwh" in key:
                    if DeviceValues[str(key)] != str(lp2llkwh):
                        mclient.publish("openWB/lp/2/kWhCounter", payload=str(lp2llkwh), qos=0, retain=True)
                        mclient.loop(timeout=2.0)
                        DeviceValues.update({'lp2llkwh': str(lp2llkwh)})
                    if parentWB != "0":
                        remoteclient.publish("openWB/set/chargepoint/"+parentCPlp2+"/get/counter",
                                             payload=str(lp2llkwh), qos=0, retain=True)
                if "lp2plugstat" in key:
                    if DeviceValues[str(key)] != Values["lp2plugstat"]:
                        mclient.publish("openWB/lp/2/boolPlugStat", payload=Values["lp2plugstat"], qos=0, retain=True)
                        mclient.loop(timeout=2.0)
                        DeviceValues.update({'lp2plugstat': Values["lp2plugstat"]})
                        if (int(Values["lp2plugstat"]) == "1"):
                            with open('/var/www/html/openWB/ramdisk/pluggedin', 'w') as ramdisk_file:
                                ramdisk_file.write(str(Values["lp2plugstat"]))
                    if parentWB != "0":
                        remoteclient.publish("openWB/lp/"+parentCPlp2+"/boolPlugStat", payload=Values["lp2plugstat"],
                                             qos=0, retain=True)
                        remoteclient.publish("openWB/set/chargepoint/"+parentCPlp2+"/get/plug_state",
                                             payload=Values["lp2plugstat"], qos=0, retain=True)
                        remoteclient.loop(timeout=2.0)

                if "lp2chargestat" in key:
                    if DeviceValues[str(key)] != Values["lp2chargestat"]:
                        mclient.publish("openWB/lp/2/boolChargeStat", payload=Values["lp2chargestat"],
                                        qos=0, retain=True)
                        mclient.loop(timeout=2.0)
                        DeviceValues.update({'lp2chargestat': Values["lp2chargestat"]})
                    if parentWB != "0":
                        remoteclient.publish("openWB/lp/"+parentCPlp2+"/boolChargeStat",
                                             payload=Values["lp2chargestat"], qos=0, retain=True)
                        remoteclient.publish("openWB/set/chargepoint/"+parentCPlp2+"/get/charge_state",
                                             payload=Values["lp2chargestat"], qos=0, retain=True)
                        remoteclient.loop(timeout=2.0)

                if "rfidtag" in key:
                    if DeviceValues[str(key)] != str(rfidtag):
                        mclient.publish("openWB/lp/2/LastScannedRfidTag", payload=str(rfidtag), qos=0, retain=True)
                        mclient.loop(timeout=2.0)
                        DeviceValues.update({'rfidtag': str(rfidtag)})
        mclient.disconnect()
        if parentWB != "0":
            remoteclient.disconnect()
    except Exception as e:
        exc_type, _, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        metercounter = metercounter + 1
        if metercounter > 5:
            log_debug(2, "Get meter Fehler:" + str(exc_type) + str(fname) + str(exc_tb.tb_lineno) + "Fehler:" + str(e))
        pass


# control of socket lock
# GPIO 23: control direction of lock motor
# GPIO 26: power to lock motor
def controlact(action: str):
    global actcooldown
    global actcooldowntimestamp

    if actcooldown < 10:
        if action == "auf":
            GPIO.output(23, GPIO.LOW)
            GPIO.output(26, GPIO.HIGH)
            time.sleep(2)
            GPIO.output(26, GPIO.LOW)
            log_debug(1, "Aktor auf")
        if action == "zu":
            GPIO.output(23, GPIO.HIGH)
            GPIO.output(26, GPIO.HIGH)
            time.sleep(3)
            GPIO.output(26, GPIO.LOW)
            log_debug(1, "Aktor zu")
    else:
        log_debug(2, "Cooldown für Aktor aktiv.")
        if actcooldowntimestamp < 50:
            actcooldowntimestamp = int(time.time())
            log_debug(1, "Beginne 5 Minuten Cooldown für Aktor")
            with open('/var/www/html/openWB/ramdisk/lastregelungaktiv', 'w') as ramdisk_file:
                ramdisk_file.write("Cooldown für Aktor der Verriegelung erforderlich. Steckt der Stecker richtig?")
    actcooldown = actcooldown + 1


# get all values to control our chargepoints
def loadregelvars():
    global actorstat
    global lp1solla
    global u1p3pstat
    global u1p3plp2stat
    global u1p3ptmpstat
    global u1p3plp2tmpstat
    global evsefailure
    global lp2installed
    global heartbeat
    global actcooldown
    global actcooldowntimestamp
    global lp1evsehres
    global lp2evsehres
    try:
        if GPIO.input(19) is False:
            actorstat = 1
        if GPIO.input(19) is True:
            actorstat = 0
    except Exception:
        actorstat = 0
        pass
    try:
        with open('ramdisk/llsoll', 'r') as value:
            if lp1evsehres == 0:
                lp1solla = int(float(value.read()))
            else:
                lp1solla = int(float(value.read())*100)
    except FileNotFoundError:
        pass
        lp1solla = 0
    try:
        with open('ramdisk/heartbeat', 'r') as value:
            heartbeat = int(value.read())
        if heartbeat > 80:
            lp1solla = 0
            log_debug(2, "Heartbeat Fehler seit " + str(heartbeat) + "Sekunden keine Verbindung, Stoppe Ladung.")
    except FileNotFoundError:
        heartbeat = 0
        pass
    log_debug(0, "LL Soll: " + str(lp1solla) + " ActorStatus: " + str(actorstat))
    if buchseconfigured == 1:
        log_debug(1, "in Buchse" + str(evsefailure)+"lp1plugstat:"+str(Values["lp1plugstat"]))
        if actcooldowntimestamp > 50:
            tst = actcooldowntimestamp+300
            if tst < int(time.time()):
                actcooldowntimestamp = 0
                actcooldown = 0
                log_debug(1, "Cooldown für Aktor zurückgesetzt")
            else:
                timeleft = tst-int(time.time())
                log_debug(1, str(timeleft) + " Sekunden Cooldown für Aktor verbleiben.")

        if evsefailure == 0:
            if Values["lp1plugstat"] == 1:
                if actorstat == 0:
                    controlact("zu")
            if Values["lp1plugstat"] == 0:
                if actorstat == 1:
                    writelp1evse(0)
                    controlact("auf")
            if actorstat == 1:
                if Values["lp1evsell"] != lp1solla and Values["lp1plugstat"] == 1:
                    writelp1evse(lp1solla)
            else:
                if Values["lp1evsell"] != 0:
                    writelp1evse(0)
    else:
        if Values["lp1evsell"] != lp1solla:
            writelp1evse(lp1solla)
    if lp2installed:
        try:
            with open('ramdisk/llsolls1', 'r') as value:
                if lp2evsehres == 0:
                    lp2solla = int(float(value.read()))
                else:
                    lp2solla = int(float(value.read())*100)
        except Exception:
            pass
            lp2solla = 0
        log_debug(0, "LL lp2 Soll: " + str(lp2solla))
        if Values["lp2evsell"] != lp2solla:
            writelp2evse(lp2solla)
    try:
        with open('ramdisk/u1p3pstat', 'r') as value:
            u1p3ptmpstat = int(value.read())
    except Exception:
        pass
        u1p3ptmpstat = 3
    try:
        u1p3pstat
    except Exception:
        u1p3pstat = 3
    if u1p3pstat != u1p3ptmpstat:
        log_debug(1, "Umschaltung erfolgt auf " + str(u1p3ptmpstat) + " Phasen an Lp1")
        writelp1evse(0)
        time.sleep(1)
        if u1p3ptmpstat == 1:
            GPIO.output(22, GPIO.HIGH)
            GPIO.output(29, GPIO.HIGH)
            time.sleep(2)
            GPIO.output(29, GPIO.LOW)
            time.sleep(5)
            GPIO.output(22, GPIO.LOW)
            time.sleep(1)
        if u1p3ptmpstat == 3:
            GPIO.output(22, GPIO.HIGH)
            GPIO.output(37, GPIO.HIGH)
            time.sleep(2)
            GPIO.output(37, GPIO.LOW)
            time.sleep(5)
            GPIO.output(22, GPIO.LOW)
            time.sleep(1)
        u1p3pstat = u1p3ptmpstat
        writelp1evse(lp1solla)
    if lp2installed:
        try:
            with open('ramdisk/u1p3plp2stat', 'r') as value:
                u1p3plp2tmpstat = int(value.read())
        except Exception:
            pass
            u1p3plp2tmpstat = 3
        try:
            u1p3plp2stat
        except Exception:
            u1p3plp2stat = 3
        if u1p3plp2stat != u1p3plp2tmpstat:
            log_debug(1, "Umschaltung erfolgt auf " + str(u1p3plp2tmpstat) + " Phasen an Lp2")
            writelp2evse(0)
            time.sleep(1)
            if u1p3plp2tmpstat == 1:
                GPIO.output(15, GPIO.HIGH)
                GPIO.output(11, GPIO.HIGH)
                time.sleep(2)
                GPIO.output(11, GPIO.LOW)
                time.sleep(5)
                GPIO.output(15, GPIO.LOW)
                time.sleep(1)
            if u1p3plp2tmpstat == 3:
                GPIO.output(15, GPIO.HIGH)
                GPIO.output(13, GPIO.HIGH)
                time.sleep(2)
                GPIO.output(13, GPIO.LOW)
                time.sleep(5)
                GPIO.output(15, GPIO.LOW)
                time.sleep(1)
            u1p3plp2stat = u1p3plp2tmpstat
            writelp2evse(lp2solla)


def writelp2evse(lla):
    try:
        client.write_registers(1000, lla, unit=2)
        log_debug(1, "Write to EVSE lp2 " + str(lla))
    except Exception:
        log_debug(2, "FAILEDWrite to EVSE lp2 " + str(lla))


def writelp1evse(lla):
    if lp1evsehres == 1:
        mpp = pp*100
        if lla > mpp:
            lla = mpp
    else:
        if lla > pp:
            lla = pp
    try:
        client.write_registers(1000, lla, unit=1)
        log_debug(1, "Write to EVSE lp1 " + str(lla))
    except Exception:
        log_debug(2, "FAILED Write to EVSE lp1 " + str(lla))


while True:
    getmeter()
    loadregelvars()
    time.sleep(1)
