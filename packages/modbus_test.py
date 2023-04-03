#!/usr/bin/env python3
import sys
import time

from modules.common import modbus
ipaddress = str(sys.argv[1])
port = int(sys.argv[2])
slaveid = int(sys.argv[3])
start = int(sys.argv[4])
length = int(sys.argv[5])
data_type = str(sys.argv[6])
func = int(sys.argv[7])
named_tuple = time.localtime()  # get struct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S opentrace", named_tuple)
try:
    client = modbus.ModbusTcpClient_(ipaddress, port=port)
    if func == 0:
        if length > 1:
            resp = client.read_input_registers(start, [modbus.ModbusDataType[data_type]]*length, unit=slaveid)
        else:
            resp = client.read_input_registers(start, modbus.ModbusDataType[data_type], unit=slaveid)
    else:
        if length > 1:
            resp = client.read_holding_registers(start, [modbus.ModbusDataType[data_type]]*length, unit=slaveid)
        else:
            resp = client.read_holding_registers(start, modbus.ModbusDataType[data_type], unit=slaveid)
    print(resp)
except Exception as e:
    print("Exception "+str(e))
