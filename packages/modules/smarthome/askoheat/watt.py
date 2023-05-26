#!/usr/bin/python3
import sys
import os
import struct
import codecs
from pymodbus.client.sync import ModbusTcpClient
import logging
from smarthome.smartlog import initlog
from smarthome.smartret import writeret
devicenumber = int(sys.argv[1])
ipadr = str(sys.argv[2])
uberschuss = int(sys.argv[3])
forcesend = int(sys.argv[4])
# forcesend = 0 default time period applies
# forcesend = 1 default overwritten send now
# forcesend = 9 default overwritten no send
initlog("askoheat", devicenumber)
log = logging.getLogger("askoheat")
bp = '/var/www/html/openWB/ramdisk/smarthome_device_'
file_stringpv = bp + str(devicenumber) + '_pv'
file_stringcount = bp + str(devicenumber) + '_count'
file_stringcount5 = bp + str(devicenumber) + '_count5'
# pv modus
pvmodus = 0
modbuswrite = 0
neupower = 0
if os.path.isfile(file_stringpv):
    with open(file_stringpv, 'r') as f:
        pvmodus = int(f.read())
# aktuelle Leistung lesen
client = ModbusTcpClient(ipadr, port=502)
start = 110
# test
# start = 3522
resp = client.read_input_registers(start, 1, unit=1)
value1 = resp.registers[0]
all = format(value1, '04x')
aktpower = int(struct.unpack('>h', codecs.decode(all, 'hex'))[0])
# Wassertemperatur lesen
start = 638
#  test
# start = 3522
resp = client.read_input_registers(start, 1, unit=1)
value1 = resp.registers[0]
all = format(value1, '04x')
temp0 = int(struct.unpack('>h', codecs.decode(all, 'hex'))[0])
if temp0 == 0:
    temp0 = 300
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
if count5 == 0:
    # log counter
    count1 = 999
    if os.path.isfile(file_stringcount):
        with open(file_stringcount, 'r') as f:
            count1 = int(f.read())
    count1 = count1+1
    neupower = aktpower + uberschuss
    if neupower < 0:
        neupower = 0
    if neupower > 30000:
        neupower = 30000
    if pvmodus == 99:
        modbuswrite = 1
        neupower = 0
        pvmodus = 0
        with open(file_stringpv, 'w') as f:
            f.write(str(pvmodus))
    # sonst wenn pv modus lauft , ueberschuss schicken
    else:
        if pvmodus == 1:
            modbuswrite = 1
    # logschreiben
    if count1 > 80:
        count1 = 0
    with open(file_stringcount, 'w') as f:
        f.write(str(count1))
    # mehr log schreiben
    if count1 < 3:
        log.info(" watt devicenr %d ipadr %s ueberschuss %6d Akt Leistung  %6d " %
                 (devicenumber, ipadr, uberschuss, aktpower))
        log.info(" watt devicenr %d ipadr %s Neu Leistung %6d pvmodus %1d modbuswrite %1d" %
                 (devicenumber, ipadr, neupower, pvmodus, modbuswrite))
    # modbus write
    if modbuswrite == 1:
        rq = client.write_register(201, neupower, unit=1)
        if count1 < 3:
            log.info("watt devicenr %d ipadr %s device written by modbus " %
                     (devicenumber, ipadr))
answer = '{"power":' + str(aktpower) + ',"powerc":0'
answer += ',"send":' + str(modbuswrite) + ',"sendpower":' + str(neupower)
answer += ',"on":' + str(pvmodus) + ',"temp0":' + str(temp0) + '}'
writeret(answer, devicenumber)
