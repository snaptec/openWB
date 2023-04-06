#!/usr/bin/python
import sys
import struct
from pymodbus.client.sync import ModbusSerialClient

seradd = str(sys.argv[1])
idadd = int(sys.argv[2])


def write_to_ramdisk(file: str, content) -> None:
    with open('/var/www/html/openWB/ramdisk/' + file, 'w') as f:
        f.write(str(content))


with ModbusSerialClient(method="rtu", port=seradd, baudrate=9600, stopbits=1, bytesize=8, timeout=1) as client:
    resp = client.read_input_registers(0x00, 2, unit=idadd)
    voltage = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
    voltage = float("%.1f" % voltage)
    write_to_ramdisk("llv1", voltage)
    resp = client.read_input_registers(0x06, 2, unit=idadd)
    lla1 = float(struct.unpack('>f', struct.pack('>HH', *resp.registers))[0])
    lla1 = float("%.1f" % lla1)
    write_to_ramdisk("lla1", lla1)
    resp = client.read_input_registers(0x08, 2, unit=idadd)
    lla2 = float(struct.unpack('>f', struct.pack('>HH', *resp.registers))[0])
    lla2 = float("%.1f" % lla2)
    write_to_ramdisk("llas11", lla2)
    resp = client.read_input_registers(0x0A, 2, unit=idadd)
    lla3 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
    lla3 = float("%.1f" % lla3)
    write_to_ramdisk("llas21", lla3)
    resp = client.read_input_registers(0x0C, 2, unit=idadd)
    llw1 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
    llw1 = int(llw1)
    if llw1 < 15:
        llw1 = 0
    write_to_ramdisk("llaktuell", llw1)

    resp = client.read_input_registers(0x015A, 2, unit=idadd)
    llkwh = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
    llkwh = float("%.3f" % llkwh)
    write_to_ramdisk("llkwh", llkwh)
    resp = client.read_input_registers(0x015C, 2, unit=idadd)
    llkwh = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
    llkwh = float("%.3f" % llkwh)
    write_to_ramdisk("llkwhs1", llkwh)
    resp = client.read_input_registers(0x015E, 2, unit=idadd)
    llkwh = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
    llkwh = float("%.3f" % llkwh)
    write_to_ramdisk("llkwhs2", llkwh)
    resp = client.read_input_registers(0x0E, 2, unit=idadd)
    llw2 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
    llw2 = int(llw2)
    if llw2 < 15:
        llw2 = 0
    write_to_ramdisk("llaktuells1", llw2)

    resp = client.read_input_registers(0x10, 2, unit=idadd)
    llw3 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
    llw3 = int(llw3)
    if llw3 < 15:
        llw3 = 0
    write_to_ramdisk("llaktuells2", llw3)

    resp = client.read_input_registers(0x02, 2, unit=idadd)
    voltage = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
    voltage = float("%.1f" % voltage)
    write_to_ramdisk("llvs11", voltage)
    resp = client.read_input_registers(0x04, 2, unit=idadd)
    voltage = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
    voltage = float("%.1f" % voltage)
    write_to_ramdisk("llvs21", voltage)
