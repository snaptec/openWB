#!/usr/bin/env python3
from typing import List
import logging
import struct
import codecs

from pymodbus.client.sync import ModbusTcpClient

from helpermodules.cli import run_using_positional_cli_args

log = logging.getLogger("Varta Speicher")


def update(ipaddress: str, ip2address: str):
    with ModbusTcpClient(ipaddress, port=502) as client:
        # battsoc
        resp = client.read_holding_registers(1068, 1, unit=1)
        value1 = resp.registers[0]
        all = format(value1, '04x')
        sfinal = int(struct.unpack('>h', codecs.decode(all, 'hex'))[0])

        # battleistung
        resp = client.read_holding_registers(1066, 1, unit=1)
        value1 = resp.registers[0]
        all = format(value1, '04x')
        lfinal = int(struct.unpack('>h', codecs.decode(all, 'hex'))[0])

    if ip2address != 'none':
        with ModbusTcpClient(ip2address, port=502) as client2:
            # battsoc
            resp = client2.read_holding_registers(1068, 1, unit=1)
            value1 = resp.registers[0]
            all = format(value1, '04x')
            final = int(struct.unpack('>h', codecs.decode(all, 'hex'))[0])
            sfinal = (sfinal+final)/2
            # battleistung
            resp = client2.read_holding_registers(1066, 1, unit=1)
            value1 = resp.registers[0]
            all = format(value1, '04x')
            final = int(struct.unpack('>h', codecs.decode(all, 'hex'))[0])
            lfinal = lfinal+final

    with open('/var/www/html/openWB/ramdisk/speichersoc', 'w') as f:
        f.write(str(sfinal))
    with open('/var/www/html/openWB/ramdisk/speicherleistung', 'w') as f:
        f.write(str(lfinal))


def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
