#!/usr/bin/env python3
import struct
from pymodbus.client.sync import ModbusTcpClient

if __name__ == "__main__":
    from pathlib import Path
    import os
    import sys
    parentdir2 = str(Path(os.path.abspath(__file__)).parents[2])
    sys.path.insert(0, parentdir2)
    from helpermodules import log
    import set_values
else:
    from ...helpermodules import log
    from . import set_values


class module(set_values.set_values):
    def __init__(self, pv_num, ramdisk=False) -> None:
        super().__init__()
        self.ramdisk = ramdisk
        self.data = {}
        self.data["simulation"] = {}
        self.pv_num = pv_num

    def read(self):
        """ unterscheidet die Version des EVU-Kits und liest die Werte des Moduls aus.
        """
        try:
            if self.data["config"]["version"] == 1:
                self._read_lovato()
            elif self.data["config"]["version"] == 2:
                self._read_sdm()
            else:
                self._read_mpm3pm()
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk, "PV"+str(self.pv_num))

    def _read_lovato(self):
        try:
            client = ModbusTcpClient('192.168.193.13', port=8899)

            # Counters
            try:
                resp = client.read_input_registers(0x1a1f, 2, unit=0x08)
                all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
                finalbezug1 = int(struct.unpack('>i', all.decode('hex'))[0])
                resp = client.read_input_registers(0x1a21, 2, unit=0x08)
                all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
                finalbezug2 = int(struct.unpack('>i', all.decode('hex'))[0])
                if (finalbezug1 > finalbezug2):
                    counter = finalbezug1
                else:
                    counter = finalbezug2
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "PV"+str(self.pv_num))
                counter = 0

            # phasen watt
            try:
                resp = client.read_input_registers(0x0013, 2, unit=0x08)
                all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
                power1 = int(struct.unpack('>i', all.decode('hex'))[0] / 100)

                resp = client.read_input_registers(0x0015, 2, unit=0x08)
                all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
                power2 = int(struct.unpack('>i', all.decode('hex'))[0] / 100)
                resp = client.read_input_registers(0x0017, 2, unit=0x08)
                all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
                power3 = int(struct.unpack('>i', all.decode('hex'))[0] / 100)

                power = power1 + power2 + power3
                if (power > 10):
                    power = power*-1
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "PV"+str(self.pv_num))
                power = 0

            try:
                resp = client.read_input_registers(0x0007, 2, unit=0x08)
                all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
                current1 = float(struct.unpack('>i', all.decode('hex'))[0]) / 10000
                resp = client.read_input_registers(0x0009, 2, unit=0x08)
                all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
                current2 = float(struct.unpack('>i', all.decode('hex'))[0]) / 10000
                resp = client.read_input_registers(0x000b, 2, unit=0x08)
                all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
                current3 = float(struct.unpack('>i', all.decode('hex'))[0]) / 10000
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "PV"+str(self.pv_num))
                current1 = 0
                current2 = 0
                current3 = 0

            values = [power,
                      counter,
                      [current1, current2, current3]]
            self.set(self.pv_num, values, self.ramdisk)
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk, "PV"+str(self.pv_num))

    def _read_sdm(self):
        try:
            client = ModbusTcpClient('192.168.193.13', port=8899)
            sdmid = 116

            try:
                resp = client.read_input_registers(0x0C, 2, unit=sdmid)
                llw1 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
                power1 = int(llw1)
                resp = client.read_input_registers(0x0E, 2, unit=sdmid)
                llw1 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
                power2 = int(llw1)
                resp = client.read_input_registers(0x10, 2, unit=sdmid)
                llw1 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
                power3 = int(llw1)
                power = power1 + power2 + power3
                if (power > 10):
                    power = power*-1
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "PV"+str(self.pv_num))
                power = 0

            try:
                resp = client.read_input_registers(0x06, 2, unit=sdmid)
                current1 = float(struct.unpack('>f', struct.pack('>HH', *resp.registers))[0])
                resp = client.read_input_registers(0x08, 2, unit=sdmid)
                current2 = float(struct.unpack('>f', struct.pack('>HH', *resp.registers))[0])
                resp = client.read_input_registers(0x0A, 2, unit=sdmid)
                current3 = float(struct.unpack('>f', struct.pack('>HH', *resp.registers))[0])
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "PV"+str(self.pv_num))
                current1 = 0
                current2 = 0
                current3 = 0

            try:
                resp = client.read_input_registers(0x0156, 2, unit=sdmid)
                pvkwh = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
                counter = float(pvkwh) * 1000
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "PV"+str(self.pv_num))
                counter = 0

            values = [power,
                      counter,
                      [current1, current2, current3]]
            self.set(self.pv_num, values, self.ramdisk)
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk, "PV"+str(self.pv_num))

    def _read_mpm3pm(self):
        try:
            client = ModbusTcpClient('192.168.193.13', port=8899)

            try:
                resp = client.read_input_registers(0x0004, 4, unit=8)
                value1 = resp.registers[0]
                value2 = resp.registers[1]
                all = format(value1, '04x') + format(value2, '04x')
                ikwh = int(struct.unpack('>i', all.decode('hex'))[0])
                counter = float(ikwh) * 10
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "PV"+str(self.pv_num))
                counter = 0

            try:
                resp = client.read_input_registers(0x0E, 2, unit=8)
                lla1 = resp.registers[1]
                current1 = float(lla1) / 100
                resp = client.read_input_registers(0x10, 2, unit=8)
                lla2 = resp.registers[1]
                current2 = float(lla2) / 100
                resp = client.read_input_registers(0x12, 2, unit=8)
                lla3 = resp.registers[1]
                current3 = float(lla3) / 100
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "PV"+str(self.pv_num))
                current1 = 0
                current2 = 0
                current3 = 0

            # total watt
            try:
                resp = client.read_input_registers(0x26, 2, unit=8)
                value1 = resp.registers[0]
                value2 = resp.registers[1]
                all = format(value1, '04x') + format(value2, '04x')
                power = int(struct.unpack('>i', all.decode('hex'))[0]) / 100
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "PV"+str(self.pv_num))
                power = 0

            values = [power,
                      counter,
                      [current1, current2, current3]]
            self.set(self.pv_num, values, self.ramdisk)
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk, "PV"+str(self.pv_num))


if __name__ == "__main__":
    try:
        mod = module(0, True)
        mod.data["config"] = {}
        version = int(sys.argv[1])
        mod.data["config"]["version"] = version

        mod.read()
    except Exception as e:
        log.log_exception_comp(e, True)
