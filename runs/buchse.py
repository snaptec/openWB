#!/usr/bin/python
import os
import time
import struct
import traceback
from typing import Tuple
import RPi.GPIO as GPIO
from pymodbus.client.sync import ModbusSerialClient
import paho.mqtt.client as mqtt

basePath = "/var/www/html/openWB"
ramdiskPath = basePath + "/ramdisk"
logFilename = ramdiskPath + "/buchse.log"

DeviceValues = {}
Values = {}


# handling of all logging statements
def log_debug(level: int, msg: str, traceback_str: str = None) -> None:
    if level >= loglevel:
        with open(logFilename, 'a') as log_file:
            log_file.write(time.ctime() + ': ' + msg + '\n')
            if traceback_str is not None:
                log_file.write(traceback_str + '\n')


# write value to file in ramdisk
def write_to_ramdisk(filename: str, content: str) -> None:
    with open(ramdiskPath + "/" + filename, "w") as file:
        file.write(content)


# read value from file in ramdisk
def read_from_ramdisk(filename: str) -> str:
    try:
        with open(ramdiskPath + "/" + filename, 'r') as file:
            return file.read()
    except FileNotFoundError:
        log_debug(2, "Error reading file '" + filename + "' from ramdisk!", traceback.format_exc())
        return ""


def init_gpio() -> None:
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


def init_values() -> None:
    global DeviceValues
    global Values
    # values LP1
    DeviceValues.update({'lp1voltage1': str(5)})
    DeviceValues.update({'lp1voltage2': str(5)})
    DeviceValues.update({'lp1voltage3': str(5)})
    DeviceValues.update({'lp1lla1': str(5)})
    DeviceValues.update({'lp1lla2': str(5)})
    DeviceValues.update({'lp1lla3': str(5)})
    DeviceValues.update({'lp1llkwh': str(5)})
    DeviceValues.update({'lp1watt': str(5)})
    DeviceValues.update({'lp1chargestat': str(5)})
    DeviceValues.update({'lp1plugstat': str(5)})
    DeviceValues.update({'lp1readerror': str(0)})
    Values.update({'lp1plugstat': str(5)})
    Values.update({'lp1chargestat': str(5)})
    Values.update({'lp1evsell': str(1)})


