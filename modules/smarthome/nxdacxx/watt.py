#!/usr/bin/python3
import sys
import os
import time
import json
from pymodbus.client.sync import ModbusTcpClient
named_tuple = time.localtime()   # getstruct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S N4DAC02 watty.py", named_tuple)
devicenumber = str(sys.argv[1])
ipadr = str(sys.argv[2])
uberschuss = int(sys.argv[3])
maxpower = int(sys.argv[4])
forcesend = int(sys.argv[5])
# forcesend = 0 default acthor time period applies
# forcesend = 1 default overwritten send now
# forcesend = 9 default overwritten no send
bp = '/var/www/html/openWB/ramdisk/smarthome_device_'
file_string = bp + str(devicenumber) + '_N4DAC02.log'
file_stringpv = bp + str(devicenumber) + '_pv'
file_stringcount = bp + str(devicenumber) + '_count'
file_stringcount5 = bp + str(devicenumber) + '_count5'
count5 = 999
if os.path.isfile(file_stringcount5):
    with open(file_stringcount5, 'r') as f:
        count5 = int(f.read())
if (forcesend == 0):
    count5 = count5 + 1
elif (forcesend == 1):
    count5 = 999
else:
    count5 = 1
if count5 > 3:
    count5 = 0
with open(file_stringcount5, 'w') as f:
    f.write(str(count5))
modbuswrite = 0
neupower = uberschuss
if neupower < 0:
    neupower = 0
if neupower > maxpower:
    neupower = maxpower
volt = 0
pvmodus = 0
if os.path.isfile(file_stringpv):
    with open(file_stringpv, 'r') as f:
        pvmodus = int(f.read())
powerc = 0
aktpower = 0
if count5 == 0:
    count1 = 999
    if os.path.isfile(file_stringcount):
        with open(file_stringcount, 'r') as f:
            count1 = int(f.read())
    count1 = count1+1
    # wurde  gerade ausgeschaltet ?    (pvmodus == 99 ?)
    # dann 0 schicken wenn kein pvmodus mehr
    # und pv modus ausschalten
    if pvmodus == 99:
        modbuswrite = 1
        pvmodus = 0
        neupower = 0
        with open(file_stringpv, 'w') as f:
            f.write(str(pvmodus))
    # sonst wenn pv modus lauft , ueberschuss schicken
    else:
        if pvmodus == 1:
            modbuswrite = 1
    # logschreiben
    if count1 > 80:
        count1 = 0
    if count1 < 3:
        if os.path.isfile(file_string):
            pass
        else:
            with open(file_string, 'w') as f:
                print('N4DAC02 start log', file=f)
        with open(file_string, 'a') as f:
            helpstr = '%s devicenr %s ipadr %s ueberschuss %6d '
            helpstr += ' maxueberschuss %6d pvmodus %1d modbuswrite %1d'
            print(helpstr % (time_string, devicenumber, ipadr, uberschuss,
                             maxpower, pvmodus, modbuswrite), file=f)
    # modbus write
    if modbuswrite == 1:
        client = ModbusTcpClient(ipadr, port=502)
        volt = int((neupower * 1000) / maxpower)
        rq = client.write_register(1, volt)
        # oder
        # rq = client.write_register(1, volt, unit = 1)
        if count1 < 3:
            with open(file_string, 'a') as f:
                print('%s devicenr %s ipadr %s Volt %6d written by modbus ' %
                      (time_string, devicenumber, ipadr, volt), file=f)
    with open(file_stringcount, 'w') as f:
        f.write(str(count1))
else:
    if pvmodus == 99:
        pvmodus = 0
answer = '{"power":' + str(aktpower) + ',"powerc":' + str(powerc)
answer += ',"send":' + str(modbuswrite) + ',"sendpower":' + str(volt)
answer += ',"on":' + str(pvmodus) + '}'
with open('/var/www/html/openWB/ramdisk/smarthome_device_ret' +
          str(devicenumber), 'w') as f1:
    json.dump(answer, f1)
