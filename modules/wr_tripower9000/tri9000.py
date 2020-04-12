#!/usr/bin/python
import sys
from smadash import SMADASH
from modbuswr import ModbusWR
import openWBlib
import re

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





