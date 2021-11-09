#!/usr/bin/env python3
import math
import sys

from modules.common.modbus import ModbusClient, ModbusDataType

# Sunspec (API) documentation: https://www.solaredge.com/sites/default/files/sunspec-implementation-technical-note.pdf


ipaddress = str(sys.argv[1])
try:
    slave1id = int(sys.argv[2])
except:
    slave1id=0
try:
    slave2id = int(sys.argv[3])
except:
    slave2id=0
try:
    slave3id = int(sys.argv[4])
except:
    slave3id=0
try:
    slave4id = int(sys.argv[5])
except:
    slave4id=0
batwrsame = int(sys.argv[6])
extprodakt = int(sys.argv[7])
zweiterspeicher = int(sys.argv[8])
subbat = int(sys.argv[9])

storage2power = 0

client = ModbusClient(ipaddress)

# batterie auslesen und pv leistung korrigieren
storagepower = 0
storage2power = 0
if batwrsame == 1:
    soc = client.read_holding_registers(62852, ModbusDataType.FLOAT_32, unit=slave1id)
    try:
        if zweiterspeicher == 1:
            soc2 = client.read_holding_registers(62852, ModbusDataType.FLOAT_32, unit=slave2id)
            fsoc=(soc+soc2)/2
        else:
            fsoc=soc
    except:
        fsoc=soc
    f = open('/var/www/html/openWB/ramdisk/speichersoc', 'w')
    f.write(str(fsoc))
    f.close()
    storagepower = client.read_holding_registers(62836, ModbusDataType.FLOAT_32, unit=slave1id)
    try:
        if zweiterspeicher == 1:
            storage2power = client.read_holding_registers(62836, ModbusDataType.FLOAT_32, unit=slave2id)
    except:
        storage2power = 0
    final=storagepower+storage2power
    f = open('/var/www/html/openWB/ramdisk/speicherleistung', 'w')
    f.write(str(final))
    f.close()

try:
    # 40083 = AC Power value (Watt), 40084 = AC Power scale factor
    power_base, power_scale = client.read_holding_registers(40083, [ModbusDataType.INT_16] * 2, unit=slave1id)
    fwr1watt = -power_base * math.pow(10, power_scale)
    # 40093 = AC Lifetime Energy production (Watt hours)
    final = client.read_holding_registers(40093, ModbusDataType.INT_32, unit=slave1id)
except:
    fwr1watt=0
if slave2id != 0:
    try:
        power_base, power_scale = client.read_holding_registers(40083, [ModbusDataType.INT_16] * 2, unit=slave2id)
        fwr2watt = -power_base * math.pow(10, power_scale)
        final += client.read_holding_registers(40093, ModbusDataType.INT_32, unit=slave2id)
    except:
        fwr2watt=0
else:
    fwr2watt=0
if slave3id != 0:
    try:
        power_base, power_scale = client.read_holding_registers(40083, [ModbusDataType.INT_16] * 2, unit=slave3id)
        fwr2watt = -power_base * math.pow(10, power_scale)
        final += client.read_holding_registers(40093, ModbusDataType.INT_32, unit=slave3id)
    except:
        fwr3watt=0
else:
    fwr3watt=0
if slave4id != 0:
    try:
        power_base, power_scale = client.read_holding_registers(40083, [ModbusDataType.INT_16] * 2, unit=slave4id)
        fwr2watt = -power_base * math.pow(10, power_scale)
        final += client.read_holding_registers(40093, ModbusDataType.INT_32, unit=slave4id)
    except:
        fwr4watt=0
else:
    fwr4watt=0

if extprodakt == 1:
    try:
        # 40380 = "Meter 2/Total Real Power (sum of active phases)" (Watt)
        extprod = -client.read_holding_registers(40380, ModbusDataType.INT_16, unit=slave1id)
    except:
        extprod = 0
else:
    extprod = 0
if subbat == 1:
    if storagepower > 0:
        storagepower=0
    if storage2power > 0:
        storage2power=0
    allwatt=fwr1watt+fwr2watt+fwr3watt+fwr4watt-storagepower-storage2power+extprod
else:
    allwatt=fwr1watt+fwr2watt+fwr3watt+fwr4watt-storagepower-storage2power+extprod
if allwatt > 0:
    allwatt=0
f = open('/var/www/html/openWB/ramdisk/pvwatt', 'w')
f.write(str(allwatt))
f.close()
f = open('/var/www/html/openWB/ramdisk/pvkwh', 'w')
f.write(str(final))
f.close()
pvkwhk= final / 1000
f = open('/var/www/html/openWB/ramdisk/pvkwhk', 'w')
f.write(str(pvkwhk))
f.close()
