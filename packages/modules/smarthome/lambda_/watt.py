#!/usr/bin/python3
import sys
import os
import time
import struct
import codecs
import logging
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.client.sync import ModbusTcpClient
from smarthome.smartlog import initlog
from smarthome.smartret import writeret
#  fix for pymodbus endian class (changes once 2023 august to enum to uppercases only,
#   checked during runtime,
#   not compatible betwwen openwb 1.9 (want lowercases) and openwb 2.0 (wants upercase))
auto = "@"
big = ">"
little = "<"
named_tuple = time.localtime()  # getstruct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S lambda watty.py", named_tuple)
devicenumber = int(sys.argv[1])
ipadr = str(sys.argv[2])
uberschuss = int(sys.argv[3])
uberschussvz = str(sys.argv[4])
forcesend = int(sys.argv[5])
pvwatt = int(sys.argv[6])
# forcesend = 0 default acthor time period applies
# forcesend = 1 default overwritten send now
# forcesend = 9 default overwritten no send
initlog("lambda", devicenumber)
log = logging.getLogger("lambda")
if (uberschussvz == 'UN'):
    uberschuss = uberschuss * -1
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
# aktuelle Leistung lesen
client = ModbusTcpClient(ipadr, port=502)
start = 103
resp = client.read_holding_registers(start, 2)
#
value1 = resp.registers[0]
all = format(value1, '04x')
aktpower = int(struct.unpack('>h', codecs.decode(all, 'hex'))[0])
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
    if (uberschussvz == 'UZ'):
        neupower = pvwatt
        if neupower < 0:
            neupower = 0
        if neupower > 65535:
            neupower = 65535
    else:
        if neupower < -32767:
            neupower = -32767
        if neupower > 32767:
            neupower = 32767
    # wurde lambda gerade ausgeschaltet ?    (pvmodus == 99 ?)
    # dann 0 schicken wenn kein pvmodus mehr
    # und pv modus ausschalten
    if pvmodus == 99:
        modbuswrite = 1
        neupower = 0
        pvmodus = 0
        with open(file_stringpv, 'w') as f:
            f.write(str(pvmodus))
    if count1 < 3:
        log.info(' %d ipadr %s ueberschuss %6d Akt Leistung %6d'
                 % (devicenumber, ipadr, uberschuss, aktpower))
        log.info(' %d ipadr %s neupower %6d pvmodus %1d modbusw %1d'
                 % (devicenumber, ipadr, neupower, pvmodus, modbuswrite))
    # modbus write
    if modbuswrite == 1:
        # andernfalls absturz bei negativen Zahlen
        builder = BinaryPayloadBuilder(byteorder=big)
        builder.reset()
        builder.add_16bit_int(neupower)
        pay = builder.to_registers()
        client.write_registers(102, [pay[0]])
        if count1 < 3:
            log.info(' %d ipadr %s written %6d %#4X' %
                     (devicenumber, ipadr, pay[0], pay[0]))
else:
    if pvmodus == 99:
        pvmodus = 0
answer = '{"power":' + str(aktpower) + ',"powerc":0'
answer += ',"send":' + str(modbuswrite) + ',"sendpower":' + str(neupower)
answer += ',"on":' + str(pvmodus) + '}'
writeret(answer, devicenumber)
