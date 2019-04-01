#!/usr/bin/python
# coding: utf8

#########################################################
#
#liest aus Wechselrichter Kostal Plenticore die
#PV-Leistung unter Beachtung Batterie falls vorhanden
#und die bisher kumulierte PV-Leistung
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

#PV-Leistung berechnen, kann nicht unmittelbar ausgelesen werden
#dazu Plenticore Register 100 lesen: Total_DC_power [W]
#Total_DC_power ist die gesamte DC-seitige Leistung, einschl. ggf.
#angeschlossener Batterie
resp= client.read_holding_registers(100,2,unit=71)
FRegister = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Little)
pvwatt =int(FRegister.decode_32bit_float())

#da ggf. Batterie DC-seitig in Total_DC_power enthalten ist,
#muss deren Lade-/Entladeleistung mitbetrachtet werden
#dazu Wert aus Ramdisk lesen
#resp = client.read_holding_registers(582,1,unit=71)
#FRegister = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Little)
#battwatt = int(FRegister.decode_16bit_int())
f = open('/var/www/html/openWB/ramdisk/speicherleistung', 'r')
battwatt = int(f.read())
f.close()

#PV-Leistung ist Total_DC_power - Actual_batt_ch_disch_power
#für weitere Berechnung/Anzeige mit neg. Vorzeichen
fpvwatt = (pvwatt + battwatt) * -1
f = open('/var/www/html/openWB/ramdisk/pvwatt', 'w')
f.write(str(fpvwatt))
f.close()

#PV Gesamt-Ertrag kwh
#dazu Plenticore Register 320 lesen: Total_yield [Wh]
resp= client.read_holding_registers(320,2,unit=71)
FRegister = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Little)
final =int(FRegister.decode_32bit_float())
#in Wattstunden
f = open('/var/www/html/openWB/ramdisk/pvkwh', 'w')
f.write(str(final))
f.close()
pvkwhk= final / 1000
#in Kilowattstunden
f = open('/var/www/html/openWB/ramdisk/pvkwhk', 'w')
f.write(str(pvkwhk))
f.close()
