#!/usr/bin/python
import struct
from pymodbus.client.sync import ModbusTcpClient
from typing import List
import codecs

from helpermodules.cli import run_using_positional_cli_args


def update(ipaddress: str, slave1id: int):
    with ModbusTcpClient(ipaddress, port=502) as client:
        # Batterie auslesen und PV Leistung korrigieren
        # read watt
        resp = client.read_holding_registers(40083, 2, unit=slave1id)
        watt = format(resp.registers[0], '04x')
        wr1watt = int(struct.unpack('>h', codecs.decode(watt, 'hex'))[0]) * -1
        # read multiplier
        multiplier = format(resp.registers[1], '04x')
        fmultiplier = int(struct.unpack('>h', codecs.decode(multiplier, 'hex'))[0])
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
        with open('/var/www/html/openWB/ramdisk/pv2watt', 'w') as f:
            f.write(str(int(fwr1watt)))

        resp = client.read_holding_registers(40093, 2, unit=slave1id)
        value1 = resp.registers[0]
        value2 = resp.registers[1]
        all = format(value1, '04x') + format(value2, '04x')
        final = int(struct.unpack('>i', codecs.decode(all, 'hex'))[0])
        with open('/var/www/html/openWB/ramdisk/pv2kwh', 'w') as f:
            f.write(str(final))
        pvkwhk = final / 1000
        with open('/var/www/html/openWB/ramdisk/pv2kwhk', 'w') as f:
            f.write(str(pvkwhk))


def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
