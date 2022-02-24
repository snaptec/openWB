#!/usr/bin/python
import struct
from pymodbus.client.sync import ModbusTcpClient
from typing import List

from helpermodules.cli import run_using_positional_cli_args


def update(ipaddress: str, slave1id: int):
    client = ModbusTcpClient(ipaddress, port=502)

    with client:
        # batterie auslesen und pv leistung korrigieren
        resp = client.read_holding_registers(40083, 2, unit=slave1id)
        # read watt
        watt = format(resp.registers[0], '04x')
        wr1watt = int(struct.unpack('>h', watt.decode('hex'))[0]) * -1
        # read multiplier
        multiplier = format(resp.registers[1], '04x')
        fmultiplier = int(struct.unpack('>h', multiplier.decode('hex'))[0])
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
        f = open('/var/www/html/openWB/ramdisk/pv2watt', 'w')
        f.write(str(fwr1watt))
        f.close()

        resp = client.read_holding_registers(40093, 2, unit=slave1id)
        value1 = resp.registers[0]
        value2 = resp.registers[1]
        all = format(value1, '04x') + format(value2, '04x')
        final = int(struct.unpack('>i', all.decode('hex'))[0])
        f = open('/var/www/html/openWB/ramdisk/pv2kwh', 'w')
        f.write(str(final))
        f.close()
        pvkwhk = final / 1000
        f = open('/var/www/html/openWB/ramdisk/pv2kwhk', 'w')
        f.write(str(pvkwhk))
        f.close()


def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
