#!/usr/bin/python3
import sys
from pymodbus.transaction import ModbusRtuFramer
from pymodbus.client.sync import ModbusTcpClient

seradd = str(sys.argv[1])
evseid = int(sys.argv[2])
wreg = int(sys.argv[3])
val = int(sys.argv[4])

client = ModbusTcpClient(seradd, port=8899, framer=ModbusRtuFramer)
rq = client.write_registers(wreg, val, unit=evseid)
