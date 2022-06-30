#!/usr/bin/python3
from typing import List
import struct
from pymodbus.client.sync import ModbusTcpClient

from helpermodules.cli import run_using_positional_cli_args


def update(ipaddress: str):
    with ModbusTcpClient(ipaddress, port=502) as client:
        resp = client.read_holding_registers(30865, 2, unit=3)
        value1 = resp.registers[0]
        value2 = resp.registers[1]
        all = format(value1, '04x') + format(value2, '04x')
        bezug = int(struct.unpack('>i', all.decode('hex'))[0])
        resp = client.read_holding_registers(30867, 2, unit=3)
        value1 = resp.registers[0]
        value2 = resp.registers[1]
        all = format(value1, '04x') + format(value2, '04x')
        einsp = int(struct.unpack('>i', all.decode('hex'))[0])
        if bezug > 5:
            final = bezug
        else:
            final = einsp * -1
    with open('/var/www/html/openWB/ramdisk/wattbezug', 'w') as file:
        file.write(str(final))


def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
