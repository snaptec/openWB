#!/usr/bin/python
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import sys
import os
import time
import getopt
import socket
import ConfigParser
import struct
import binascii

ipaddress = str(sys.argv[1])
modbusID = str(sys.argv[2])

active_power = 0
total_power = 0

client = ModbusClient(ipaddress, port=502, unit_id=modbusID)

client.connect()
if client.connect():
    time.sleep(1)
    rr = client.read_holding_registers(0x7D50, 0x02)
    time.sleep(5)
    rw = client.read_holding_registers(0x7D6A, 0x02)

    active_power = rr.registers[1]
    total_power = rw.registers[1]


f = open('/var/www/html/openWB/ramdisk/pv2watt', 'w')
f.write(str(active_power*-1))
f.close()

f = open('/var/www/html/openWB/ramdisk/pv2kwh', 'w')
f.write(str(total_power*10.0))
f.close()
