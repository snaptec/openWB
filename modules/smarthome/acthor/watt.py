#!/usr/bin/python3
import sys
import os
import time
import json
import struct
import codecs
from pymodbus.client.sync import ModbusTcpClient
named_tuple = time.localtime()   # getstruct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S acthor watty.py", named_tuple)
devicenumber = str(sys.argv[1])
ipadr = str(sys.argv[2])
uberschuss = int(sys.argv[3])
atype = str(sys.argv[4])
instpower = int(sys.argv[5])
forcesend = int(sys.argv[6])
# forcesend = 0 default acthor time period applies
# forcesend = 1 default overwritten send now
# forcesend = 9 default overwritten no send
fp = '/var/www/html/openWB/ramdisk/smarthome_device_'
file_string = fp + str(devicenumber) + '_acthor.log'
file_stringpv = fp + str(devicenumber) + '_pv'
file_stringcount = fp + str(devicenumber) + '_count'
file_stringcount5 = fp + str(devicenumber) + '_count5'
count5 = 999
if os.path.isfile(file_stringcount5):
    f = open(file_stringcount5, 'r')
    count5 = int(f.read())
    f.close()
if (forcesend == 0):
    count5 = count5 + 1
elif (forcesend == 1):
    count5 = 999
else:
    count5 = 1
if count5 > 3:
    count5 = 0
f = open(file_stringcount5, 'w')
f.write(str(count5))
f.close()
faktor = 1.0
modbuswrite = 0
neupower = 0
if instpower == 0:
    instpower = 1000
cap = 9000
if atype == "9s18":
    faktor = 18000/instpower
    cap = 18000
elif atype == "9s":
    faktor = 9000/instpower
elif atype == "M3":
    faktor = 6000/instpower
else:
    faktor = 3000/instpower
pvmodus = 0
if os.path.isfile(file_stringpv):
    f = open(file_stringpv, 'r')
    pvmodus = int(f.read())
    f.close()
powerc = 0
# aktuelle Leistung lesen
client = ModbusTcpClient(ipadr, port=502)
#
#
start = 1000
resp=client.read_holding_registers(start,10,unit=1)
# start = 3524
# resp = client.read_input_registers(start, 10, unit=1)
value1 = resp.registers[0]
all = format(value1, '04x')
aktpower = int(struct.unpack('>h', codecs.decode(all, 'hex'))[0])
if count5 == 0:
    count1 = 999
    if os.path.isfile(file_stringcount):
        f = open(file_stringcount, 'r')
        count1 = int(f.read())
        f.close()
    count1 = count1+1
    value1 = resp.registers[3]
    all = format(value1, '04x')
    status = int(struct.unpack('>h', codecs.decode(all, 'hex'))[0])
    # logik
    if uberschuss < 0:
        neupowertarget = int((uberschuss + aktpower) * faktor)
    else:
        neupowertarget = int((uberschuss + aktpower) * faktor)
    if neupowertarget < 0:
        neupowertarget = 0
    if neupowertarget > int(cap * faktor):
        neupowertarget = int(cap * faktor)
    # status nach handbuch Thor
    # 0.. Aus
    # 1-8 Geraetestart
    # 9 Betrieb
    # >=200 Fehlerzustand Leistungsteil
    neupower = neupowertarget
    # wurde Thor gerade ausgeschaltet ?    (pvmodus == 99 ?)
    # dann 0 schicken wenn kein pvmodus mehr
    # und pv modus ausschalten
    if pvmodus == 99:
        modbuswrite = 1
        neupower = 0
        f = open(file_stringpv, 'w')
        pvmodus = 0
        f.write(str(pvmodus))
        f.close()
    # sonst wenn pv modus lauft , ueberschuss schicken
    else:
        if pvmodus == 1:
            modbuswrite = 1
    # logschreiben
    if count1 > 80:
        count1 = 0
    if count1 < 3:
        if os.path.isfile(file_string):
            f = open(file_string, 'a')
        else:
            f = open(file_string, 'w')
        helpstr = '%s devicenr %s ipadr %s ueberschuss %6d Akt Leistung'
        helpstr += ' %6d Status %2d type %s inst. Leistung %6d Skalierung %.2f'
        print(helpstr % (time_string, devicenumber, ipadr, uberschuss,
                         aktpower, status, atype, instpower, faktor), file=f)
        helpstr = '%s devicenr %s ipadr %s Neu Leistung %6d '
        helpstr += 'pvmodus %1d modbuswrite %1d'
        print(helpstr % (time_string, devicenumber, ipadr, neupower,
                         pvmodus, modbuswrite), file=f)
        f.close()
    # modbus write
    if modbuswrite == 1:
        rq = client.write_register(1000, neupower, unit=1)
        if count1 < 3:
            f = open(file_string, 'a')
            print('%s devicenr %s ipadr %s device written by modbus ' %
                  (time_string, devicenumber, ipadr), file=f)
            f.close()
    f = open(file_stringcount, 'w')
    f.write(str(count1))
    f.close()
else:
    if pvmodus == 99:
        pvmodus = 0
answer = '{"power":' + str(aktpower) + ',"powerc":' + str(powerc)
answer += ',"send":' + str(modbuswrite) + ',"sendpower":' + str(neupower)
answer += ',"on":' + str(pvmodus) + '}'
f1 = open('/var/www/html/openWB/ramdisk/smarthome_device_ret' +
          str(devicenumber), 'w')
json.dump(answer, f1)
f1.close()
