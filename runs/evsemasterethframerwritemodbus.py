#!/usr/bin/python3
import sys
from pymodbus.transaction import ModbusRtuFramer
from pymodbus.client.sync import ModbusTcpClient

lla = int(sys.argv[1])

client = ModbusTcpClient('192.168.193.18', port=8899, framer=ModbusRtuFramer)
rq = client.write_registers(1000, lla, unit=1)
