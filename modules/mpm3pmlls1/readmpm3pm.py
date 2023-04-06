#!/usr/bin/python
import sys
import struct
from pymodbus.client.sync import ModbusSerialClient

seradd = sys.argv[1]
idadd = int(sys.argv[2])


def write_to_ramdisk(file: str, content) -> None:
    with open('/var/www/html/openWB/ramdisk/' + file, 'w') as f:
        f.write(str(content))


print("DUO2:"+str(seradd)+" idadd:"+str(idadd))
with ModbusSerialClient(method="rtu", port=seradd, baudrate=9600, stopbits=1, bytesize=8, timeout=1) as client:
    if (idadd < 100):
        # MPM3PM
        resp = client.read_input_registers(0x0002, 4, unit=idadd)
        value1 = resp.registers[0]
        value2 = resp.registers[1]
        all = format(value1, '04x') + format(value2, '04x')
        ikwh = int(struct.unpack('>i', all.decode('hex'))[0])
        ikwh = float(ikwh) / 100
        write_to_ramdisk("llkwhs1", ikwh)

        resp = client.read_input_registers(0x0E, 2, unit=idadd)
        lla1 = resp.registers[1]
        lla1 = float(lla1) / 100
        write_to_ramdisk("llas11", lla1)

        resp = client.read_input_registers(0x10, 2, unit=idadd)
        lla2 = resp.registers[1]
        lla2 = float(lla2) / 100
        write_to_ramdisk("llas12", lla2)

        resp = client.read_input_registers(0x12, 2, unit=idadd)
        lla3 = resp.registers[1]
        lla3 = float(lla3) / 100
        write_to_ramdisk("llas13", lla3)

        resp = client.read_input_registers(0x26, 2, unit=idadd)
        value1 = resp.registers[0]
        value2 = resp.registers[1]
        all = format(value1, '04x') + format(value2, '04x')
        final = int(struct.unpack('>i', all.decode('hex'))[0]) / 100
        if final < 10:
            final = 0
        write_to_ramdisk("llaktuells1", final)

        resp = client.read_input_registers(0x08, 4, unit=idadd)
        voltage = resp.registers[1]
        voltage = float(voltage) / 10
        print("voltage1"+str(voltage))
        write_to_ramdisk("llvs11", voltage)

        resp = client.read_input_registers(0x0A, 4, unit=idadd)
        voltage = resp.registers[1]
        voltage = float(voltage) / 10
        print("voltage2"+str(voltage))
        write_to_ramdisk("llvs12", voltage)

        resp = client.read_input_registers(0x0C, 4, unit=idadd)
        voltage = resp.registers[1]
        voltage = float(voltage) / 10
        print("voltage3"+str(voltage))
        write_to_ramdisk("llvs13", voltage)
    else:
        # SDM630
        resp = client.read_input_registers(0x00, 2, unit=idadd)
        voltage = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
        voltage = float("%.1f" % voltage)
        write_to_ramdisk("llvs11", voltage)
        resp = client.read_input_registers(0x06, 2, unit=idadd)
        lla1 = float(struct.unpack('>f', struct.pack('>HH', *resp.registers))[0])
        lla1 = float("%.1f" % lla1)
        write_to_ramdisk("llas11", lla1)
        resp = client.read_input_registers(0x08, 2, unit=idadd)
        lla2 = float(struct.unpack('>f', struct.pack('>HH', *resp.registers))[0])
        lla2 = float("%.1f" % lla2)
        write_to_ramdisk("llas12", lla2)
        resp = client.read_input_registers(0x0A, 2, unit=idadd)
        lla3 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
        lla3 = float("%.1f" % lla3)
        write_to_ramdisk("llas13", lla3)
        resp = client.read_input_registers(0x0C, 2, unit=idadd)
        llw1 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
        llw1 = int(llw1)
        resp = client.read_input_registers(0x0156, 2, unit=idadd)
        llkwh = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
        llkwh = float("%.3f" % llkwh)
        write_to_ramdisk("llkwhs1", llkwh)
        resp = client.read_input_registers(0x0E, 2, unit=idadd)
        llw2 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
        llw2 = int(llw2)
        resp = client.read_input_registers(0x10, 2, unit=idadd)
        llw3 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
        llw3 = int(llw3)

        resp = client.read_input_registers(0x02, 2, unit=idadd)
        voltage = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
        voltage = float("%.1f" % voltage)
        write_to_ramdisk("llvs12", voltage)
        resp = client.read_input_registers(0x04, 2, unit=idadd)
        voltage = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
        voltage = float("%.1f" % voltage)
        write_to_ramdisk("llvs13", voltage)
        llg = llw1 + llw2 + llw3
        if llg < 10:
            llg = 0
        write_to_ramdisk("llaktuells1", llg)
