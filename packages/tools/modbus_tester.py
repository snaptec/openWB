#!/usr/bin/env python3
import sys
import time
from modules.common import modbus

host = sys.argv[1]
port = int(sys.argv[2])
slave_id = int(sys.argv[3])
start = int(sys.argv[4])
length = int(sys.argv[5])
data_type = sys.argv[6]
func = int(sys.argv[7])


print(time.strftime("%Y-%m-%d %H:%M:%S modbus-tester"))
print("Parameter:")
print("Host: " + host)
print("Port: " + str(port))
print("Modbus ID: " + str(slave_id))
print("Startadresse: " + str(start))
print("Anzahl: " + str(length))
print("Datentyp: " + data_type)
print("Funktion: " + str(func) + "\n")
try:
    client = modbus.ModbusTcpClient_(host, port=port)
    if func == 4:
        if length > 1:
            resp = client.read_input_registers(start, [modbus.ModbusDataType[data_type]]*length, unit=slave_id)
        else:
            resp = client.read_input_registers(start, modbus.ModbusDataType[data_type], unit=slave_id)
    elif func == 3:
        if length > 1:
            resp = client.read_holding_registers(start, [modbus.ModbusDataType[data_type]]*length, unit=slave_id)
        else:
            resp = client.read_holding_registers(start, modbus.ModbusDataType[data_type], unit=slave_id)
    else:
        print("unsupported function code: " + str(func))
        exit(1)
    print("Ergebnis: " + str(resp))
except Exception as e:
    print("Exception "+str(e))
