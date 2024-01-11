#!/usr/bin/python
import sys
import time
import struct
from pymodbus.client.sync import ModbusSerialClient

serial_port = str(sys.argv[1])
unit_id_1 = int(sys.argv[2])
unit_id_2 = int(sys.argv[3])
unit_id_3 = int(sys.argv[4])


def write_to_ramdisk(file, content):
    with open('/var/www/html/openWB/ramdisk/' + file, 'w') as f:
        f.write(str(content))


client = ModbusSerialClient(method="rtu", port=serial_port, baudrate=9600, stopbits=1, bytesize=8, timeout=1)

resp = client.read_input_registers(0x00, 2, unit=unit_id_1)
llv1 = struct.unpack('>f', struct.pack('>HH', *resp.registers))
llv1 = float("%.1f" % llv1[0])
write_to_ramdisk('llv1', llv1)
resp = client.read_input_registers(0x06, 2, unit=unit_id_1)
lla1 = struct.unpack('>f', struct.pack('>HH', *resp.registers))
lla1 = float("%.3f" % lla1[0])
write_to_ramdisk('lla1', lla1)
resp = client.read_input_registers(0x0C, 2, unit=unit_id_1)
ll = struct.unpack('>f', struct.pack('>HH', *resp.registers))
wl1 = int(ll[0])

resp = client.read_input_registers(0x0156, 2, unit=unit_id_1)
llwh = struct.unpack('>f', struct.pack('>HH', *resp.registers))
llwh1 = float("%.3f" % llwh[0])
time.sleep(0.5)
resp = client.read_input_registers(0x00, 2, unit=unit_id_2)
llv2 = struct.unpack('>f', struct.pack('>HH', *resp.registers))
llv2 = float("%.1f" % llv2[0])
write_to_ramdisk('llv2', llv2)
resp = client.read_input_registers(0x06, 2, unit=unit_id_2)
lla2 = struct.unpack('>f', struct.pack('>HH', *resp.registers))
lla2 = float("%.3f" % lla2[0])
write_to_ramdisk('lla2', lla2)
resp = client.read_input_registers(0x0C, 2, unit=unit_id_2)
ll = struct.unpack('>f', struct.pack('>HH', *resp.registers))
wl2 = int(ll[0])
resp = client.read_input_registers(0x0156, 2, unit=unit_id_2)
llwh = struct.unpack('>f', struct.pack('>HH', *resp.registers))
llwh2 = float("%.3f" % llwh[0])
time.sleep(0.5)
resp = client.read_input_registers(0x00, 2, unit=unit_id_3)
llv3 = struct.unpack('>f', struct.pack('>HH', *resp.registers))
llv3 = float("%.1f" % llv3[0])
write_to_ramdisk('llv3', llv3)
resp = client.read_input_registers(0x06, 2, unit=unit_id_3)
lla3 = struct.unpack('>f', struct.pack('>HH', *resp.registers))
lla3 = float("%.3f" % lla3[0])
write_to_ramdisk('lla3', lla3)
resp = client.read_input_registers(0x0C, 2, unit=unit_id_3)
ll = struct.unpack('>f', struct.pack('>HH', *resp.registers))
wl3 = int(ll[0])
resp = client.read_input_registers(0x0156, 2, unit=unit_id_3)
llwh = struct.unpack('>f', struct.pack('>HH', *resp.registers))
llwh3 = float("%.3f" % llwh[0])

llwh = llwh1 + llwh2 + llwh3
write_to_ramdisk('llkwh', llwh)

ll = wl1 + wl2 + wl3
write_to_ramdisk('llaktuell', ll)
