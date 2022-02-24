#!/usr/bin/python
import struct
from pymodbus.client.sync import ModbusSerialClient
from typing import List

from helpermodules.cli import run_using_positional_cli_args


def update(seradd: str, sdmid: int):
    client = ModbusSerialClient(method="rtu", port=seradd, baudrate=9600, stopbits=1, bytesize=8, timeout=1)

    with client:
        # Voltage
        resp = client.read_input_registers(0x08, 4, unit=sdmid)
        voltage = resp.registers[1]
        voltage = float(voltage) / 10
        f = open('/var/www/html/openWB/ramdisk/evuv1', 'w')
        f.write(str(voltage))
        f.close()
        resp = client.read_input_registers(0x0A, 4, unit=sdmid)
        voltage = resp.registers[1]
        voltage = float(voltage) / 10
        f = open('/var/www/html/openWB/ramdisk/evuv2', 'w')
        f.write(str(voltage))
        f.close()
        resp = client.read_input_registers(0x0C, 4, unit=sdmid)
        voltage = resp.registers[1]
        voltage = float(voltage) / 10
        f = open('/var/www/html/openWB/ramdisk/evuv3', 'w')
        f.write(str(voltage))
        f.close()

        # import kWh
        resp = client.read_input_registers(0x0002, 4, unit=sdmid)
        value1 = resp.registers[0]
        value2 = resp.registers[1]
        all = format(value1, '04x') + format(value2, '04x')
        ikwh = int(struct.unpack('>i', all.decode('hex'))[0])
        ikwh = float(ikwh) * 10
        f = open('/var/www/html/openWB/ramdisk/bezugkwh', 'w')
        f.write(str(ikwh))
        f.close()

        # phasen strom
        resp = client.read_input_registers(0x0E, 2, unit=sdmid)
        lla1 = resp.registers[1]
        lla1 = float(lla1) / 100
        f = open('/var/www/html/openWB/ramdisk/bezuga1', 'w')
        f.write(str(lla1))
        f.close()
        resp = client.read_input_registers(0x10, 2, unit=sdmid)
        lla2 = resp.registers[1]
        lla2 = float(lla2) / 100
        f = open('/var/www/html/openWB/ramdisk/bezuga2', 'w')
        f.write(str(lla2))
        f.close()
        resp = client.read_input_registers(0x12, 2, unit=sdmid)
        lla3 = resp.registers[1]
        lla3 = float(lla3) / 100
        f = open('/var/www/html/openWB/ramdisk/bezuga3', 'w')
        f.write(str(lla3))
        f.close()

        # phasen watt
        resp = client.read_input_registers(0x14, 2, unit=sdmid)
        value1 = resp.registers[0]
        value2 = resp.registers[1]
        all = format(value1, '04x') + format(value2, '04x')
        final = int(struct.unpack('>i', all.decode('hex'))[0]) / 100
        f = open('/var/www/html/openWB/ramdisk/bezugw1', 'w')
        f.write(str(final))
        f.close()
        resp = client.read_input_registers(0x16, 2, unit=sdmid)
        value1 = resp.registers[0]
        value2 = resp.registers[1]
        all = format(value1, '04x') + format(value2, '04x')
        final = int(struct.unpack('>i', all.decode('hex'))[0]) / 100
        f = open('/var/www/html/openWB/ramdisk/bezugw2', 'w')
        f.write(str(final))
        f.close()
        resp = client.read_input_registers(0x18, 2, unit=sdmid)
        value1 = resp.registers[0]
        value2 = resp.registers[1]
        all = format(value1, '04x') + format(value2, '04x')
        final = int(struct.unpack('>i', all.decode('hex'))[0]) / 100
        f = open('/var/www/html/openWB/ramdisk/bezugw3', 'w')
        f.write(str(final))
        f.close()

        # total watt
        resp = client.read_input_registers(0x26, 2, unit=sdmid)
        value1 = resp.registers[0]
        value2 = resp.registers[1]
        all = format(value1, '04x') + format(value2, '04x')
        final = int(struct.unpack('>i', all.decode('hex'))[0]) / 100
        f = open('/var/www/html/openWB/ramdisk/wattbezug', 'w')
        f.write(str(final))
        f.close()

        # export kwh
        resp = client.read_input_registers(0x0004, 4, unit=sdmid)
        value1 = resp.registers[0]
        value2 = resp.registers[1]
        all = format(value1, '04x') + format(value2, '04x')
        ekwh = int(struct.unpack('>i', all.decode('hex'))[0])
        ekwh = float(ekwh) * 10
        f = open('/var/www/html/openWB/ramdisk/einspeisungkwh', 'w')
        f.write(str(ekwh))
        f.close()

        # evuhz
        resp = client.read_input_registers(0x2c, 4, unit=sdmid)
        value1 = resp.registers[0]
        value2 = resp.registers[1]
        all = format(value1, '04x') + format(value2, '04x')
        hz = int(struct.unpack('>i', all.decode('hex'))[0])
        hz = round((float(hz) / 100), 2)
        f = open('/var/www/html/openWB/ramdisk/evuhz', 'w')
        f.write(str(hz))
        f.close()


def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
