#!/usr/bin/python

#####
#
# File: tri9000.py
#
# Copyright 2020 Kevin Wieland, Holger Lamm
#
#  This file is part of openWB.
#
#     openWB is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     openWB is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with openWB.  If not, see <https://www.gnu.org/licenses/>.
#
#####

import sys
from smadash import SMADASH
from modbuswr import ModbusWR
import openWBlib

ramdisk = '/var/www/html/openWB/ramdisk/'
wrs = []

def GetWR(host, typ):
   if typ == "modbus":
      instance = ModbusWR(host)
   else:  # if typ == "dash":
      instance = SMADASH(host)
   return instance

config = openWBlib.openWBconfig()
settings = [ 'tri9000ip', 'wrsma2ip', 'wrsma3ip', 'wrsma4ip']

for nameconf in settings:
   wrtype = config[nameconf]
   wrconnect = 'modbus'
   if wrtype is None: wrtype = "none"
   if wrtype.find('@') > 0:
      wrtype, wrconnect = wrtype.split('@')
   if wrtype != "none":
      try:
         wrs.append(GetWR(wrtype, wrconnect).read())
      except Exception as e:
         openWBlib.log("Error connecting to SMA inverter " + wrtype + ": " + str(e)) 

totalpower, totalgeneration = 0,0
index = 1
for w,g in wrs:
   totalpower += w
   totalgeneration += g
   with open(ramdisk + 'pvwatt%i' % index, 'w') as f:
     f.write(str(w))
   with open(ramdisk + 'pvkwhk%i' % index, 'w') as f:
     f.write(str(g))
   index += 1
   
with open(ramdisk + 'pvwatt', 'w') as f:
    f.write(str(totalpower))
with open(ramdisk + 'pvkwh', 'w') as f:
    f.write(str(totalgeneration))
