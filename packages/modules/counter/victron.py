#!/usr/bin/env python3
import sys
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.client.sync import ModbusTcpClient

if __name__ == "__main__":
    from pathlib import Path
    import os
    parentdir2 = str(Path(os.path.abspath(__file__)).parents[2])
    sys.path.insert(0, parentdir2)
    from helpermodules import log
    import set_values
else:
    from ...helpermodules import log
    from . import set_values


class module(set_values.set_values):
    def __init__(self, counter_num, ramdisk=False) -> None:
        super().__init__()
        self.ramdisk = ramdisk
        self.data = {}
        self.data["simulation"] = {}
        self.counter_num = counter_num

    def read(self):
        try:
            modbus_id = self.data["config"]["modbus_id"]

            client = ModbusTcpClient(self.data["config"]["ip_address"], port=502)
            connection = client.connect()

            # grid power
            try:
                resp = client.read_holding_registers(2600, 1, unit=modbus_id)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                power1 = str(decoder.decode_16bit_int())
                resp = client.read_holding_registers(2601, 1, unit=modbus_id)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                power2 = str(decoder.decode_16bit_int())
                resp = client.read_holding_registers(2602, 1, unit=modbus_id)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                power3 = str(decoder.decode_16bit_int())
                power_all = int(power1) + int(power2) + int(power3)
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                power1 = 0
                power2 = 0
                power3 = 0
                power_all = 0

            # grid ampere
            try:
                resp = client.read_holding_registers(2617, 1, unit=modbus_id)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                current1 = str(decoder.decode_16bit_int())
                current1 = float(current1) / 10
                resp = client.read_holding_registers(2619, 1, unit=modbus_id)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                current2 = str(decoder.decode_16bit_int())
                current2 = float(current2) / 10
                resp = client.read_holding_registers(2621, 1, unit=modbus_id)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                current3 = str(decoder.decode_16bit_int())
                current3 = float(current3) / 10
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                current1 = 0
                current2 = 0
                current3 = 0

            # grid voltage
            try:
                resp = client.read_holding_registers(2616, 1, unit=modbus_id)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                voltage1 = str(decoder.decode_16bit_uint())
                voltage1 = float(voltage1) / 10
                resp = client.read_holding_registers(2618, 1, unit=modbus_id)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                voltage2 = str(decoder.decode_16bit_uint())
                voltage2 = float(voltage2) / 10
                resp = client.read_holding_registers(2620, 1, unit=modbus_id)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                voltage3 = str(decoder.decode_16bit_uint())
                voltage3 = float(voltage3) / 10
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                voltage1 = 0
                voltage2 = 0
                voltage3 = 0

            # grid import
            try:
                resp = client.read_holding_registers(2622, 2, unit=modbus_id)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                wh1 = str(decoder.decode_32bit_uint())
                resp = client.read_holding_registers(2624, 2, unit=modbus_id)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                wh2 = str(decoder.decode_32bit_uint())
                resp = client.read_holding_registers(2626, 2, unit=modbus_id)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                wh3 = str(decoder.decode_32bit_uint())

                whs = int(wh1) + int(wh2) + int(wh3)
                imported = whs * 10
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                imported = 0

            # grid export
            try:
                resp = client.read_holding_registers(2628, 2, unit=modbus_id)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                whe1 = str(decoder.decode_32bit_uint())
                resp = client.read_holding_registers(2630, 2, unit=modbus_id)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                whe2 = str(decoder.decode_32bit_uint())
                resp = client.read_holding_registers(2632, 2, unit=modbus_id)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                whe3 = str(decoder.decode_32bit_uint())

                whes = int(whe1) + int(whe2) + int(whe3)
                exported = whes * 10
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                exported = 0

            client.close()

            values = [[voltage1, voltage2, voltage3],
                      [current1, current2, current3],
                      [power1, power2, power3],
                      [0, 0, 0],
                      [imported, exported],
                      power_all,
                      50]
            self.set(self.counter_num, values, self.ramdisk)
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))


if __name__ == "__main__":
    try:
        mod = module(0, True)
        mod.data["config"] = {}
        ip_address = str(sys.argv[1])
        mod.data["config"]["ip_address"] = ip_address
        modbus_id = int(sys.argv[2])
        mod.data["config"]["modbus_id"] = modbus_id

        if int(os.environ.get('debug')) >= 2:
            log.log_1_9('Counter-Module victron ip_address: ' + str(ip_address))
            log.log_1_9('Counter-Module victron modbus_id: ' + str(modbus_id))

        mod.read()
    except Exception as e:
        log.log_exception_comp(e, True)