# read all meter values and publish to mqtt broker
def read_meter():
    global evsefailure
    global client
    global llmeterconfiglp1
    global sdmid

    if (llmeterconfiglp1 == 0):
        log_debug(2, "Erkenne verbauten Zaehler.")
        # check sdm
        try:
            resp = client.read_input_registers(0x00, 2, unit=105)
            voltage = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
            if int(voltage) > 20:
                llmeterconfiglp1 = 105
                sdmid = 105
                log_debug(2, "SDM Zaehler erkannt")
        except AttributeError:
            log_debug(2, "SDM check failed", traceback.format_exc())
            # check B23
            try:
                resp = client.read_holding_registers(0x5B00, 2, unit=201)
                voltage = resp.registers[1]
                if int(voltage) > 20:
                    llmeterconfiglp1 = 201
                    sdmid = 201
                    log_debug(2, "B23 Zaehler erkannt")
            except AttributeError:
                log_debug(2, "B23 check failed", traceback.format_exc())
    else:
        sdmid = llmeterconfiglp1
    try:
        if sdmid < 200:
            # SDM
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
            write_to_ramdisk("llaktuell", str(lp1llg))
            resp = client.read_input_registers(0x00, 2, unit=sdmid)
            voltage = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
            lp1voltage1 = float("%.1f" % voltage)
            write_to_ramdisk("llv1", str(lp1voltage1))
            resp = client.read_input_registers(0x02, 2, unit=sdmid)
            voltage = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
            lp1voltage2 = float("%.1f" % voltage)
            write_to_ramdisk("llv2", str(lp1voltage2))
            resp = client.read_input_registers(0x04, 2, unit=sdmid)
            voltage = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
            lp1voltage3 = float("%.1f" % voltage)
            write_to_ramdisk("llv3", str(lp1voltage3))
            resp = client.read_input_registers(0x06, 2, unit=sdmid)
            lp1lla1 = float(struct.unpack('>f', struct.pack('>HH', *resp.registers))[0])
            lp1lla1 = float("%.1f" % lp1lla1)
            write_to_ramdisk("lla1", str(lp1lla1))
            resp = client.read_input_registers(0x08, 2, unit=sdmid)
            lp1lla2 = float(struct.unpack('>f', struct.pack('>HH', *resp.registers))[0])
            lp1lla2 = float("%.1f" % lp1lla2)
            write_to_ramdisk("lla2", str(lp1lla2))
            resp = client.read_input_registers(0x0A, 2, unit=sdmid)
            lp1lla3 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
            lp1lla3 = float("%.1f" % lp1lla3)
            write_to_ramdisk("lla3", str(lp1lla3))
            resp = client.read_input_registers(0x0156, 2, unit=sdmid)
            lp1llkwh = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
            lp1llkwh = float("%.3f" % lp1llkwh)
            write_to_ramdisk("llkwh", str(lp1llkwh))
            resp = client.read_input_registers(0x46, 2, unit=sdmid)
            hz = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
            hz = float("%.2f" % hz)
            write_to_ramdisk("llhz", str(hz))
        else:
            # B23
            # llkwh
            resp = client.read_holding_registers(0x5000, 4, unit=sdmid)
            lp1llkwh = struct.unpack('>Q', struct.pack('>HHHH', *resp.registers))[0]/100
            write_to_ramdisk("llkwh", str(lp1llkwh))
            # Voltage
            resp = client.read_holding_registers(0x5B00, 2, unit=sdmid)
            voltage = resp.registers[1]
            lp1voltage1 = float(voltage) / 10
            write_to_ramdisk("llv1", str(lp1voltage1))
            resp = client.read_holding_registers(0x5B02, 2, unit=sdmid)
            lp1voltage2 = resp.registers[1]
            lp1voltage2 = float(lp1voltage2) / 10
            write_to_ramdisk("llv2", str(lp1voltage2))
            resp = client.read_holding_registers(0x5B04, 2, unit=sdmid)
            voltage = resp.registers[1]
            lp1voltage3 = float(voltage) / 10
            write_to_ramdisk("llv3", str(lp1voltage3))
            # Ampere
            resp = client.read_holding_registers(0x5B0C, 2, unit=sdmid)
            amp = resp.registers[1]
            lp1lla1 = float(amp) / 100
            write_to_ramdisk("lla1", str(lp1lla1))
            resp = client.read_holding_registers(0x5B0E, 2, unit=sdmid)
            amp = resp.registers[1]
            lp1lla2 = float(amp) / 100
            write_to_ramdisk("lla2", str(lp1lla2))
            resp = client.read_holding_registers(0x5B10, 2, unit=sdmid)
            amp = resp.registers[1]
            lp1lla3 = float(amp) / 100
            write_to_ramdisk("lla3", str(lp1lla3))
            # Gesamt watt
            resp = client.read_holding_registers(0x5B14, 2, unit=sdmid)
            lp1llg = int(struct.unpack('>i', struct.pack('>HH', *resp.registers))[0]/100)
            write_to_ramdisk("llaktuell", str(lp1llg))
            # LL Hz
            resp = client.read_holding_registers(0x5B2C, 2, unit=sdmid)
            hz = float(resp.registers[0]) / 100
            write_to_ramdisk("llhz", str(hz))

        try:
            time.sleep(0.1)
            rq = client.read_holding_registers(1000, 1, unit=1)
            lp1ll = rq.registers[0]
            evsefailure = 0
        except:
            lp1ll = 0
            evsefailure = 1
        try:
            time.sleep(0.1)
            rq = client.read_holding_registers(1002, 1, unit=1)
            lp1var = rq.registers[0]
            evsefailure = 0
            DeviceValues.update({'lp1readerror': str(0)})
        except:
            DeviceValues.update({'lp1readerror': str(int(DeviceValues['lp1readerror'])+1)})
            log_debug(2, "Fehler!", traceback.format_exc())
            lp1var = 5
            evsefailure = 1
        if (lp1var == 5 and int(DeviceValues['lp1readerror']) > MaxEvseError):
            log_debug(2, "Anhaltender Fehler beim Auslesen der EVSE von lp1! (" +
                      str(DeviceValues['lp1readerror']) + ")")
            log_debug(2, "Plugstat und Chargestat werden zurückgesetzt.")
            Values.update({'lp1plugstat': 0})
            Values.update({'lp1chargestat': 0})
        elif (lp1var == 1):
            Values.update({'lp1plugstat': 0})
            Values.update({'lp1chargestat': 0})
        elif (lp1var == 2):
            Values.update({'lp1plugstat': 1})
            Values.update({'lp1chargestat': 0})
        elif (lp1var == 3 and lp1ll > 0):
            Values.update({'lp1plugstat': 1})
            Values.update({'lp1chargestat': 1})
        elif (lp1var == 3 and lp1ll == 0):
            Values.update({'lp1plugstat': 1})
            Values.update({'lp1chargestat': 0})
        write_to_ramdisk("plugstat", str(Values["lp1plugstat"]))
        write_to_ramdisk("chargestat", str(Values["lp1chargestat"]))
        Values.update({'lp1evsell': lp1ll})
        log_debug(0, "EVSE lp1plugstat: " + str(lp1var) + " EVSE lp1LL: " + str(lp1ll))

        mclient = mqtt.Client("openWB-buchse-bulkpublisher-" + str(os.getpid()))
        mclient.connect("localhost")
        mclient.loop(timeout=2.0)
        for key in DeviceValues:
            if ("lp1watt" in key):
                if (DeviceValues[str(key)] != str(lp1llg)):
                    mclient.publish("openWB/lp/1/W", payload=str(lp1llg), qos=0, retain=True)
                    mclient.loop(timeout=2.0)
                    DeviceValues.update({'lp1watt': str(lp1llg)})
            if ("lp1voltage1" in key):
                if (DeviceValues[str(key)] != str(lp1voltage1)):
                    mclient.publish("openWB/lp/1/VPhase1", payload=str(lp1voltage1), qos=0, retain=True)
                    mclient.loop(timeout=2.0)
                    DeviceValues.update({'lp1voltage1': str(lp1voltage1)})
            if ("lp1voltage2" in key):
                if (DeviceValues[str(key)] != str(lp1voltage2)):
                    mclient.publish("openWB/lp/1/VPhase2", payload=str(lp1voltage2), qos=0, retain=True)
                    mclient.loop(timeout=2.0)
                    DeviceValues.update({'lp1voltage2': str(lp1voltage2)})
            if ("lp1voltage3" in key):
                if (DeviceValues[str(key)] != str(lp1voltage3)):
                    mclient.publish("openWB/lp/1/VPhase3", payload=str(lp1voltage3), qos=0, retain=True)
                    mclient.loop(timeout=2.0)
                    DeviceValues.update({'lp1voltage3': str(lp1voltage3)})
            if ("lp1lla1" in key):
                if (DeviceValues[str(key)] != str(lp1lla1)):
                    mclient.publish("openWB/lp/1/APhase1", payload=str(lp1lla1), qos=0, retain=True)
                    mclient.loop(timeout=2.0)
                    DeviceValues.update({'lp1lla1': str(lp1lla1)})
            if ("lp1lla2" in key):
                if (DeviceValues[str(key)] != str(lp1lla2)):
                    mclient.publish("openWB/lp/1/APhase2", payload=str(lp1lla2), qos=0, retain=True)
                    mclient.loop(timeout=2.0)
                    DeviceValues.update({'lp1lla2': str(lp1lla2)})
            if ("lp1lla3" in key):
                if (DeviceValues[str(key)] != str(lp1lla3)):
                    mclient.publish("openWB/lp/1/APhase3", payload=str(lp1lla3), qos=0, retain=True)
                    mclient.loop(timeout=2.0)
                    DeviceValues.update({'lp1lla3': str(lp1lla3)})
            if ("lp1llkwh" in key):
                if (DeviceValues[str(key)] != str(lp1llkwh)):
                    mclient.publish("openWB/lp/1/kWhCounter", payload=str(lp1llkwh), qos=0, retain=True)
                    mclient.loop(timeout=2.0)
                    DeviceValues.update({'lp1llkwh': str(lp1llkwh)})
            if ("lp1plugstat" in key):
                if (DeviceValues[str(key)] != Values["lp1plugstat"]):
                    mclient.publish("openWB/lp/1/boolPlugStat", payload=Values["lp1plugstat"], qos=0, retain=True)
                    mclient.loop(timeout=2.0)
                    DeviceValues.update({'lp1plugstat': Values["lp1plugstat"]})
            if ("lp1chargestat" in key):
                if (DeviceValues[str(key)] != Values["lp1chargestat"]):
                    mclient.publish("openWB/lp/1/boolChargeStat", payload=Values["lp1chargestat"], qos=0, retain=True)
                    mclient.loop(timeout=2.0)
                    DeviceValues.update({'lp1chargestat': Values["lp1chargestat"]})
        mclient.disconnect()
    except Exception:
        log_debug(2, "Get meter Fehler!", traceback.format_exc())


