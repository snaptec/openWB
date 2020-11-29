#!/usr/bin/python
import sys
import os
import time
import getopt
import socket
import ConfigParser
import struct
import binascii
from pymodbus.client.sync import ModbusTcpClient
ipaddress = str(sys.argv[1])
port = 502
from pymodbus.client.sync import ModbusTcpClient
client = ModbusTcpClient(ipaddress, port=502)
#EVStatus
resp= client.read_input_registers(100,1,unit=180)
EVStatus = resp.registers[0]
f = open('/var/www/html/openWB/ramdisk/phoenixlp1rEVStatus', 'w')
f.write(chr(EVStatus))
f.close()
#ProxLadestrom
resp= client.read_input_registers(101,1,unit=180)
ProxLadestrom = resp.registers[0]
f = open('/var/www/html/openWB/ramdisk/phoenixlp1rProxLadestrom', 'w')
f.write(str(ProxLadestrom))
f.close()
#Ladezeit
resp= client.read_input_registers(102,2,unit=180)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value2, '04x') + format(value1, '04x')
Ladezeit = int(struct.unpack('>i', all.decode('hex'))[0])
f = open('/var/www/html/openWB/ramdisk/phoenixlp1rLadezeit', 'w')
f.write(str(Ladezeit))
f.close()
#ProxLadestrom
resp= client.read_input_registers(101,1,unit=180)
ProxLadestrom = resp.registers[0]
f = open('/var/www/html/openWB/ramdisk/phoenixlp1rProxLadestrom', 'w')
f.write(str(ProxLadestrom))
f.close()
#Firmware
resp= client.read_input_registers(105,2,unit=180)
value1 = resp.registers[0]
value2 = resp.registers[1]
#all = (value2) +" " + (value1)
#Firmware = all
f = open('/var/www/html/openWB/ramdisk/phoenixlp1rFirmware', 'w')
f.write(str(value1))
f.close()
#Fehlercode
resp= client.read_input_registers(107,1,unit=180)
Fehlercode = resp.registers[0]
f = open('/var/www/html/openWB/ramdisk/phoenixlp1rFehlercode', 'w')
f.write(str(Fehlercode))
f.close()
#V1
resp= client.read_input_registers(108,2,unit=180)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value2, '04x') + format(value1, '04x')
V1 = int(struct.unpack('>i', all.decode('hex'))[0])
f = open('/var/www/html/openWB/ramdisk/phoenixlp1rV1', 'w')
f.write(str(V1))
f.close()
#V2
resp= client.read_input_registers(110,2,unit=180)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value2, '04x') + format(value1, '04x')
V2 = int(struct.unpack('>i', all.decode('hex'))[0])
f = open('/var/www/html/openWB/ramdisk/phoenixlp1rV2', 'w')
f.write(str(V2))
f.close()
#V3
resp= client.read_input_registers(112,2,unit=180)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value2, '04x') + format(value1, '04x')
V3 = int(struct.unpack('>i', all.decode('hex'))[0])
f = open('/var/www/html/openWB/ramdisk/phoenixlp1rV3', 'w')
f.write(str(V3))
f.close()
#A1
resp= client.read_input_registers(114,2,unit=180)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value2, '04x') + format(value1, '04x')
A1 = int(struct.unpack('>i', all.decode('hex'))[0])
f = open('/var/www/html/openWB/ramdisk/phoenixlp1rA1', 'w')
f.write(str(A1))
f.close()
#A2
resp= client.read_input_registers(116,2,unit=180)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value2, '04x') + format(value1, '04x')
A2 = int(struct.unpack('>i', all.decode('hex'))[0])
f = open('/var/www/html/openWB/ramdisk/phoenixlp1rA2', 'w')
f.write(str(A2))
f.close()
#A3
resp= client.read_input_registers(118,2,unit=180)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value2, '04x') + format(value1, '04x')
A3 = int(struct.unpack('>i', all.decode('hex'))[0])
f = open('/var/www/html/openWB/ramdisk/phoenixlp1rA3', 'w')
f.write(str(A3))
f.close()
#actPower
resp= client.read_input_registers(120,2,unit=180)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value2, '04x') + format(value1, '04x')
actPower = int(struct.unpack('>i', all.decode('hex'))[0])
f = open('/var/www/html/openWB/ramdisk/phoenixlp1ractPower', 'w')
f.write(str(actPower))
f.close()
#EnergyUpTime
resp= client.read_input_registers(120,2,unit=180)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value2, '04x') + format(value1, '04x')
EnergyUpTime = int(struct.unpack('>i', all.decode('hex'))[0])
f = open('/var/www/html/openWB/ramdisk/phoenixlp1rEnergyUpTime', 'w')
f.write(str(EnergyUpTime))
f.close()
#EnergySession
resp= client.read_input_registers(132,2,unit=180)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value2, '04x') + format(value1, '04x')
EnergySession = int(struct.unpack('>i', all.decode('hex'))[0])
f = open('/var/www/html/openWB/ramdisk/phoenixlp1rEnergySession', 'w')
f.write(str(EnergySession))
f.close()
#PWM
resp= client.read_holding_registers(300,1,unit=180)
PWM = resp.registers[0]
f = open('/var/www/html/openWB/ramdisk/phoenixlp1rPWM', 'w')
f.write(str(PWM))
f.close()
#EnableSet
resp= client.read_coils(400,1,unit=180)
if resp.bits[0] == True:
 EnableSet = 1
else:
 EnableSet = 0
f = open('/var/www/html/openWB/ramdisk/phoenixlp1rEnableSet', 'w')
f.write(str(EnableSet))
f.close()
