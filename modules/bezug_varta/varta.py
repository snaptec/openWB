#!/usr/bin/python
from typing import List
import logging
import struct
from pymodbus.client.sync import ModbusTcpClient

from helpermodules.cli import run_using_positional_cli_args

log = logging.getLogger("Varta EVU")


def update(ipaddress: str):
    client = ModbusTcpClient(ipaddress, port=502)

    with client:
        # gridleistung
        resp = client.read_holding_registers(1078, 1, unit=1)
        value1 = resp.registers[0]
        all = format(value1, '04x')
        final = int(struct.unpack('>h', all.decode('hex'))[0])*-1
        f = open('/var/www/html/openWB/ramdisk/wattbezug', 'w')
        f.write(str(final))
        f.close()


def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
