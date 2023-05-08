#!/usr/bin/python
import sys
import struct
from pymodbus.client.sync import ModbusSerialClient

serial_port = str(sys.argv[1])
unit_id = int(sys.argv[2])
pv_flag = str(sys.argv[3])


def write_to_ramdisk(file, content):
    with open('/var/www/html/openWB/ramdisk/' + file, 'w') as f:
        f.write(str(content))


client = ModbusSerialClient(method="rtu", port=serial_port, baudrate=9600, stopbits=1, bytesize=8, timeout=1)

resp = client.read_input_registers(0x0004, 4, unit=unit_id)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value1, '04x') + format(value2, '04x')
ekwh = int(struct.unpack('>i', all.decode('hex'))[0])
ekwh = float(ekwh) / 100
write_to_ramdisk('speicherekwh', ekwh)

resp = client.read_input_registers(0x0002, 4, unit=unit_id)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value1, '04x') + format(value2, '04x')
ikwh = int(struct.unpack('>i', all.decode('hex'))[0])
ikwh = float(ikwh) * 10
write_to_ramdisk('speicherikwh', ikwh)

resp = client.read_input_registers(0x0E, 2, unit=unit_id)
lla1 = resp.registers[1]
lla1 = float(lla1) / 100
write_to_ramdisk('speichera1', lla1)

resp = client.read_input_registers(0x10, 2, unit=unit_id)
lla2 = resp.registers[1]
lla2 = float(lla2) / 100
write_to_ramdisk('speichera2', lla2)

resp = client.read_input_registers(0x12, 2, unit=unit_id)
lla3 = resp.registers[1]
lla3 = float(lla3) / 100
write_to_ramdisk('speichera3', lla3)

# total watt
resp = client.read_input_registers(0x26, 2, unit=unit_id)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value1, '04x') + format(value2, '04x')
final = int(struct.unpack('>i', all.decode('hex'))[0]) / 100
if (pv_flag == 1):
    with open('/var/www/html/openWB/ramdisk/pvwatt', 'r') as pvwatt_file:
        pvwatt = pvwatt_file.read()
    final = (int(final) - int(pvwatt)) * -1
write_to_ramdisk('speicherleistung', final)
