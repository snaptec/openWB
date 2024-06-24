#!/usr/bin/python3
import sys
import os
import struct
import codecs
import logging
from pymodbus.client.sync import ModbusTcpClient
from smarthome.smartlog import initlog
from smarthome.smartret import writeret
bp = '/var/www/html/openWB/ramdisk/smarthome_device_'
devicenumber = int(sys.argv[1])
ipadr = str(sys.argv[2])
uberschuss = int(sys.argv[3])
atype = str(sys.argv[4])
instpower = int(sys.argv[5])
forcesend = int(sys.argv[6])
aktpoweralt = int(sys.argv[7])
measuretyp = str(sys.argv[8])
# forcesend = 0 default time period applies
# forcesend = 1 default overwritten send now
# forcesend = 9 default overwritten no send
initlog("acthor", devicenumber)
log = logging.getLogger("acthor")
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
faktor = 1.0
modbuswrite = 0
neupower = 0
if instpower == 0:
    instpower = 1000
cap = 9000
if atype == "9s45":
    faktor = 45000/instpower
    cap = 45000
elif atype == "9s27":
    faktor = 27000/instpower
    cap = 27000
elif atype == "9s18":
    faktor = 18000/instpower
    cap = 18000
elif atype == "9s":
    faktor = 9000/instpower
elif atype == "M3":
    faktor = 6000/instpower
elif atype == "E2M1":
    faktor = 3500/instpower
elif atype == "E2M3":
    faktor = 6500/instpower
else:
    faktor = 3000/instpower
pvmodus = 0
if os.path.isfile(file_stringpv):
    with open(file_stringpv, 'r') as f:
        pvmodus = int(f.read())
powerc = 0
# aktuelle Leistung lesen
client = ModbusTcpClient(ipadr, port=502)
#
start = 1000
resp = client.read_holding_registers(start, 35, unit=1)
# Test only
# start = 3524
# resp = client.read_input_registers(start, 35, unit=1)
value1 = resp.registers[0]
all = format(value1, '04x')
aktpower = int(struct.unpack('>h', codecs.decode(all, 'hex'))[0])
# sofern externe Messung wird dieser Wert genommen
if measuretyp == 'empty':
    aktpower = int(struct.unpack('>h', codecs.decode(all, 'hex'))[0])
else:
    aktpower = aktpoweralt
# Wassertemperatur lesen
# Temp0 Warmwasser 1001
# Temp1 1030 <- Optional wenn 0, nicht angeschlossen dann ersetzt durch 300 (keine Anzeige)
# Temp2 1031 <- Optional wenn 0, nicht angeschlossen dann ersetzt durch 300 (keine Anzeige)
# elwa2 hat nur zwei temp Fuehler
# nicht drei
value1 = resp.registers[1]
all = format(value1, '04x')
temp0int = int(struct.unpack('>h', codecs.decode(all, 'hex'))[0])
temp0 = temp0int / 10
value1 = resp.registers[30]
all = format(value1, '04x')
temp1int = int(struct.unpack('>h', codecs.decode(all, 'hex'))[0])
temp1 = temp1int / 10
if temp1 == 0:
    temp1 = 300
if (atype == "E2M3" or atype == "E2M1"):
    temp2 = 300.0
else:
    value1 = resp.registers[31]
    all = format(value1, '04x')
    temp2int = int(struct.unpack('>h', codecs.decode(all, 'hex'))[0])
    temp2 = temp2int / 10
if temp2 == 0:
    temp2 = 300
if count5 == 0:
    count1 = 999
    if os.path.isfile(file_stringcount):
        with open(file_stringcount, 'r') as f:
            count1 = int(f.read())
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
    if instpower > cap:
        cap = instpower
    if neupowertarget > int(cap * faktor):
        neupowertarget = int(cap * faktor)
    # status nach handbuch Thor/elwa2
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
        log.info(" watt devicenr %d ipadr %s ueberschuss %6d Akt Leistung  %6d Status %2d Externe Messung %s" %
                 (devicenumber, ipadr, uberschuss, aktpower, status, measuretyp))
        log.info(" watt devicenr %d ipadr %s Neu Leistung %6d pvmodus %1d modbuswrite %1d" %
                 (devicenumber, ipadr, neupower, pvmodus, modbuswrite))
        log.info(" watt devicenr %d ipadr %s type %s inst. Leistung %6d Skalierung %.2f" %
                 (devicenumber, ipadr, atype, instpower, faktor))
    # modbus write
    if modbuswrite == 1:
        rq = client.write_register(1000, neupower, unit=1)
        if count1 < 3:
            log.info("watt devicenr %d ipadr %s device written by modbus " %
                     (devicenumber, ipadr))
else:
    if pvmodus == 99:
        pvmodus = 0
answer = '{"power":' + str(aktpower) + ',"powerc":' + str(powerc)
answer += ',"send":' + str(modbuswrite) + ',"sendpower":' + str(neupower)
answer += ',"temp0":' + str(temp0)
answer += ',"temp1":' + str(temp1)
answer += ',"temp2":' + str(temp2)
answer += ',"on":' + str(pvmodus) + '}'
writeret(answer, devicenumber)
