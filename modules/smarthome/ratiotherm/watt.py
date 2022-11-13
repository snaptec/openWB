#!/usr/bin/python3
import sys
import os
from pymodbus.payload import BinaryPayloadBuilder, Endian
from pymodbus.client.sync import ModbusTcpClient
import logging
from smarthome.smartlog import initlog
from smarthome.smartret import writeret
devicenumber = int(sys.argv[1])
ipadr = str(sys.argv[2])
uberschuss = int(sys.argv[3])
forcesend = int(sys.argv[4])
initlog("ratiotherm", devicenumber)
log = logging.getLogger("ratiotherm")
# forcesend = 0 default acthor time period applies
# forcesend = 1 default overwritten send now
# forcesend = 9 default overwritten no send
bp = '/var/www/html/openWB/ramdisk/smarthome_device_'
file_stringpv = bp + str(devicenumber) + '_pv'
file_stringcount = bp + str(devicenumber) + '_count'
file_stringcount5 = bp + str(devicenumber) + '_count5'
count5 = 999
modbuswrite = 0
neupower = 0
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
# pv modus
pvmodus = 0
if os.path.isfile(file_stringpv):
    with open(file_stringpv, 'r') as f:
        pvmodus = int(f.read())
aktpower = 0
if count5 == 0:
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
    # logik nur schicken bei pvmodus
    if pvmodus == 1:
        modbuswrite = 1
    neupower = uberschuss
    if neupower < 0:
        neupower = 0
    if neupower > 32767:
        neupower = 32767
    # wurde ratiotherm gerade ausgeschaltet ?    (pvmodus == 99 ?)
    # dann 0 schicken wenn kein pvmodus mehr
    # und pv modus ausschalten
    if pvmodus == 99:
        modbuswrite = 1
        neupower = 0
        pvmodus = 0
        with open(file_stringpv, 'w') as f:
            f.write(str(pvmodus))
    if count1 < 3:
        log.info(" watt devicenr %d ipadr %s ueberschuss %6d Akt Leistung  %6d"
                 % (devicenumber, ipadr, uberschuss, aktpower))
        log.info(" watt devicenr %d ipadr %s neupower %6d pvmodus %1d modbusw %1d"
                 % (devicenumber, ipadr, neupower, pvmodus, modbuswrite))
    # modbus write
    if modbuswrite == 1:
        # andernfalls absturz bei negativen Zahlen
        builder = BinaryPayloadBuilder(byteorder=Endian.Big)
        builder.reset()
        builder.add_16bit_int(neupower)
        pay = builder.to_registers()
        client = ModbusTcpClient(ipadr, port=502)
        client.write_register(100, pay[0], unit=1)
        if count1 < 3:
            log.info(" watt devicenr %d ipadr %s written %6d %#4X"
                     % (devicenumber, ipadr, pay[0], pay[0]))
else:
    if pvmodus == 99:
        pvmodus = 0
answer = '{"power":' + str(aktpower) + ',"powerc":0'
answer += ',"send":' + str(modbuswrite) + ',"sendpower":' + str(neupower)
answer += ',"on":' + str(pvmodus) + '}'
writeret(answer, devicenumber)
