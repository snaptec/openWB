#!/usr/bin/python
import struct
from pymodbus.client.sync import ModbusTcpClient
from typing import List

from helpermodules.cli import run_using_positional_cli_args


def update(seradd: str, sdmid: int, ser2add: str, sdm2id: int):
    with ModbusTcpClient(seradd, port=8899) as client:
        resp = client.read_input_registers(0x000C, 2, unit=sdmid)
        watt = struct.unpack('>f', struct.pack('>HH', *resp.registers))
        watt1 = int(watt[0])

        resp = client.read_input_registers(0x004a, 2, unit=sdmid)
        vwh = struct.unpack('>f', struct.pack('>HH', *resp.registers))
        vwh1 = float("%.3f" % vwh[0])
        resp = client.read_input_registers(0x0048, 2, unit=sdmid)
        v1wh = struct.unpack('>f', struct.pack('>HH', *resp.registers))
        v1wh1 = float("%.3f" % v1wh[0])

    try:
        if sdm2id > 0:
            with ModbusTcpClient(ser2add, port=8899) as client2:
                resp = client2.read_input_registers(0x000C, 2, unit=sdm2id)
                watt = struct.unpack('>f', struct.pack('>HH', *resp.registers))
                watt2 = int(watt[0])

                resp = client2.read_input_registers(0x004a, 2, unit=sdm2id)
                vwh = struct.unpack('>f', struct.pack('>HH', *resp.registers))
                vwh2 = float("%.3f" % vwh[0])
                resp = client2.read_input_registers(0x0048, 2, unit=sdm2id)
                v1wh = struct.unpack('>f', struct.pack('>HH', *resp.registers))
                v1wh2 = float("%.3f" % v1wh[0])
        else:
            watt2 = 0
            vwh2 = 0
            v1wh2 = 0

    except:
        watt2 = 0
        vwh2 = 0
        v1wh2 = 0
        pass

    watt = watt1+watt2
    if watt > 0:
        watt = watt*-1
    with open("/var/www/html/openWB/ramdisk/pv2watt", 'w') as f:
        f.write(str(watt))

    if vwh1 > v1wh1:
        final1wh = vwh1
    else:
        final1wh = v1wh1
    if vwh2 > v1wh2:
        final2wh = vwh2
    else:
        final2wh = v1wh2
    finalwh = final1wh+final2wh
    vwh2 = float(finalwh) * int(1000)
    vwh3 = str(vwh2)
    with open("/var/www/html/openWB/ramdisk/pv2kwh", 'w') as f:
        f.write(str(vwh3))


def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