# control of socket lock
# GPIO 23: control direction of lock motor
# GPIO 26: power to lock motor
def set_socket_actuator(action):
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


# get actual socket lock state
def get_socket_state() -> int:
    actorstat_tmp = GPIO.input(19)
    if actorstat_tmp == GPIO.LOW:
        return 1
    else:
        return 0


# get all values to control our chargepoint
def load_control_values():
    global actorstat
    global lp1solla
    global u1p3pstat
    global u1p3ptmpstat
    global evsefailure

    actorstat = get_socket_state()
    try:
        lp1solla = int(read_from_ramdisk("llsoll"))
    except ValueError:
        lp1solla = 0
    log_debug(0, "LL Soll: " + str(lp1solla) + " ActorStatus: " + str(actorstat))
    if socket_configured:
        if (evsefailure == 0):
            if (Values["lp1plugstat"] == 1):
                if (actorstat == 0):
                    set_socket_actuator("zu")
            if (Values["lp1plugstat"] == 0):
                if (actorstat == 1):
                    writelp1evse(0)
                    set_socket_actuator("auf")
            if (actorstat == 1):
                if (Values["lp1evsell"] != lp1solla and Values["lp1plugstat"] == 1):
                    writelp1evse(lp1solla)
            else:
                if (Values["lp1evsell"] != 0):
                    writelp1evse(0)
    else:
        if (Values["lp1evsell"] != lp1solla):
            writelp1evse(lp1solla)
    try:
        u1p3ptmpstat = int(read_from_ramdisk("u1p3pstat"))
    except ValueError:
        u1p3ptmpstat = 3
    try:
        u1p3pstat
    except:
        u1p3pstat = 3
    u1p3pstat = switch_phases_cp1(u1p3ptmpstat, u1p3pstat)


