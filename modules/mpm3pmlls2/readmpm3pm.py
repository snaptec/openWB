#!/usr/bin/python
import sys
import struct
from pymodbus.client.sync import ModbusSerialClient

seradd = str(sys.argv[1])
sdmid = int(sys.argv[2])


def write_to_ramdisk(file: str, content) -> None:
    with open('/var/www/html/openWB/ramdisk/' + file, 'w') as f:
        f.write(str(content))


print("DUO3:"+str(seradd)+" idadd:"+str(sdmid))
with ModbusSerialClient(method="rtu", port=seradd, baudrate=9600, stopbits=1, bytesize=8, timeout=1) as client:
    resp = client.read_input_registers(0x0002, 4, unit=sdmid)
    value1 = resp.registers[0]
    value2 = resp.registers[1]
    all = format(value1, '04x') + format(value2, '04x')
    ikwh = int(struct.unpack('>i', all.decode('hex'))[0])
    ikwh = float(ikwh) / 100
    write_to_ramdisk("llkwhs2", ikwh)

    resp = client.read_input_registers(0x0E, 2, unit=sdmid)
    lla1 = resp.registers[1]
    lla1 = float(lla1) / 100
    write_to_ramdisk("llas21", lla1)

    resp = client.read_input_registers(0x10, 2, unit=sdmid)
    lla2 = resp.registers[1]
    lla2 = float(lla2) / 100
    write_to_ramdisk("llas22", lla2)

    resp = client.read_input_registers(0x12, 2, unit=sdmid)
    lla3 = resp.registers[1]
    lla3 = float(lla3) / 100
    write_to_ramdisk("llas23", lla3)

    resp = client.read_input_registers(0x26, 2, unit=sdmid)
    value1 = resp.registers[0]
    value2 = resp.registers[1]
    all = format(value1, '04x') + format(value2, '04x')
    final = int(struct.unpack('>i', all.decode('hex'))[0]) / 100
    write_to_ramdisk("llaktuells2", final)

    resp = client.read_input_registers(0x08, 4, unit=sdmid)
    voltage = resp.registers[1]
    voltage = float(voltage) / 10
    write_to_ramdisk("llvs21", voltage)

    resp = client.read_input_registers(0x0A, 4, unit=sdmid)
    voltage = resp.registers[1]
    voltage = float(voltage) / 10
    write_to_ramdisk("llvs22", voltage)

    resp = client.read_input_registers(0x0C, 4, unit=sdmid)
    voltage = resp.registers[1]
    voltage = float(voltage) / 10
    write_to_ramdisk("llvs23", voltage)
