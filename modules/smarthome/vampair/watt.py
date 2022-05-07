#!/usr/bin/python3
import sys
import os
import time
import json
import struct
import codecs

from pymodbus.client.sync import ModbusTcpClient
named_tuple = time.localtime()  # getstruct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S vampair watty.py", named_tuple)
devicenumber = str(sys.argv[1])
ipadr = str(sys.argv[2])
uberschuss = int(sys.argv[3])
bp = '/var/www/html/openWB/ramdisk/smarthome_device_'
file_string = bp + str(devicenumber) + '_vampair.log'
file_stringpv = bp + str(devicenumber) + '_pv'
file_stringcount = bp + str(devicenumber) + '_count'
file_stringcount5 = bp + str(devicenumber) + '_count5'
count5 = 999
if os.path.isfile(file_stringcount5):
    with open(file_stringcount5, 'r') as f:
        count5 = int(f.read())
count5 = count5+1
if count5 > 6:
    count5 = 0
with open(file_stringcount5, 'w') as f:
    f.write(str(count5))
if count5 == 0:
    # pv modus
    pvmodus = 0
    if os.path.isfile(file_stringpv):
        with open(file_stringpv, 'r') as f:
            pvmodus = int(f.read())
    # log counter
    count1 = 999
    if os.path.isfile(file_stringcount):
        with open(file_stringcount, 'r') as f:
            count1 = int(f.read())
    count1 = count1+1
    if count1 > 80:
        count1 = 0
    with open(file_stringcount, 'w') as f:
        f.write(str(count1))
    # aktuelle Leistung lesen
    client = ModbusTcpClient(ipadr, port=502)
    start = 2322
    resp = client.read_input_registers(start, 2, unit=1)
    value1 = resp.registers[0]
    all = format(value1, '04x')
    aktpower = int(struct.unpack('>h', codecs.decode(all, 'hex'))[0])
    # logik nur schicken bei pvmodus
    modbuswrite = 0
    if pvmodus == 1:
        modbuswrite = 1
    neupower = uberschuss
    if neupower < -32767:
        neupower = -32767
    if neupower > 32767:
        neupower = 32767
    # wurde vampair gerade ausgeschaltet ?    (pvmodus == 99 ?)
    # dann 0 schicken wenn kein pvmodus mehr
    # und pv modus ausschalten
    if pvmodus == 99:
        modbuswrite = 1
        neupower = 0
        pvmodus = 0
        with open(file_stringpv, 'w') as f:
            f.write(str(pvmodus))
    # json return power = aktuelle Leistungsaufnahme in Watt,
    # on = 1 pvmodus, powerc = counter in kwh
    an = '{"power":' + str(aktpower) + ',"powerc":0,"on":' + str(pvmodus) + '}'
    with open('/var/www/html/openWB/ramdisk/smarthome_device_ret' +
              str(devicenumber), 'w') as f1:
        json.dump(an, f1)
    if count1 < 3:
        if os.path.isfile(file_string):
            pass
        else:
            with open(file_string, 'w') as f:
                print('vampair start log', file=f)
        with open(file_string, 'a') as f:
            print('%s Nr %s ipadr %s ueberschuss %6d Akt Leistung %6d'
                  % (time_string, devicenumber, ipadr, uberschuss, aktpower),
                  file=f)
            print('%s Nr %s ipadr %s ueberschuss %6d pvmodus %1d modbusw %1d'
                  % (time_string, devicenumber, ipadr, neupower, pvmodus,
                     modbuswrite), file=f)
    # modbus write
    if modbuswrite == 1:
        client.write_registers(33409, [neupower], unit=1)
        if count1 < 3:
            with open(file_string, 'a') as f:
                print('%s devicenr %s ipadr %s device written by modbus ' %
                      (time_string, devicenumber, ipadr), file=f)
