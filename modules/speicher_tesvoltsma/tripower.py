#!/usr/bin/env python3
from typing import List
import struct
import codecs
from pymodbus.client.sync import ModbusTcpClient

from helpermodules.cli import run_using_positional_cli_args


def update(ipaddress: str):
    with ModbusTcpClient(ipaddress, port=502) as client:
        # print "SoC batt"
        resp = client.read_input_registers(1056, 2, unit=25)
        value1 = resp.registers[0]
        value2 = resp.registers[1]
        all = format(value1, '04x') + format(value2, '04x')
        final = int(struct.unpack('>i', codecs.decode(all, 'hex'))[0])/10
        with open('/var/www/html/openWB/ramdisk/speichersoc', 'w') as f:
            f.write(str(final))

        # print "be-entladen watt"
        resp = client.read_input_registers(1012, 2, unit=25)
        value1 = resp.registers[0]
        value2 = resp.registers[1]
        all = format(value1, '04x') + format(value2, '04x')
        ladung = int(struct.unpack('>i', codecs.decode(all, 'hex'))[0]) * -1
        with open('/var/www/html/openWB/ramdisk/speicherleistung', 'w') as f:
            f.write(str(ladung))


def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
