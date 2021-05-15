#!/usr/bin/python
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

from pymodbus.client.sync import ModbusTcpClient as ModbusClient

active_power = 1

client = ModbusClient(ipaddress, port=502, unit_id=modbusID)
client.connect()
if client.connect():
    time.sleep(1)
    rr = client.read_holding_registers(0x7D50, 0x02)

    active_power = rr.registers[1]

f = open('/var/www/html/openWB/ramdisk/pv2watt', 'w')
f.write(str(active_power*-1))
f.close()
