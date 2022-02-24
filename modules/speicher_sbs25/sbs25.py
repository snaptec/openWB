#!/usr/bin/python3
from typing import List
import struct
from pymodbus.client.sync import ModbusTcpClient

from helpermodules.cli import run_using_positional_cli_args


def update(ipaddress: str):
    with ModbusTcpClient(ipaddress, port=502) as client:
        resp = client.read_holding_registers(30845, 2, unit=3)
        value1 = resp.registers[0]
        value2 = resp.registers[1]
        all = format(value1, '04x') + format(value2, '04x')
        speicher_soc = int(struct.unpack('>i', all.decode('hex'))[0])

        resp = client.read_holding_registers(31393, 2, unit=3)
        value1 = resp.registers[0]
        value2 = resp.registers[1]
        all = format(value1, '04x') + format(value2, '04x')
        ladung = int(struct.unpack('>i', all.decode('hex'))[0])
        resp = client.read_holding_registers(31395, 2, unit=3)
        value1 = resp.registers[0]
        value2 = resp.registers[1]
        all = format(value1, '04x') + format(value2, '04x')
        entladung = int(struct.unpack('>i', all.decode('hex'))[0])
        if ladung > 5:
            speicher_leistung = ladung
        else:
            speicher_leistung = entladung * -1
    with open('/var/www/html/openWB/ramdisk/speichersoc', 'w') as file:
        file.write(str(speicher_soc))
    with open('/var/www/html/openWB/ramdisk/speicherleistung', 'w') as file:
        file.write(str(speicher_leistung))


def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
