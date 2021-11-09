#!/usr/bin/env python3
import math
import sys

from modules.common.modbus import ModbusClient, ModbusDataType

# Sunspec (API) documentation: https://www.solaredge.com/sites/default/files/sunspec-implementation-technical-note.pdf

ipaddress = str(sys.argv[1])
slave_ids = list(map(int, filter(lambda id: id.isnumeric(), sys.argv[2:6])))
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
    soc = client.read_holding_registers(62852, ModbusDataType.FLOAT_32, unit=slave_ids[0])
    try:
        if zweiterspeicher == 1:
            soc2 = client.read_holding_registers(62852, ModbusDataType.FLOAT_32, unit=slave_ids[1])
            fsoc=(soc+soc2)/2
        else:
            fsoc=soc
    except:
        fsoc=soc
    f = open('/var/www/html/openWB/ramdisk/speichersoc', 'w')
    f.write(str(fsoc))
    f.close()
    storagepower = client.read_holding_registers(62836, ModbusDataType.FLOAT_32, unit=slave_ids[0])
    try:
        if zweiterspeicher == 1:
            storage2power = client.read_holding_registers(62836, ModbusDataType.FLOAT_32, unit=slave_ids[1])
    except:
        storage2power = 0
    final=storagepower+storage2power
    f = open('/var/www/html/openWB/ramdisk/speicherleistung', 'w')
    f.write(str(final))
    f.close()

total_energy = 0
total_power = 0

for slave_id in slave_ids:
    # 40083 = AC Power value (Watt), 40084 = AC Power scale factor
    power_base, power_scale = client.read_holding_registers(40083, [ModbusDataType.INT_16] * 2, unit=slave_id)
    total_power -= power_base * math.pow(10, power_scale)
    # 40093 = AC Lifetime Energy production (Watt hours)
    total_energy += client.read_holding_registers(40093, ModbusDataType.INT_32, unit=slave_id)

if extprodakt == 1:
    try:
        # 40380 = "Meter 2/Total Real Power (sum of active phases)" (Watt)
        extprod = -client.read_holding_registers(40380, ModbusDataType.INT_16, unit=slave_ids[0])
    except:
        extprod = 0
else:
    extprod = 0
if subbat == 1:
    if storagepower > 0:
        storagepower=0
    if storage2power > 0:
        storage2power=0
    allwatt = total_power - storagepower - storage2power + extprod
else:
    allwatt = total_power - storagepower - storage2power + extprod
if allwatt > 0:
    allwatt=0
f = open('/var/www/html/openWB/ramdisk/pvwatt', 'w')
f.write(str(allwatt))
f.close()
f = open('/var/www/html/openWB/ramdisk/pvkwh', 'w')
f.write(str(total_energy))
f.close()
pvkwhk= total_energy / 1000
f = open('/var/www/html/openWB/ramdisk/pvkwhk', 'w')
f.write(str(pvkwhk))
f.close()
