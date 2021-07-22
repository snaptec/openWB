#!/usr/bin/python
import sys
# import os
# import time
# import getopt
# import socket
# import ConfigParser
import struct
# import binascii
from pymodbus.client.sync import ModbusTcpClient

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

client = ModbusTcpClient(ipaddress, port=502)

# batterie auslesen und pv leistung korrigieren
storagepower = 0
storage2power = 0
if batwrsame == 1:
    rr = client.read_holding_registers(62852, 2, unit=slave1id)
    raw = struct.pack('>HH', rr.getRegister(1), rr.getRegister(0))
    soc = int(struct.unpack('>f', raw)[0])
    try:
        if zweiterspeicher == 1:
            rr = client.read_holding_registers(62852, 2, unit=slave2id)
            raw = struct.pack('>HH', rr.getRegister(1), rr.getRegister(0))
            soc2 = int(struct.unpack('>f', raw)[0])
            fsoc=(soc+soc2)/2
        else:
            fsoc=soc
    except:
        fsoc=soc
    f = open('/var/www/html/openWB/ramdisk/speichersoc', 'w')
    f.write(str(fsoc))
    f.close()
    rr = client.read_holding_registers(62836, 2, unit=slave1id)
    raw = struct.pack('>HH', rr.getRegister(1), rr.getRegister(0))
    storagepower = int(struct.unpack('>f', raw)[0])
    try:
        if zweiterspeicher == 1:
            rr = client.read_holding_registers(62836, 2, unit=slave2id)
            raw = struct.pack('>HH', rr.getRegister(1), rr.getRegister(0))
            storage2power = int(struct.unpack('>f', raw)[0])
    except:
        storage2power = 0
    final=storagepower+storage2power
    f = open('/var/www/html/openWB/ramdisk/speicherleistung', 'w')
    f.write(str(final))
    f.close()

try:
    resp= client.read_holding_registers(40083,2,unit=slave1id)
    # read watt
    watt=format(resp.registers[0], '04x')
    wr1watt=int(struct.unpack('>h', watt.decode('hex'))[0]) * -1
    # read multiplier
    multiplier=format(resp.registers[1], '04x')
    fmultiplier=int(struct.unpack('>h', multiplier.decode('hex'))[0])
    if fmultiplier == 2:
        fwr1watt = wr1watt * 100
    if fmultiplier == 1:
        fwr1watt = wr1watt * 10
    if fmultiplier == 0:
        fwr1watt = wr1watt
    if fmultiplier == -1:
        fwr1watt = wr1watt / 10
    if fmultiplier == -2:
        fwr1watt = wr1watt / 100
    if fmultiplier == -3:
        fwr1watt = wr1watt / 1000
    if fmultiplier == -4:
        fwr1watt = wr1watt / 10000
    if fmultiplier == -5:
        fwr1watt = wr1watt / 10000
    resp= client.read_holding_registers(40093,2,unit=slave1id)
    value1 = resp.registers[0]
    value2 = resp.registers[1]
    all = format(value1, '04x') + format(value2, '04x')
    final = int(struct.unpack('>i', all.decode('hex'))[0])
except:
    fwr1watt=0
if slave2id != 0:
    try:
        resp= client.read_holding_registers(40083,2,unit=slave2id)
        # read watt
        watt=format(resp.registers[0], '04x')
        wr2watt=int(struct.unpack('>h', watt.decode('hex'))[0]) * -1
        # read multiplier
        multiplier=format(resp.registers[1], '04x')
        fmultiplier=int(struct.unpack('>h', multiplier.decode('hex'))[0])
        if fmultiplier == 2:
            fwr2watt = wr2watt * 100
        if fmultiplier == 1:
            fwr2watt = wr2watt * 10
        if fmultiplier == 0:
            fwr2watt = wr2watt
        if fmultiplier == -1:
            fwr2watt = wr2watt / 10
        if fmultiplier == -2:
            fwr2watt = wr2watt / 100
        if fmultiplier == -3:
            fwr2watt = wr2watt / 1000
        if fmultiplier == -4:
            fwr2watt = wr2watt / 10000
        if fmultiplier == -5:
            fwr2watt = wr2watt / 10000
        resp= client.read_holding_registers(40093,2,unit=slave2id)
        value1 = resp.registers[0]
        value2 = resp.registers[1]
        all = format(value1, '04x') + format(value2, '04x')
        final = final + int(struct.unpack('>i', all.decode('hex'))[0])
    except:
        fwr2watt=0
else:
    fwr2watt=0
if slave3id != 0:
    try:
        resp= client.read_holding_registers(40083,2,unit=slave3id)
        # read watt
        watt=format(resp.registers[0], '04x')
        wr3watt=int(struct.unpack('>h', watt.decode('hex'))[0]) * -1
        # read multiplier
        multiplier=format(resp.registers[1], '04x')
        fmultiplier=int(struct.unpack('>h', multiplier.decode('hex'))[0])
        if fmultiplier == 2:
            fwr3watt = wr3watt * 100
        if fmultiplier == 1:
            fwr3watt = wr3watt * 10
        if fmultiplier == 0:
            fwr3watt = wr3watt
        if fmultiplier == -1:
            fwr3watt = wr3watt / 10
        if fmultiplier == -2:
            fwr3watt = wr3watt / 100
        if fmultiplier == -3:
            fwr3watt = wr3watt / 1000
        if fmultiplier == -4:
            fwr3watt = wr3watt / 10000
        if fmultiplier == -5:
            fwr3watt = wr3watt / 10000
        resp= client.read_holding_registers(40093,2,unit=slave3id)
        value1 = resp.registers[0]
        value2 = resp.registers[1]
        all = format(value1, '04x') + format(value2, '04x')
        final = final + int(struct.unpack('>i', all.decode('hex'))[0])
    except:
        fwr3watt=0
else:
    fwr3watt=0
if slave4id != 0:
    try:
        resp= client.read_holding_registers(40083,2,unit=slave4id)
        # read watt
        watt=format(resp.registers[0], '04x')
        wr4watt=int(struct.unpack('>h', watt.decode('hex'))[0]) * -1
        # read multiplier
        multiplier=format(resp.registers[1], '04x')
        fmultiplier=int(struct.unpack('>h', multiplier.decode('hex'))[0])
        if fmultiplier == 2:
            fwr4watt = wr4watt * 100
        if fmultiplier == 1:
            fwr4watt = wr4watt * 10
        if fmultiplier == 0:
            fwr4watt = wr4watt
        if fmultiplier == -1:
            fwr4watt = wr4watt / 10
        if fmultiplier == -2:
            fwr4watt = wr4watt / 100
        if fmultiplier == -3:
            fwr4watt = wr4watt / 1000
        if fmultiplier == -4:
            fwr4watt = wr4watt / 10000
        if fmultiplier == -5:
            fwr4watt = wr4watt / 10000
        resp= client.read_holding_registers(40093,2,unit=slave4id)
        value1 = resp.registers[0]
        value2 = resp.registers[1]
        all = format(value1, '04x') + format(value2, '04x')
        final = final + int(struct.unpack('>i', all.decode('hex'))[0])
    except:
        fwr4watt=0
else:
    fwr4watt=0

if extprodakt == 1:
    try:
        resp= client.read_holding_registers(40380,1,unit=slave1id)
        value1 = resp.registers[0]
        all = format(value1, '04x')
        extprod = int(struct.unpack('>h', all.decode('hex'))[0]) * -1
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
