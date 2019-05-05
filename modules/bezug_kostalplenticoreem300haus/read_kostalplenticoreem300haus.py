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
#Plenticore Register 222: Current_phase_1_(powermeter) [A]
reg_222 = client.read_holding_registers(222,2,unit=71)
#Phase 2
#Plenticore Register 232: Current_phase_2_(powermeter) [A]
reg_232 = client.read_holding_registers(232,2,unit=71)
#Phase 3
#Plenticore Register 242: Current_phase_3_(powermeter) [A]
reg_242 = client.read_holding_registers(242,2,unit=71)
#Leistung EVU
#Plenticore Register 252: Total_active_power_(powermeter) [W]
#Sensorposition 1 (Hausanschluss): (+)Hausverbrauch (-)Erzeugung
reg_252 = client.read_holding_registers(252,2,unit=71)

#ausgelesene Register dekodieren
FRegister_222 = BinaryPayloadDecoder.fromRegisters(reg_222.registers, byteorder=Endian.Big, wordorder=Endian.Little)
FRegister_232 = BinaryPayloadDecoder.fromRegisters(reg_232.registers, byteorder=Endian.Big, wordorder=Endian.Little)
FRegister_242 = BinaryPayloadDecoder.fromRegisters(reg_242.registers, byteorder=Endian.Big, wordorder=Endian.Little)
FRegister_252 = BinaryPayloadDecoder.fromRegisters(reg_252.registers, byteorder=Endian.Big, wordorder=Endian.Little)

#dekodierte Register in entsprechende Typen umwandeln
Current_phase_1_powermeter = round(FRegister_222.decode_32bit_float(),2)
Current_phase_2_powermeter = round(FRegister_232.decode_32bit_float(),2)
Current_phase_3_powermeter = round(FRegister_242.decode_32bit_float(),2)
Total_active_power_powermeter = int(FRegister_252.decode_32bit_float())

#PV Leistung wurde schon im Modul Wechselrichter bestimmt, hier aus ramdisk lesen
#with open('/var/www/html/openWB/ramdisk/pvwatt', 'r') as f:
#    f.read(int(PV_power_ac))
#//TODO: Lesen funktioniert so nicht, da String in ramdisk

#Bezug berechnen je nach Position des Energy Managers
Bezug = Total_active_power_powermeter

#//TODO: Subtraktion funktioniert nicht wegen fehlendem Wert aus ramdisk oben
#if int(sys.argv[2]) == 0:
#    Bezug = Bezug - PV_power_ac

#und zur Weiterverarbeitung alle Werte in die ramdisk
with open('/var/www/html/openWB/ramdisk/wattbezug', 'w') as f:
    f.write(str(Bezug))
with open('/var/www/html/openWB/ramdisk/bezuga1', 'w') as f:
    f.write(str(Current_phase_1_powermeter))
with open('/var/www/html/openWB/ramdisk/bezuga2', 'w') as f:
    f.write(str(Current_phase_2_powermeter))
with open('/var/www/html/openWB/ramdisk/bezuga3', 'w') as f:
    f.write(str(Current_phase_3_powermeter))
