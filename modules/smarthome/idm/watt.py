#!/usr/bin/python3
import sys
import os
import time
import json
import getopt
import socket
import struct
import codecs
import binascii
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.client.sync import ModbusTcpClient
named_tuple = time.localtime() # getstruct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S idm watty.py", named_tuple)
devicenumber=str(sys.argv[1])
ipadr=str(sys.argv[2])
uberschuss=int(sys.argv[3])
file_string= '/var/www/html/openWB/ramdisk/smarthome_device_' + str(devicenumber) + '_idm.log'
file_stringpv= '/var/www/html/openWB/ramdisk/smarthome_device_' + str(devicenumber) + '_pv'
file_stringcount= '/var/www/html/openWB/ramdisk/smarthome_device_' + str(devicenumber) + '_count'
file_stringcount5= '/var/www/html/openWB/ramdisk/smarthome_device_' + str(devicenumber) + '_count5'
count5 = 999
if os.path.isfile(file_stringcount5):
   f = open( file_stringcount5, 'r')
   count5 =int(f.read())
   f.close()
count5=count5+1
if count5 > 6:
   count5=0
f = open( file_stringcount5 , 'w')
f.write(str(count5))
f.close()
if count5==0:
   # pv modus
   pvmodus = 0
   if os.path.isfile(file_stringpv):
      f = open( file_stringpv , 'r')
      pvmodus =int(f.read())
      f.close()
   # log counter
   count1 = 999
   if os.path.isfile(file_stringcount):
      f = open( file_stringcount , 'r')
      count1 =int(f.read())
      f.close()
   count1=count1+1
   if count1 > 80:
      count1=0
   f = open( file_stringcount , 'w')
   f.write(str(count1))
   f.close()
   # aktuelle Leistung lesen
   client = ModbusTcpClient(ipadr, port=502)
   #start = 3524 
   start = 4122
   rr=client.read_input_registers(start,2,unit=1)
   raw = struct.pack('>HH', rr.getRegister(1), rr.getRegister(0))
   lkw= float(struct.unpack('>f', raw)[0])
   aktpower = int(lkw*1000)
   # logik nur schicken bei pvmodus
   modbuswrite = 0
   if pvmodus == 1:
      modbuswrite = 1
   # Nur positiven Uberschuss schicken, nicht aktuelle Leistung 
   neupower = uberschuss
   if neupower < 0:
      neupower = 0
   if neupower > 40000:
      neupower = 40000
   # wurde IDM gerade ausgeschaltet ?    (pvmodus == 99 ?)
   # dann 0 schicken wenn kein pvmodus mehr
   # und pv modus ausschalten
   if pvmodus == 99:
      modbuswrite = 1
      neupower = 0
      f = open( file_stringpv , 'w')
      pvmodus = 0
      f.write(str(pvmodus))
      f.close()
   lkwneu=float(neupower)
   lkwneu=lkwneu/1000
   builder = BinaryPayloadBuilder(byteorder=Endian.Big,wordorder=Endian.Little)
   builder.add_32bit_float( lkwneu )
   payload = builder.to_registers()
   regnew = builder.to_registers()
   #json return power = aktuelle Leistungsaufnahme in Watt, on = 1 pvmodus, powerc = counter in kwh
   powerc = 0
   answer = '{"power":' + str(aktpower) + ',"powerc":' + str(powerc) + ',"on":' + str(pvmodus) + '} '   
   f1 = open('/var/www/html/openWB/ramdisk/smarthome_device_ret' + str(devicenumber), 'w')
   json.dump(answer,f1)
   f1.close()
   #mehr log schreiben 
   if count1 < 3:
      if os.path.isfile(file_string):
         f = open( file_string , 'a')
      else:
         f = open( file_string , 'w')
      print ('%s devicenr %s ipadr %s ueberschuss (openWb) %6d Akt Leistung  %6d' % (time_string,devicenumber,ipadr,uberschuss,aktpower),file=f)
      print ('%s devicenr %s ipadr %s ueberschuss (IDM)    %6d pvmodus %1d modbuswrite %1d  ' % (time_string,devicenumber,ipadr,neupower,pvmodus,modbuswrite),file=f)
      f.close()
   # modbus write
   if modbuswrite == 1:
      client.write_registers(74, regnew, unit=1)
      if count1 < 3:
         f = open( file_string , 'a')
         print ('%s devicenr %s ipadr %s device written by modbus ' % (time_string,devicenumber,ipadr),file=f)
         f.close()