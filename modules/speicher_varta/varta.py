#!/usr/bin/python
from typing import List
import logging
import struct

from helpermodules.cli import run_using_positional_cli_args


from pymodbus.client.sync import ModbusTcpClient

log = logging.getLogger("Varta Speicher")


def update(ipaddress: str, ip2address: str):
    client = ModbusTcpClient(ipaddress, port=502)

    # battsoc
    with client:
        resp = client.read_holding_registers(1068, 1, unit=1)
        value1 = resp.registers[0]
        all = format(value1, '04x')

        sfinal = int(struct.unpack('>h', all.decode('hex'))[0])

        # battleistung
        resp = client.read_holding_registers(1066, 1, unit=1)
        value1 = resp.registers[0]
        all = format(value1, '04x')
        lfinal = int(struct.unpack('>h', all.decode('hex'))[0])

    if ip2address != 'none':
        client2 = ModbusTcpClient(ip2address, port=502)
        with client2:
            # battsoc
            resp = client2.read_holding_registers(1068, 1, unit=1)
            value1 = resp.registers[0]
            all = format(value1, '04x')
            final = int(struct.unpack('>h', all.decode('hex'))[0])
            sfinal = (sfinal+final)/2
            # battleistung
            resp = client2.read_holding_registers(1066, 1, unit=1)
            value1 = resp.registers[0]
            all = format(value1, '04x')
            final = int(struct.unpack('>h', all.decode('hex'))[0])
            lfinal = lfinal+final

    f = open('/var/www/html/openWB/ramdisk/speichersoc', 'w')
    f.write(str(sfinal))
    f.close()
    f = open('/var/www/html/openWB/ramdisk/speicherleistung', 'w')
    f.write(str(lfinal))
    f.close()


def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
