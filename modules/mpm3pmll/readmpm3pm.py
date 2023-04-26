#!/usr/bin/python
import sys
import os
import os.path
import struct
from pymodbus.client.sync import ModbusSerialClient

seradd = str(sys.argv[1])
sdmid = int(sys.argv[2])

client = ModbusSerialClient(method="rtu", port=seradd, baudrate=9600, stopbits=1, bytesize=8, timeout=1)

if (sdmid < 100):
    resp = client.read_input_registers(0x0002, 4, unit=sdmid)
    value1 = resp.registers[0]
    value2 = resp.registers[1]
    all = format(value1, '04x') + format(value2, '04x')
    ikwh = int(struct.unpack('>i', all.decode('hex'))[0])
    # resp = client.read_input_registers(0x0002,2, unit=sdmid)
    # ikwh = resp.registers[1]
    ikwh = float(ikwh) / 100
    f = open('/var/www/html/openWB/ramdisk/llkwh', 'w')
    f.write(str(ikwh))
    f.close()

    resp = client.read_input_registers(0x0E, 2, unit=sdmid)
    lla1 = resp.registers[1]
    lla1 = float(lla1) / 100
    f = open('/var/www/html/openWB/ramdisk/lla1', 'w')
    f.write(str(lla1))
    f.close()

    resp = client.read_input_registers(0x10, 2, unit=sdmid)
    lla2 = resp.registers[1]
    lla2 = float(lla2) / 100
    f = open('/var/www/html/openWB/ramdisk/lla2', 'w')
    f.write(str(lla2))
    f.close()

    resp = client.read_input_registers(0x12, 2, unit=sdmid)
    lla3 = resp.registers[1]
    lla3 = float(lla3) / 100
    f = open('/var/www/html/openWB/ramdisk/lla3', 'w')
    f.write(str(lla3))
    f.close()

    resp = client.read_input_registers(0x26, 2, unit=sdmid)
    value1 = resp.registers[0]
    value2 = resp.registers[1]
    all = format(value1, '04x') + format(value2, '04x')
    final = int(struct.unpack('>i', all.decode('hex'))[0]) / 100
    if final < 15:
        final = 0
    f = open('/var/www/html/openWB/ramdisk/llaktuell', 'w')
    f.write(str(final))
    f.close()

    resp = client.read_input_registers(0x08, 4, unit=sdmid)
    voltage = resp.registers[1]
    voltage = float(voltage) / 10
    f = open('/var/www/html/openWB/ramdisk/llv1', 'w')
    f.write(str(voltage))
    f.close()

    resp = client.read_input_registers(0x0A, 4, unit=sdmid)
    voltage = resp.registers[1]
    voltage = float(voltage) / 10
    f = open('/var/www/html/openWB/ramdisk/llv2', 'w')
    f.write(str(voltage))
    f.close()

    resp = client.read_input_registers(0x0C, 4, unit=sdmid)
    voltage = resp.registers[1]
    voltage = float(voltage) / 10
    f = open('/var/www/html/openWB/ramdisk/llv3', 'w')
    f.write(str(voltage))
    f.close()
    resp = client.read_input_registers(0x2c, 4, unit=sdmid)
    value1 = resp.registers[0]
    value2 = resp.registers[1]
    all = format(value1, '04x') + format(value2, '04x')
    hz = int(struct.unpack('>i', all.decode('hex'))[0])
    hz = round((float(hz) / 100), 2)
    f = open('/var/www/html/openWB/ramdisk/llhz', 'w')
    f.write(str(hz))
    f.close()