def __switch_phases(gpio_cp: int, gpio_relay: int):
    GPIO.output(gpio_cp, GPIO.HIGH)  # CP on
    GPIO.output(gpio_relay, GPIO.HIGH)  # 3 on/off
    time.sleep(2)
    GPIO.output(gpio_relay, GPIO.LOW)  # 3 on/off
    time.sleep(5)
    GPIO.output(gpio_cp, GPIO.LOW)  # CP off
    time.sleep(1)


def switch_phases_cp1(new_phases: int, old_phases: int) -> int:
    if (new_phases != old_phases):
        log_debug(1, "switching phases on cp1: old=" + str(old_phases) + " new=" + str(new_phases))
        gpio_cp = 22
        if (new_phases == 1):
            gpio_relay = 29
        else:
            gpio_relay = 37
        __switch_phases(gpio_cp, gpio_relay)
    else:
        log_debug(0, "no need to switch phases on cp1: old=" + str(old_phases) + " new=" + str(new_phases))
    return new_phases


def writelp1evse(lla):
    if (lla > pp):
        lla = pp
    client.write_registers(1000, lla, unit=1)
    log_debug(1, "Write to EVSE lp1 " + str(lla))


# check for "openWB Buchse"
def check_for_socket() -> Tuple[bool, int]:
    try:
        with open('/home/pi/ppbuchse', 'r') as value:
            pp_value = int(value.read())
    except (FileNotFoundError, ValueError):
        pp_value = 32
    # here we always have a socket
    socket_is_configured = True
    log_debug(1, "check for socket: " + str(socket_is_configured) + " " + str(pp_value))
    return [socket_is_configured, pp_value]


# guess USB/modbus device name
def detect_modbus_usb_port() -> str:
    try:
        with open("/dev/ttyUSB0"):
            return "/dev/ttyUSB0"
    except FileNotFoundError:
        return "/dev/serial0"


loglevel = 1

MaxEvseError = 5
sdmid = 105
actorstat = 0
evsefailure = 0
llmeterconfiglp1 = 0

init_gpio()
init_values()
socket_configured, pp = check_for_socket()
seradd = detect_modbus_usb_port()
# connect with USB/modbus device
with ModbusSerialClient(method="rtu", port=seradd, baudrate=9600, stopbits=1, bytesize=8, timeout=1) as client:
    # start our control loop
    while True:
        read_meter()
        load_control_values()
        time.sleep(1)
