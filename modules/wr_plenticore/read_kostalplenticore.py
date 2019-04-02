#!/usr/bin/python
# coding: utf8

#########################################################
#
#liest aus Wechselrichter Kostal Plenticore Register
#zu PV-Statistik und berechnet PV-Leistung unter
#Beachtung angeschlossener Batterie falls vorhanden
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

#Plenticore als Modbus Client einrichhten
client = ModbusTcpClient(ipaddress, port=1502)

#dann erst alle relevanten Register auslesen:

#Plenticore Register 100: Total_DC_power [W]
#ist die gesamte DC-seitige Leistung, einschl. ggf.
#angeschlossener Batterie
reg_100 = client.read_holding_registers(100,2,unit=71)
#Plenticore Register 582: Actual_batt_ch_disch_power [W]
##ist Lade-/Entladeleistung des angeschlossenen Speichers
#{charge=negativ, discharge=positiv}
reg_582 = client.read_holding_registers(582,1,unit=71)
#Plenticore Register 320: Total_yield [Wh]
#PV Gesamt-Ertrag
reg_320 = client.read_holding_registers(320,2,unit=71)
#//TODO: weitere Register später hinzufügen für PV-Statistik
#

#ausgelesene Register dekodieren
FRegister_100 = BinaryPayloadDecoder.fromRegisters(reg_100.registers, byteorder=Endian.Big, wordorder=Endian.Little)
FRegister_582 = BinaryPayloadDecoder.fromRegisters(reg_582.registers, byteorder=Endian.Big, wordorder=Endian.Little)
FRegister_320 = BinaryPayloadDecoder.fromRegisters(reg_320.registers, byteorder=Endian.Big, wordorder=Endian.Little)

#dekodierte Register in entsprechende Typen umwandeln
Total_DC_power = int(FRegister_100.decode_32bit_float())
Actual_batt_ch_disch_power = int(FRegister_582.decode_16bit_int())
Total_yield = int(FRegister_320.decode_32bit_float())

#da ggf. Batterie DC-seitig in Total_DC_power enthalten ist,
#muss deren Lade-/Entladeleistung mitbetrachtet werden
PV_power = (Total_DC_power + Actual_batt_ch_disch_power) * -1

#und zur Weiterverarbeitung Werte in die ramdisk
with open('/var/www/html/openWB/ramdisk/pvwatt', 'w') as f:
    f.write(str(PV_power))
#in Wattstunden
with open('/var/www/html/openWB/ramdisk/pvkwh', 'w') as f:
    f.write(str(Total_yield))
#in Kilowattstunden
with open('/var/www/html/openWB/ramdisk/pvkwhk', 'w') as f:
    f.write(str(Total_yield / 1000))
