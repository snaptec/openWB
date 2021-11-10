#!/usr/bin/python3
import sys
import os
import time
import json
import getopt
import socket
import struct
import codecs
from pymodbus.client.sync import ModbusTcpClient
named_tuple = time.localtime() # getstruct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S elwa watty.py", named_tuple)
devicenumber=str(sys.argv[1])
ipadr=str(sys.argv[2])
uberschuss=int(sys.argv[3])
file_string= '/var/www/html/openWB/ramdisk/smarthome_device_' + str(devicenumber) + '_elwa.log'
file_stringpv= '/var/www/html/openWB/ramdisk/smarthome_device_' + str(devicenumber) + '_pv'
file_stringcount= '/var/www/html/openWB/ramdisk/smarthome_device_' + str(devicenumber) + '_count'
file_stringcount5= '/var/www/html/openWB/ramdisk/smarthome_device_' + str(devicenumber) + '_count5'
powerc = 0
# pv modus
pvmodus = 0
if os.path.isfile(file_stringpv):
    f = open( file_stringpv , 'r')
    pvmodus =int(f.read())
    f.close()
# aktuelle Leistung lesen
client = ModbusTcpClient(ipadr, port=502)
#
start = 1000
resp=client.read_holding_registers(start,20,unit=1)
value1 = resp.registers[0]
all = format(value1, '04x')
aktpower= int(struct.unpack('>h',codecs.decode(all, 'hex'))[0])
count5 = 999
if os.path.isfile(file_stringcount5):
    f = open( file_stringcount5, 'r')
    count5 =int(f.read())
    f.close()
count5=count5+1
if count5 > 3:
    count5=0
f = open( file_stringcount5 , 'w')
f.write(str(count5))
f.close()
if count5==0:
    # log counter
    count1 = 999
    if os.path.isfile(file_stringcount):
        f = open( file_stringcount , 'r')
        count1 =int(f.read())
        f.close()
    count1=count1+1
    # status und fuse lesen
    value1 = resp.registers[3]
    all = format(value1, '04x')
    status= int(struct.unpack('>h',codecs.decode(all, 'hex') )[0])
    value1 = resp.registers[14]
    all = format(value1, '04x')
    fuse= int(struct.unpack('>h',codecs.decode(all, 'hex') )[0])
    # logik
    if fuse == 13:
        faktor = 1.2
    else:
        faktor = 1
    modbuswrite = 0
    # weiche Anpassung bei negativem ueberschuss
    if uberschuss < 0:
        neupower = aktpower + uberschuss
    else:
        neupower = int(uberschuss * faktor) + aktpower
    if neupower < 0:
        neupower = 0
    if neupower > 4000:
        neupower = 4000
    # status nach handbuch
    #
    #2 Heat
    #3 Standby
    #4 Boost heat
    #5 Heat finished
    #9 Setup
    #201 Error Overtemp Fuse blown
    #202 Error Overtemp measured
    #203 Error Overtemp Electronics
    #204 Error Hardware Fault
    #205 Error Temp Sensor
    # boost heat dran ?, nichts schicken
    if status == 4:
        neupower = 0
        modbuswrite = 0
    else:
    # solar heizen dran ?
        if status == 2:
    # dann 0 schicken wenn kein pvmodus mehr
            if pvmodus == 0:
                modbuswrite = 1
                neupower = 0
    # sonst wenn pv modus lauft , ueberschuss schicken
            else:
                modbuswrite = 1
    # wenn nicht solarheizen und nicht bost heat, auch ueberschuss schicken wenn pv modus lauft
        else:
            if pvmodus == 1:
                modbuswrite = 1
    #Sonst nichts schicken
    # test only faken aktpower
    #if pvmodus == 1:
    #   aktpower = neupower
    #else:
    #   aktpower = 0
    # test only
    #json return power = aktuelle Leistungsaufnahme in Watt, on = 1 pvmodus, powerc = counter in kwh
    #answer = '{"power":225,"on":0} '
    answer = '{"power":' + str(aktpower) + ',"powerc":' + str(powerc) + ',"on":' + str(pvmodus) + '} '
    f1 = open('/var/www/html/openWB/ramdisk/smarthome_device_ret' + str(devicenumber), 'w')
    json.dump(answer,f1)
    f1.close()
    # logschreiben
    if count1 > 80:
        count1=0
    #mehr log schreiben
    if count1 < 3:
        if os.path.isfile(file_string):
            f = open( file_string , 'a')
        else:
            f = open( file_string , 'w')
        print ('%s devicenr %s ipadr %s ueberschuss %6d Akt Leistung  %6d Status %2d' % (time_string,devicenumber,ipadr,uberschuss,aktpower,status),file=f)
        print ('%s devicenr %s ipadr %s Neu Leistung %6d pvmodus %1d modbuswrite %1d  ' % (time_string,devicenumber,ipadr,neupower,pvmodus,modbuswrite),file=f)
        f.close()
    f = open( file_stringcount , 'w')
    f.write(str(count1))
    f.close()
    # modbus write
    if modbuswrite == 1:
        rq = client.write_register(1000, neupower, unit=1)
        if count1 < 3:
            f = open( file_string , 'a')
            print ('%s devicenr %s ipadr %s device written by modbus ' % (time_string,devicenumber,ipadr),file=f)
            f.close()
else:
    answer = '{"power":' + str(aktpower) + ',"powerc":' + str(powerc) + ',"on":' + str(pvmodus) + '} '
    f1 = open('/var/www/html/openWB/ramdisk/smarthome_device_ret' + str(devicenumber), 'w')
    json.dump(answer,f1)
    f1.close()
