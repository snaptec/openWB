#!/usr/bin/python
# coding: utf8

#########################################################
#
#liest aus Wechselrichter Kostal Plenticore mit EM300
#den Strom auf allen 3 Phasen sowie Bezug/Einspeisung
#bei Verwendung EM300 am Hausanschlusspunkt
#
#2019 Kevin Wieland, Michael Ortenstein
#This file is part of openWB
#
#########################################################

import sys
import os
import time
import getopt
import socket
import ConfigParser
import struct
import binascii
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
ipaddress = str(sys.argv[1])
from pymodbus.client.sync import ModbusTcpClient
client = ModbusTcpClient(ipaddress, port=1502)

#Strom auf Phasen 1-3 EVU aus Kostal Plenticore lesen
#Wechselrichter bekommt Daten von Energy Manager EM300

#Phase 1
#dazu Plenticore Register 222 lesen: Current_phase_1_(powermeter) [A]
resp= client.read_holding_registers(222,2,unit=71)
FRegister = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Little)
final =round(FRegister.decode_32bit_float(),2)
f = open('/var/www/html/openWB/ramdisk/bezuga1', 'w')
f.write(str(final))
f.close()

#Phase 2
#dazu Plenticore Register 232 lesen: Current_phase_2_(powermeter) [A]
resp= client.read_holding_registers(232,2,unit=71)
FRegister = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Little)
final =round(FRegister.decode_32bit_float(),2)
f = open('/var/www/html/openWB/ramdisk/bezuga2', 'w')
f.write(str(final))
f.close()

#Phase 3
#dazu Plenticore Register 242 lesen: Current_phase_3_(powermeter) [A]
resp= client.read_holding_registers(242,2,unit=71)
FRegister = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Little)
final =round(FRegister.decode_32bit_float(),2)
f = open('/var/www/html/openWB/ramdisk/bezuga3', 'w')
f.write(str(final))
f.close()

#Leistung EVU aus Kostal Plenticore lesen
#Wechselrichter bekommt Daten von Energy Manager EM300
#dazu Plenticore Register 252 lesen: Total_active_power_(powermeter) [W]
#Sensorposition 1 (Hausanschluss): (+)Hausverbrauch (-)Erzeugung
resp= client.read_holding_registers(252,2,unit=71)
FRegister = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Little)
final =int(FRegister.decode_32bit_float())

#PV Leistung
resp= client.read_holding_registers(100,2,unit=71)
FRegister = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Little)
pvwatt =int(FRegister.decode_32bit_float())
fpvwatt = pvwatt * -1

if ( int(sys.argv[2]) == 0):
    final = final - fpvwatt
else:
    final = final
f = open('/var/www/html/openWB/ramdisk/wattbezug', 'w')
f.write(str(final))
f.close()




