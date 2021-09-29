#!/usr/bin/env python3
from pymodbus.client.sync import ModbusTcpClient
import struct
import sys

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
    def __init__(self, bat_num, ramdisk=False) -> None:
        super().__init__()
        self.ramdisk = ramdisk
        self.data = {}
        self.data["simulation"] = {}
        self.bat_num = bat_num

    def read(self):
        """ unterscheidet die Version des EVU-Kits und liest die Werte des Moduls aus.
        """
        try:
            if self.data["config"]["version"] == 0:
                self._read_mpm3pm()
            elif self.data["config"]["version"] == 1:
                self._read_sdm120()
            elif self.data["config"]["version"] == 2:
                self._read_sdm630()
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk, "Bat"+str(self.bat_num))

    def _read_mpm3pm(self):
        try:
            client = ModbusTcpClient('192.168.193.19', port=8899)

            try:
                resp = client.read_input_registers(0x0002, 4, unit=1)
                value1 = resp.registers[0]
                value2 = resp.registers[1]
                all = format(value1, '04x') + format(value2, '04x')
                imported = int(struct.unpack('>i', all.decode('hex'))[0])
                imported = float(imported) * 10
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Bat"+str(self.bat_num))
                imported = 0

            # total watt
            try:
                resp = client.read_input_registers(0x26, 2, unit=1)
                value1 = resp.registers[0]
                value2 = resp.registers[1]
                all = format(value1, '04x') + format(value2, '04x')
                power = int(struct.unpack('>i', all.decode('hex'))[0]) / 100
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Bat"+str(self.bat_num))
                power = 0

            # export kwh
            try:
                resp = client.read_input_registers(0x0004, 4, unit=1)
                value1 = resp.registers[0]
                value2 = resp.registers[1]
                all = format(value1, '04x') + format(value2, '04x')
                exported = int(struct.unpack('>i', all.decode('hex'))[0])
                exported = float(exported) * 10
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Bat"+str(self.bat_num))
                exported = 0

            values = [power,
                      0,
                      [imported, exported]]
            self.set(self.bat_num, values, self.ramdisk)
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk, "Bat"+str(self.bat_num))

    def _read_sdm120(self):
        try:
            client = ModbusTcpClient('192.168.193.19', port=8899)

            try:
                resp = client.read_input_registers(0x0048, 2, unit=9)
                vwh = struct.unpack('>f', struct.pack('>HH', *resp.registers))
                imported = float(vwh[0]) * int(1000)
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Bat"+str(self.bat_num))
                imported = 0

            # total watt
            try:
                resp = client.read_input_registers(0x000C, 2, unit=9)
                watt = struct.unpack('>f', struct.pack('>HH', *resp.registers))
                power = int(watt[0])
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Bat"+str(self.bat_num))
                power = 0

            # export kwh
            try:
                resp = client.read_input_registers(0x004a, 2, unit=9)
                vwhe = struct.unpack('>f', struct.pack('>HH', *resp.registers))
                exported = float(vwhe[0]) * int(1000)
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Bat"+str(self.bat_num))
                exported = 0

            values = [power,
                      0,
                      [imported, exported]]
            self.set(self.bat_num, values, self.ramdisk)
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk, "Bat"+str(self.bat_num))

    def _read_sdm630(self):
        try:
            client = ModbusTcpClient('192.168.193.15', port=8899)

            try:
                resp = client.read_input_registers(0x0048, 2, unit=117)
                vwh = struct.unpack('>f', struct.pack('>HH', *resp.registers))
                imported = float(vwh[0]) * int(1000)
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Bat"+str(self.bat_num))
                imported = 0

            # total watt
            try:
                resp = client.read_input_registers(0x000C, 2, unit=117)
                watt = struct.unpack('>f', struct.pack('>HH', *resp.registers))
                watt1 = int(watt[0])
                resp = client.read_input_registers(0x000E, 2, unit=117)
                watt = struct.unpack('>f', struct.pack('>HH', *resp.registers))
                watt2 = int(watt[0])
                resp = client.read_input_registers(0x0010, 2, unit=117)
                watt = struct.unpack('>f', struct.pack('>HH', *resp.registers))
                watt3 = int(watt[0])
                power = (watt1+watt2+watt3)*-1
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Bat"+str(self.bat_num))
                power = 0

            # export kwh
            try:
                resp = client.read_input_registers(0x004a, 2, unit=117)
                vwhe = struct.unpack('>f', struct.pack('>HH', *resp.registers))
                exported = float(vwhe[0]) * int(1000)
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Bat"+str(self.bat_num))
                exported = 0

            values = [power,
                      0,
                      [imported, exported]]
            self.set(self.bat_num, values, self.ramdisk)
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk, "Bat"+str(self.bat_num))


if __name__ == "__main__":
    try:
        mod = module(0, True)
        mod.data["config"] = {}
        version = int(sys.argv[1])
        mod.data["config"]["version"] = version

        mod.read()
    except Exception as e:
        log.log_exception_comp(e, True)
