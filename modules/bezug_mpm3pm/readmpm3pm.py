#!/usr/bin/python
import sys
import os
import time
import getopt
import struct
seradd = str(sys.argv[1])
from pymodbus.client.sync import ModbusSerialClient
client = ModbusSerialClient(method = "rtu", port=seradd, baudrate=9600,
                                stopbits=1, bytesize=8, timeout=1)


sdmid = int(sys.argv[2])

#Voltage
resp = client.read_input_registers(0x08,4, unit=sdmid)
voltage = resp.registers[1]
voltage = float(voltage) / 10
f = open('/var/www/html/openWB/ramdisk/evuv1', 'w')
f.write(str(voltage))
f.close()

resp = client.read_input_registers(0x0A,4, unit=sdmid)
voltage = resp.registers[1]
voltage = float(voltage) / 10
f = open('/var/www/html/openWB/ramdisk/evuv2', 'w')
f.write(str(voltage))
f.close()

resp = client.read_input_registers(0x0C,4, unit=sdmid)
voltage = resp.registers[1]
voltage = float(voltage) / 10
f = open('/var/www/html/openWB/ramdisk/evuv3', 'w')
f.write(str(voltage))
f.close()

resp = client.read_input_registers(0x0002,2, unit=sdmid)
ikwh = resp.registers[1]
ikwh = float(ikwh) * 10
f = open('/var/www/html/openWB/ramdisk/bezugkwh', 'w')
f.write(str(ikwh))
f.close()

resp = client.read_input_registers(0x0E,2, unit=sdmid)
lla1 = resp.registers[1]
lla1 = float(lla1) / 100
f = open('/var/www/html/openWB/ramdisk/bezuga1', 'w')
f.write(str(lla1))
f.close()

resp = client.read_input_registers(0x10,2, unit=sdmid)
lla2 = resp.registers[1]
lla2 = float(lla2) / 100
f = open('/var/www/html/openWB/ramdisk/bezuga2', 'w')
f.write(str(lla2))
f.close()

resp = client.read_input_registers(0x12,2, unit=sdmid)
lla3 = resp.registers[1]
lla3 = float(lla3) / 100
f = open('/var/www/html/openWB/ramdisk/bezuga3', 'w')
f.write(str(lla3))
f.close()

#total watt
resp = client.read_input_registers(0x26,2, unit=sdmid)
if ( resp.registers[0] > 32768 ):
    firstreg = 65536 - resp.registers[0] - 1
    firstreg = firstreg * 65536
    final = firstreg + resp.registers[1]
    final = final / 100 * -1
else:
    firstreg = resp.registers[0] * 65536
    final = firstreg + resp.registers[1]
    final = final / 100
f = open('/var/www/html/openWB/ramdisk/wattbezug', 'w')
f.write(str(final))
f.close()

#export kwh
resp = client.read_input_registers(0x0004,4, unit=sdmid)
ekwh = resp.registers[1]
ekwh = float(ekwh) * 10
f = open('/var/www/html/openWB/ramdisk/einspeisungkwh', 'w')
f.write(str(ekwh))
f.close()

