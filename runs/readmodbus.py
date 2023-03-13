#!/usr/bin/env python3
import sys
from pymodbus.client.sync import ModbusSerialClient


def detect_modbus_usb_port():
    """guess USB/modbus device name"""
    known_devices = ("/dev/ttyUSB0", "/dev/ttyACM0", "/dev/serial0")
    for device in known_devices:
        try:
            with open(device):
                return device
        except FileNotFoundError:
            pass
    return known_devices[-1]  # this does not make sense, but is the same behavior as the old code


seradd = detect_modbus_usb_port()
modbusid = int(sys.argv[2])
readreg = int(sys.argv[3])
reganzahl = int(sys.argv[4])

client = ModbusSerialClient(method="rtu", port=seradd, baudrate=9600, stopbits=1, bytesize=8, timeout=1)
request = client.read_holding_registers(readreg, reganzahl, unit=modbusid)
if request.isError():
    # handle error, log?
    print('Modbus Error:', request)
else:
    result = request.registers
    print(result[0])
