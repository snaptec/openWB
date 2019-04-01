#!/usr/bin/python
# coding: utf8

#########################################################
#
#liest aus Wechselrichter Kostal Plenticore
#mit angeschlossener Batterie die Lade-/Entladeleistung
#und den Batterie-SOC
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

#Plenticore Register 582 lesen: Actual_batt_ch_disch_power [W]
#{charge=negativ, discharge=positiv}
resp = client.read_holding_registers(582,1,unit=71)
FRegister = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Little)
battwatt = int(FRegister.decode_16bit_int())
f = open('/var/www/html/openWB/ramdisk/speicherleistung', 'w')
f.write(str(battwatt))
f.close()

#Plenticore Register 514 lesen: Battery_actual_SOC [%]
resp = client.read_holding_registers(514,1,unit=71)
FRegister = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Little)
battsoc = int(FRegister.decode_16bit_int())
f = open('/var/www/html/openWB/ramdisk/speichersoc', 'w')
f.write(str(battsoc))
f.close()
