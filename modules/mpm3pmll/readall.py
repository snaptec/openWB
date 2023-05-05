#!/usr/bin/python
import os
import os.path
import struct
import traceback
from pymodbus.client.sync import ModbusSerialClient
from pymodbus.exceptions import ModbusIOException


def write_to_ramdisk(file, content):
    with open('/var/www/html/openWB/ramdisk/' + file, 'w') as f:
        f.write(str(content))


def detect_modbus_usb_port():
    """guess USB/modbus device name"""
    known_devices = ("/dev/ttyUSB0", "/dev/ttyACM0", "/dev/serial0")
    for device in known_devices:
        try:
            with open(device):
                return device
        except Exception:
            pass
    return known_devices[-1]  # this does not make sense, but is the same behavior as the old code


serial_port = detect_modbus_usb_port()
client = ModbusSerialClient(method="rtu", port=serial_port, baudrate=9600, stopbits=1, bytesize=8, timeout=1)
unit_id = None

try:
    with open('/var/www/html/openWB/ramdisk/llmodulconfig', 'r') as value:
        meter_type = str(value.read())
        if meter_type == 'sdm':
            unit_id = 105
        elif meter_type == 'mpm':
            unit_id = 5
        elif meter_type == 'b23':
            unit_id = 201
        else:
            raise Exception
except Exception:
    # check mpm3pm
    try:
        meter_unit_id = 5
        resp = client.read_input_registers(0x10, 2, unit=meter_unit_id)
        if type(resp) == ModbusIOException:
            print("no response from id " + str(meter_unit_id))
            raise Exception
        write_to_ramdisk('llmodulconfig', 'mpm')
        unit_id = meter_unit_id
    except Exception:
        pass
    # check sdm
    try:
        meter_unit_id = 105
        resp = client.read_input_registers(0x00, 2, unit=meter_unit_id)
        if type(resp) == ModbusIOException:
            print("no response from id " + str(meter_unit_id))
            raise Exception
        voltage = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
        if int(voltage) > 20:
            write_to_ramdisk('llmodulconfig', 'sdm')
            unit_id = meter_unit_id
    except Exception:
        pass
    # check b23
    try:
        meter_unit_id = 201
        resp = client.read_holding_registers(0x5B00, 2, unit=meter_unit_id)
        if type(resp) == ModbusIOException:
            print("no response from id " + str(meter_unit_id))
            raise Exception
        voltage = resp.registers[1]
        if int(voltage) > 20:
            write_to_ramdisk('llmodulconfig', 'b23')
            unit_id = meter_unit_id
    except Exception:
        pass
if unit_id is None:
    write_to_ramdisk('llmodulconfig', 'meter failure')
    print("could not detect installed meter!")
    exit(1)

