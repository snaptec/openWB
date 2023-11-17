#!/usr/bin/python3
import sys
import os
import struct
import logging
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.client.sync import ModbusTcpClient
from smarthome.smartlog import initlog
from smarthome.smartret import writeret
devicenumber = int(sys.argv[1])
ipadr = str(sys.argv[2])
uberschuss = int(sys.argv[3])
navvers = str(sys.argv[4])
pvwatt = int(sys.argv[5])
uberschussvz = str(sys.argv[6])
maxpower = int(sys.argv[7])
forcesend = int(sys.argv[8])
# forcesend = 0 default time period applies
# forcesend = 1 default overwritten send now
# forcesend = 9 default overwritten no send
initlog("idm", devicenumber)
log = logging.getLogger("idm")
bp = '/var/www/html/openWB/ramdisk/smarthome_device_'
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
if count5 > 6:
    count5 = 0
with open(file_stringcount5, 'w') as f:
    f.write(str(count5))
# aktuelle Leistung lesen
client = ModbusTcpClient(ipadr, port=502)
#  test
#  start = 3501
#  navvers = "2"
#  prod
start = 4122
if navvers == "2":
    rr = client.read_input_registers(start, 2, unit=1)
else:
    rr = client.read_holding_registers(start, 2, unit=1)
raw = struct.pack('>HH', rr.getRegister(1), rr.getRegister(0))
lkw = float(struct.unpack('>f', raw)[0])
aktpower = int(lkw*1000)
modbuswrite = 0
neupower = 0
# pv modus
pvmodus = 0
if os.path.isfile(file_stringpv):
    with open(file_stringpv, 'r') as f:
        pvmodus = int(f.read())
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
    # uberschuss begrenzung ?
    if (maxpower > 0):
        neupower = maxpower - aktpower
        # maximaler überschuss berechnet ?
        if (neupower > uberschuss):
            neupower = uberschuss
    if (uberschussvz == 'UZ'):
        # <option value="UP" data-option="UP">Überschuss als positive Zahl übertragen, Bezug negativ</option>
        # <option value="UZ" data-option="UZ">Überschuss als positive Zahl übertragen, Bezug als 0</option>
        if neupower < 0:
            neupower = 0
        if neupower > 65535:
            neupower = 65535
    else:
        if neupower < -32767:
            neupower = -32767
        if neupower > 32767:
            neupower = 32767
    # wurde IDM gerade ausgeschaltet ?    (pvmodus == 99 ?)
    # dann 0 schicken wenn kein pvmodus mehr
    # und pv modus ausschalten
    if pvmodus == 99:
        modbuswrite = 1
        neupower = 0
        pvmodus = 0
        pvwatt = 0
        with open(file_stringpv, 'w') as f:
            f.write(str(pvmodus))
    lkwneu = float(neupower)
    lkwneu = lkwneu/1000
    builder = BinaryPayloadBuilder(byteorder=Endian.Big,
                                   wordorder=Endian.Little)
    builder.add_32bit_float(lkwneu)
    regnew = builder.to_registers()
    pvw = float(pvwatt)
    pvw = pvw/1000
    builder = BinaryPayloadBuilder(byteorder=Endian.Big,
                                   wordorder=Endian.Little)
    builder.add_32bit_float(pvw)
    pvwnew = builder.to_registers()
    # json return power = aktuelle Leistungsaufnahme in Watt,
    # on = 1 pvmodus, powerc = counter in kwh
    if count1 < 3:
        log.info(" %d ipadr %s ueberschuss %6d Akt Leistung %6d Pv %6d"
                 % (devicenumber, ipadr, uberschuss, aktpower, pvwatt))
        log.info(" %d ipadr %s ueberschuss send %6d pvmodus %1d modbusw %1d"
                 % (devicenumber, ipadr, neupower, pvmodus, modbuswrite))
    # modbus write
    if modbuswrite == 1:
        client.write_registers(74, regnew, unit=1)
        if count1 < 3:
            log.info("devicenr %d ipadr %s device written by modbus " %
                     (devicenumber, ipadr))
    client.write_registers(78, pvwnew, unit=1)
else:
    if pvmodus == 99:
        pvmodus = 0
answer = '{"power":' + str(aktpower) + ',"powerc":0'
answer += ',"send":' + str(modbuswrite) + ',"sendpower":' + str(neupower)
answer += ',"on":' + str(pvmodus) + '}'
writeret(answer, devicenumber)
