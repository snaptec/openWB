#!/usr/bin/python
import sys
import os
import os.path
import struct
from pymodbus.client.sync import ModbusSerialClient


def write_to_ramdisk(file: str, content) -> None:
    with open('/var/www/html/openWB/ramdisk/' + file, 'w') as f:
        f.write(str(content))


def detect_modbus_usb_port():
    """guess USB/modbus device name"""
    known_devices = ("/dev/ttyUSB0", "/dev/ttyACM0", "/dev/serial0")
    for device in known_devices:
        try:
            with open(device):
                return device
        except IOError:
            pass
    return known_devices[-1]  # this does not make sense, but is the same behavior as the old code


seradd = detect_modbus_usb_port()
sdmid = int(sys.argv[2])

with ModbusSerialClient(method="rtu", port=seradd, baudrate=9600, stopbits=1, bytesize=8, timeout=1) as client:
    if (sdmid < 100):
        resp = client.read_input_registers(0x0002, 4, unit=sdmid)
        value1 = resp.registers[0]
        value2 = resp.registers[1]
        all = format(value1, '04x') + format(value2, '04x')
        ikwh = int(struct.unpack('>i', all.decode('hex'))[0])
        ikwh = float(ikwh) / 100
        write_to_ramdisk("llkwh", ikwh)
        resp = client.read_input_registers(0x0E, 2, unit=sdmid)
        lla1 = resp.registers[1]
        lla1 = float(lla1) / 100
        write_to_ramdisk("lla1", lla1)
        resp = client.read_input_registers(0x10, 2, unit=sdmid)
        lla2 = resp.registers[1]
        lla2 = float(lla2) / 100
        write_to_ramdisk("lla2", lla2)
        resp = client.read_input_registers(0x12, 2, unit=sdmid)
        lla3 = resp.registers[1]
        lla3 = float(lla3) / 100
        write_to_ramdisk("lla3", lla3)
        resp = client.read_input_registers(0x26, 2, unit=sdmid)
        value1 = resp.registers[0]
        value2 = resp.registers[1]
        all = format(value1, '04x') + format(value2, '04x')
        final = int(struct.unpack('>i', all.decode('hex'))[0]) / 100
        if final < 15:
            final = 0
        write_to_ramdisk("llaktuell", final)
        resp = client.read_input_registers(0x08, 4, unit=sdmid)
        voltage = resp.registers[1]
        voltage = float(voltage) / 10
        write_to_ramdisk("llv1", voltage)
        resp = client.read_input_registers(0x0A, 4, unit=sdmid)
        voltage = resp.registers[1]
        voltage = float(voltage) / 10
        write_to_ramdisk("llv2", voltage)
        resp = client.read_input_registers(0x0C, 4, unit=sdmid)
        voltage = resp.registers[1]
        voltage = float(voltage) / 10
        write_to_ramdisk("llv3", voltage)
        resp = client.read_input_registers(0x2c, 4, unit=sdmid)
        value1 = resp.registers[0]
        value2 = resp.registers[1]
        all = format(value1, '04x') + format(value2, '04x')
        hz = int(struct.unpack('>i', all.decode('hex'))[0])
        hz = round((float(hz) / 100), 2)
        write_to_ramdisk("llhz", hz)
    else:
        resp = client.read_input_registers(0x00, 2, unit=sdmid)
        voltage = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
        voltage = float("%.1f" % voltage)
        write_to_ramdisk("llv1", voltage)
        resp = client.read_input_registers(0x06, 2, unit=sdmid)
        lla1 = float(struct.unpack('>f', struct.pack('>HH', *resp.registers))[0])
        lla1 = float("%.1f" % lla1)
        write_to_ramdisk("lla1", lla1)
        resp = client.read_input_registers(0x08, 2, unit=sdmid)
        lla2 = float(struct.unpack('>f', struct.pack('>HH', *resp.registers))[0])
        lla2 = float("%.1f" % lla2)
        write_to_ramdisk("lla2", lla2)
        resp = client.read_input_registers(0x0A, 2, unit=sdmid)
        lla3 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
        lla3 = float("%.1f" % lla3)
        write_to_ramdisk("lla3", lla3)
        resp = client.read_input_registers(0x0C, 2, unit=sdmid)
        llw1 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
        llw1 = int(llw1)
        resp = client.read_input_registers(0x0156, 2, unit=sdmid)
        llkwh = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
        llkwh = float("%.3f" % llkwh)
        write_to_ramdisk("llkwh", llkwh)
        resp = client.read_input_registers(0x0E, 2, unit=sdmid)
        llw2 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
        llw2 = int(llw2)
        resp = client.read_input_registers(0x10, 2, unit=sdmid)
        llw3 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
        llw3 = int(llw3)
        resp = client.read_input_registers(0x02, 2, unit=sdmid)
        voltage = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
        voltage = float("%.1f" % voltage)
        write_to_ramdisk("llv2", voltage)
        resp = client.read_input_registers(0x04, 2, unit=sdmid)
        voltage = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
        voltage = float("%.1f" % voltage)
        write_to_ramdisk("llv3", voltage)
        llg = llw1 + llw2 + llw3
        if llg < 10:
            llg = 0
        write_to_ramdisk("llaktuell", llg)
        resp = client.read_input_registers(0x46, 2, unit=sdmid)
        hz = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
        hz = float("%.2f" % hz)
        write_to_ramdisk("llhz", hz)
        resp = client.read_input_registers(0x1E, 2, unit=sdmid)
        pf1 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
        pf1 = float("%.3f" % pf1)
        write_to_ramdisk("llpf1", pf1)
        resp = client.read_input_registers(0x20, 2, unit=sdmid)
        pf2 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
        pf2 = float("%.3f" % pf2)
        write_to_ramdisk("llpf2", pf2)
        resp = client.read_input_registers(0x22, 2, unit=sdmid)
        pf3 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
        pf3 = float("%.3f" % pf3)
        write_to_ramdisk("llpf3", pf3)

        if not os.path.isfile("/var/www/html/openWB/ramdisk/lp1Serial"):
            print("Trying to read meter serial number once from meter at address " + str(seradd) + ", ID " + str(sdmid))
            try:
                resp = client.read_holding_registers(0xFC00, 2, unit=sdmid)
                sn = struct.unpack('>I', struct.pack('>HH', *resp.registers))[0]
                write_to_ramdisk("lp1Serial", sn)
            except Exception:
                print("Meter serial number at address " + str(seradd) + ", ID " + str(sdmid) + " is not available")
                write_to_ramdisk("lp1Serial", 0)