else:
    resp = client.read_input_registers(0x00, 2, unit=sdmid)
    voltage = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
    voltage = float("%.1f" % voltage)
    f = open('/var/www/html/openWB/ramdisk/llv1', 'w')
    f.write(str(voltage))
    f.close()
    resp = client.read_input_registers(0x06, 2, unit=sdmid)
    lla1 = float(struct.unpack('>f', struct.pack('>HH', *resp.registers))[0])
    lla1 = float("%.1f" % lla1)
    f = open('/var/www/html/openWB/ramdisk/lla1', 'w')
    f.write(str(lla1))
    f.close()
    resp = client.read_input_registers(0x08, 2, unit=sdmid)
    lla2 = float(struct.unpack('>f', struct.pack('>HH', *resp.registers))[0])
    lla2 = float("%.1f" % lla2)
    f = open('/var/www/html/openWB/ramdisk/lla2', 'w')
    f.write(str(lla2))
    f.close()
    resp = client.read_input_registers(0x0A, 2, unit=sdmid)
    lla3 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
    lla3 = float("%.1f" % lla3)
    f = open('/var/www/html/openWB/ramdisk/lla3', 'w')
    f.write(str(lla3))
    f.close()
    resp = client.read_input_registers(0x0C, 2, unit=sdmid)
    llw1 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
    llw1 = int(llw1)
    resp = client.read_input_registers(0x0156, 2, unit=sdmid)
    llkwh = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
    llkwh = float("%.3f" % llkwh)
    f = open('/var/www/html/openWB/ramdisk/llkwh', 'w')
    f.write(str(llkwh))
    f.close()
    resp = client.read_input_registers(0x0E, 2, unit=sdmid)
    llw2 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
    llw2 = int(llw2)
    resp = client.read_input_registers(0x10, 2, unit=sdmid)
    llw3 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
    llw3 = int(llw3)

    resp = client.read_input_registers(0x02, 2, unit=sdmid)
    voltage = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
    voltage = float("%.1f" % voltage)
    f = open('/var/www/html/openWB/ramdisk/llv2', 'w')
    f.write(str(voltage))
    f.close()
    resp = client.read_input_registers(0x04, 2, unit=sdmid)
    voltage = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
    voltage = float("%.1f" % voltage)
    f = open('/var/www/html/openWB/ramdisk/llv3', 'w')
    f.write(str(voltage))
    f.close()
    llg = llw1 + llw2 + llw3
    if llg < 10:
        llg = 0
    f = open('/var/www/html/openWB/ramdisk/llaktuell', 'w')
    f.write(str(llg))
    f.close()
    resp = client.read_input_registers(0x46, 2, unit=sdmid)
    hz = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
    hz = float("%.2f" % hz)
    f = open('/var/www/html/openWB/ramdisk/llhz', 'w')
    f.write(str(hz))
    f.close()

    resp = client.read_input_registers(0x1E, 2, unit=sdmid)
    pf1 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
    pf1 = float("%.3f" % pf1)
    f = open('/var/www/html/openWB/ramdisk/llpf1', 'w')
    f.write(str(pf1))
    f.close()
    resp = client.read_input_registers(0x20, 2, unit=sdmid)
    pf2 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
    pf2 = float("%.3f" % pf2)
    f = open('/var/www/html/openWB/ramdisk/llpf2', 'w')
    f.write(str(pf2))
    f.close()
    resp = client.read_input_registers(0x22, 2, unit=sdmid)
    pf3 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
    pf3 = float("%.3f" % pf3)
    f = open('/var/www/html/openWB/ramdisk/llpf3', 'w')
    f.write(str(pf3))
    f.close()

    if not os.path.isfile("/var/www/html/openWB/ramdisk/lp1Serial"):
        print("Trying to read meter serial number once from meter at address " + str(seradd) + ", ID " + str(sdmid))
        try:
            resp = client.read_holding_registers(0xFC00, 2, unit=sdmid)
            sn = struct.unpack('>I', struct.pack('>HH', *resp.registers))[0]
            f = open('/var/www/html/openWB/ramdisk/lp1Serial', 'w')
            f.write(str(sn))
            f.close()
        except:
            print("Meter serial number of meter at address " + str(seradd) + ", ID " + str(sdmid) + " is not available")
            f = open('/var/www/html/openWB/ramdisk/lp1Serial', 'w')
            f.write("0")
            f.close()