try:
    if (unit_id < 100):
        resp = client.read_input_registers(0x0002, 4, unit=unit_id)
        value1 = resp.registers[0]
        value2 = resp.registers[1]
        all = format(value1, '04x') + format(value2, '04x')
        ikwh = int(struct.unpack('>i', all.decode('hex'))[0])
        ikwh = float(ikwh) / 100
        write_to_ramdisk('llkwh', ikwh)

        resp = client.read_input_registers(0x0E, 2, unit=unit_id)
        lla1 = resp.registers[1]
        lla1 = float(lla1) / 100
        write_to_ramdisk('lla1', lla1)

        resp = client.read_input_registers(0x10, 2, unit=unit_id)
        lla2 = resp.registers[1]
        lla2 = float(lla2) / 100
        write_to_ramdisk('lla2', lla2)

        resp = client.read_input_registers(0x12, 2, unit=unit_id)
        lla3 = resp.registers[1]
        lla3 = float(lla3) / 100
        write_to_ramdisk('lla3', lla3)

        resp = client.read_input_registers(0x26, 2, unit=unit_id)
        value1 = resp.registers[0]
        value2 = resp.registers[1]
        all = format(value1, '04x') + format(value2, '04x')
        final = int(struct.unpack('>i', all.decode('hex'))[0]) / 100
        if final < 15:
            final = 0
        write_to_ramdisk('llaktuell', final)

        resp = client.read_input_registers(0x08, 4, unit=unit_id)
        voltage = resp.registers[1]
        voltage = float(voltage) / 10
        write_to_ramdisk('llv1', voltage)

        resp = client.read_input_registers(0x0A, 4, unit=unit_id)
        voltage = resp.registers[1]
        voltage = float(voltage) / 10
        write_to_ramdisk('llv2', voltage)

        resp = client.read_input_registers(0x0C, 4, unit=unit_id)
        voltage = resp.registers[1]
        voltage = float(voltage) / 10
        write_to_ramdisk('llv3', voltage)
        resp = client.read_input_registers(0x2c, 4, unit=unit_id)
        value1 = resp.registers[0]
        value2 = resp.registers[1]
        all = format(value1, '04x') + format(value2, '04x')
        hz = int(struct.unpack('>i', all.decode('hex'))[0])
        hz = round((float(hz) / 100), 2)
        write_to_ramdisk('llhz', hz)
    elif unit_id > 100 and unit_id < 200:
        resp = client.read_input_registers(0x00, 2, unit=unit_id)
        voltage = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
        voltage = float("%.1f" % voltage)
        write_to_ramdisk('llv1', voltage)
        resp = client.read_input_registers(0x06, 2, unit=unit_id)
        lla1 = float(struct.unpack('>f', struct.pack('>HH', *resp.registers))[0])
        lla1 = float("%.1f" % lla1)
        write_to_ramdisk('lla1', lla1)
        resp = client.read_input_registers(0x08, 2, unit=unit_id)
        lla2 = float(struct.unpack('>f', struct.pack('>HH', *resp.registers))[0])
        lla2 = float("%.1f" % lla2)
        write_to_ramdisk('lla2', lla2)
        resp = client.read_input_registers(0x0A, 2, unit=unit_id)
        lla3 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
        lla3 = float("%.1f" % lla3)
        write_to_ramdisk('lla3', lla3)
        resp = client.read_input_registers(0x0C, 2, unit=unit_id)
        llw1 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
        llw1 = int(llw1)
        resp = client.read_input_registers(0x0156, 2, unit=unit_id)
        llkwh = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
        llkwh = float("%.3f" % llkwh)
        write_to_ramdisk('llkwh', llkwh)
        resp = client.read_input_registers(0x0E, 2, unit=unit_id)
        llw2 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
        llw2 = int(llw2)
        resp = client.read_input_registers(0x10, 2, unit=unit_id)
        llw3 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
        llw3 = int(llw3)

        resp = client.read_input_registers(0x02, 2, unit=unit_id)
        voltage = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
        voltage = float("%.1f" % voltage)
        write_to_ramdisk('llv2', voltage)
        resp = client.read_input_registers(0x04, 2, unit=unit_id)
        voltage = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
        voltage = float("%.1f" % voltage)
        write_to_ramdisk('llv3', voltage)
        llg = llw1 + llw2 + llw3
        if llg < 10:
            llg = 0
        write_to_ramdisk('llaktuell', llg)
        resp = client.read_input_registers(0x46, 2, unit=unit_id)
        hz = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
        hz = float("%.2f" % hz)
        write_to_ramdisk('llhz', hz)

        resp = client.read_input_registers(0x1E, 2, unit=unit_id)
        pf1 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
        pf1 = float("%.3f" % pf1)
        write_to_ramdisk('llpf1', pf1)
        resp = client.read_input_registers(0x20, 2, unit=unit_id)
        pf2 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
        pf2 = float("%.3f" % pf2)
        write_to_ramdisk('llpf2', pf2)
        resp = client.read_input_registers(0x22, 2, unit=unit_id)
        pf3 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
        pf3 = float("%.3f" % pf3)
        write_to_ramdisk('llpf3', pf3)

        if not os.path.isfile("/var/www/html/openWB/ramdisk/lp1Serial"):
            print("Trying to read meter serial number once from meter at address " +
                  str(serial_port) + ", ID " + str(unit_id))
            try:
                resp = client.read_holding_registers(0xFC00, 2, unit=unit_id)
                sn = struct.unpack('>I', struct.pack('>HH', *resp.registers))[0]
                write_to_ramdisk('lp1Serial', sn)
            except Exception:
                print("Meter serial number of meter at address " +
                      str(serial_port) + ", ID " + str(unit_id) + " is not available")
                write_to_ramdisk('lp1Serial', "0")

    elif unit_id > 200:
        # llkwh
        resp = client.read_holding_registers(0x5000, 4, unit=unit_id)
        value1 = resp.registers[0]
        value2 = resp.registers[1]
        value3 = resp.registers[2]
        value4 = resp.registers[3]
        all = format(value3, '04x') + format(value4, '04x')
        ikwh = int(struct.unpack('>i', all.decode('hex'))[0])
        ikwh = float(ikwh)/100
        write_to_ramdisk('llkwh', ikwh)
        # Voltage
        resp = client.read_holding_registers(0x5B00, 2, unit=unit_id)
        voltage = resp.registers[1]
        voltage = float(voltage) / 10
        write_to_ramdisk('llv1', voltage)
        resp = client.read_holding_registers(0x5B02, 2, unit=unit_id)
        voltage = resp.registers[1]
        voltage = float(voltage) / 10
        write_to_ramdisk('llv2', voltage)
        resp = client.read_holding_registers(0x5B04, 2, unit=unit_id)
        voltage = resp.registers[1]
        voltage = float(voltage) / 10
        write_to_ramdisk('llv3', voltage)
        # Ampere
        resp = client.read_holding_registers(0x5B0C, 2, unit=unit_id)
        amp = resp.registers[1]
        amp = float(amp) / 100
        write_to_ramdisk('lla1', amp)
        resp = client.read_holding_registers(0x5B0E, 2, unit=unit_id)
        amp = resp.registers[1]
        amp = float(amp) / 100
        write_to_ramdisk('lla2', amp)
        resp = client.read_holding_registers(0x5B10, 2, unit=unit_id)
        amp = resp.registers[1]
        amp = float(amp) / 100
        write_to_ramdisk('lla3', amp)

        # Gesamt watt
        resp = client.read_holding_registers(0x5B14, 2, unit=unit_id)
        value1 = resp.registers[0]
        value2 = resp.registers[1]
        all = format(value1, '04x') + format(value2, '04x')
        final = int(struct.unpack('>i', all.decode('hex'))[0]) / 100
        # if final < 15:
        #    final = 0
        write_to_ramdisk('llaktuell', final)
        # LL Hz
        resp = client.read_holding_registers(0x5B2C, 2, unit=unit_id)
        hz = float(resp.registers[0]) / 100
        write_to_ramdisk('llhz', hz)
except Exception:
    write_to_ramdisk('llmodulconfig', 'data failure')
    traceback.print_exc()
