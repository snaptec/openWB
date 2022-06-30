#!/usr/bin/python3
import sys
from pymodbus.client.sync import ModbusTcpClient

readreg = int(sys.argv[1])
reganzahl = int(sys.argv[2])

client = ModbusTcpClient('192.168.193.26', port=8899)
rq = client.read_holding_registers(readreg, reganzahl, unit=1)
print(rq.registers[0])
