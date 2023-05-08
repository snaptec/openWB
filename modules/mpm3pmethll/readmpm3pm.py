#!/usr/bin/python
import struct
from pymodbus.client.sync import ModbusTcpClient

host = '192.168.193.16'
unit_id = 5


def write_to_ramdisk(file, content):
    with open('/var/www/html/openWB/ramdisk/' + file, 'w') as f:
        f.write(str(content))


client = ModbusTcpClient(host, port=8899)

resp = client.read_input_registers(0x0002, 4, unit=unit_id)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value1, '04x') + format(value2, '04x')
ikwh = int(struct.unpack('>i', all.decode('hex'))[0])
ikwh = float(ikwh) / 100
write_to_ramdisk('llkwhs1', ikwh)

resp = client.read_input_registers(0x0E, 2, unit=unit_id)
lla1 = resp.registers[1]
lla1 = float(lla1) / 100
write_to_ramdisk('llas11', lla1)

resp = client.read_input_registers(0x10, 2, unit=unit_id)
lla2 = resp.registers[1]
lla2 = float(lla2) / 100
write_to_ramdisk('llas12', lla2)

resp = client.read_input_registers(0x12, 2, unit=unit_id)
lla3 = resp.registers[1]
lla3 = float(lla3) / 100
write_to_ramdisk('llas13', lla3)

resp = client.read_input_registers(0x26, 2, unit=unit_id)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value1, '04x') + format(value2, '04x')
final = int(struct.unpack('>i', all.decode('hex'))[0]) / 100
if final < 10:
    final = 0
write_to_ramdisk('llaktuells1', final)

resp = client.read_input_registers(0x08, 4, unit=unit_id)
voltage = resp.registers[1]
voltage = float(voltage) / 10
write_to_ramdisk('llvs11', voltage)

resp = client.read_input_registers(0x0A, 4, unit=unit_id)
voltage = resp.registers[1]
voltage = float(voltage) / 10
write_to_ramdisk('llvs12', voltage)

resp = client.read_input_registers(0x0C, 4, unit=unit_id)
voltage = resp.registers[1]
voltage = float(voltage) / 10
write_to_ramdisk('llvs13', voltage)
