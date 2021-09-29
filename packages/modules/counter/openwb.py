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
    from helpermodules import simcount
    import set_values
else:
    from ...helpermodules import log
    from ...helpermodules import simcount
    from . import set_values

class module(set_values.set_values):
    def __init__(self, counter_num, ramdisk=False) -> None:
        super().__init__()
        self.ramdisk = ramdisk
        self.data = {}
        self.data["simulation"] = {}
        self.counter_num = counter_num

    def read(self):
        """ unterscheidet die Version des EVU-Kits und liest die Werte des Moduls aus.
        """
        try:
            if self.data["config"]["version"] == 0:
                self._read_version0()
            elif self.data["config"]["version"] == 1:
                self._read_lovato()
            elif self.data["config"]["version"] == 2:
                self._read_sdm()
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))

    def _read_version0(self):
        """ liest die Werte des openWB EVU Kit Version 0.

        Parameters
        ----------
        counter_num: int
            Nummer des Zähles
        """
        try:
            ip_address = self.data["config"]["ip_address"]
            id = self.data["config"]["id"]
            client = ModbusTcpClient(ip_address, port=8899)

            # Voltage
            try:
                resp = client.read_input_registers(0x08,4, unit=id)
                voltage1 = resp.registers[1]
                voltage1 = float(voltage1) / 10
                resp = client.read_input_registers(0x0A,4, unit=id)
                voltage2 = resp.registers[1]
                voltage2 = float(voltage2) / 10
                resp = client.read_input_registers(0x0C,4, unit=id)
                voltage3 = resp.registers[1]
                voltage3 = float(voltage3) / 10
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                voltage1 = 0
                voltage2 = 0
                voltage3 = 0

            try:
                resp = client.read_input_registers(0x0002,4, unit=id)
                value1 = resp.registers[0]
                value2 = resp.registers[1]
                all = format(value1, '04x') + format(value2, '04x')
                imported = int(struct.unpack('>i', all.decode('hex'))[0])
                imported = float(imported) * 10
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                imported = 0

            # phasen watt
            try:
                resp = client.read_input_registers(0x14,2, unit=id)
                value1 = resp.registers[0]
                value2 = resp.registers[1]
                all = format(value1, '04x') + format(value2, '04x')
                power1 = int(struct.unpack('>i', all.decode('hex'))[0]) / 100
                resp = client.read_input_registers(0x16,2, unit=id)
                value1 = resp.registers[0]
                value2 = resp.registers[1]
                all = format(value1, '04x') + format(value2, '04x')
                power2 = int(struct.unpack('>i', all.decode('hex'))[0]) / 100
                resp = client.read_input_registers(0x18,2, unit=id)
                value1 = resp.registers[0]
                value2 = resp.registers[1]
                all = format(value1, '04x') + format(value2, '04x')
                power3 = int(struct.unpack('>i', all.decode('hex'))[0]) / 100
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                power1 = 0
                power2 = 0
                power3 = 0

            try:
                current1=round(float(float(power1) / float(voltage1)), 2)
                current2=round(float(float(power2) / float(voltage2)), 2)
                current3=round(float(float(power3) / float(voltage3)), 2)
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                current1 = 0
                current2 = 0
                current3 = 0

            # total watt
            try:
                resp = client.read_input_registers(0x26,2, unit=id)
                value1 = resp.registers[0]
                value2 = resp.registers[1]
                all = format(value1, '04x') + format(value2, '04x')
                power_all = int(struct.unpack('>i', all.decode('hex'))[0]) / 100
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                power_all = 0

            # export kwh
            try:
                resp = client.read_input_registers(0x0004,4, unit=id)
                value1 = resp.registers[0]
                value2 = resp.registers[1]
                all = format(value1, '04x') + format(value2, '04x')
                exported = int(struct.unpack('>i', all.decode('hex'))[0])
                exported = float(exported) * 10
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                exported = 0

            # evuhz
            try:
                resp = client.read_input_registers(0x2c,4, unit=id)
                value1 = resp.registers[0]
                value2 = resp.registers[1]
                all = format(value1, '04x') + format(value2, '04x')
                frequency = int(struct.unpack('>i', all.decode('hex'))[0])
                frequency = round((float(frequency) / 100), 2)
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                frequency = 0

            # Power Factor
            try:
                resp = client.read_input_registers(0x20,4, unit=id)
                value1 = resp.registers[0]
                value2 = resp.registers[1]
                all = format(value1, '04x') + format(value2, '04x')
                evupf1 = int(struct.unpack('>i', all.decode('hex'))[0])
                evupf1 = round((float(evupf1) / 10), 0)
                resp = client.read_input_registers(0x22,4, unit=id)
                value1 = resp.registers[0]
                value2 = resp.registers[1]
                all = format(value1, '04x') + format(value2, '04x')
                evupf2 = int(struct.unpack('>i', all.decode('hex'))[0])
                evupf2 = round((float(evupf2) / 10), 0)
                resp = client.read_input_registers(0x24,4, unit=id)
                value1 = resp.registers[0]
                value2 = resp.registers[1]
                all = format(value1, '04x') + format(value2, '04x')
                evupf3 = int(struct.unpack('>i', all.decode('hex'))[0])
                evupf3 = round((float(evupf3) / 10), 0)
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                power_factor1 = 0
                power_factor2 = 0
                power_factor3 = 0

            values = [[voltage1, voltage2, voltage3],
                        [current1, current2, current3],
                        [power1, power2, power3],
                        [power_factor1, power_factor2, power_factor3],
                        [imported, exported],
                        power_all,
                        frequency]
            self.set(self.counter_num, values, self.ramdisk)
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))

    def _read_lovato(self):
        """ liest die Werte des openWB EVU Kit Version 1 - Lovato.

        Return
        ------
        power_all: float
        """
        try:
            ip_address = self.data["config"]["ip_address"]
            id = self.data["config"]["id"]
            client = ModbusTcpClient(ip_address, port=8899)

            #Voltage
            try:
                resp = client.read_input_registers(0x0001,2, unit=id)
                voltage1 = float(resp.registers[1] / 100)
                resp = client.read_input_registers(0x0003,2, unit=id)
                voltage2 = float(resp.registers[1] / 100)
                resp = client.read_input_registers(0x0005,2, unit=id)
                voltage3 = float(resp.registers[1] / 100)
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                voltage1 = 0
                voltage2 = 0
                voltage3 = 0

            #phasen watt
            try:
                resp = client.read_input_registers(0x0013,2, unit=id)
                all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
                power1 = int(struct.unpack('>i', all.decode('hex'))[0] / 100)
                resp = client.read_input_registers(0x0015,2, unit=id)
                all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
                power2 = int(struct.unpack('>i', all.decode('hex'))[0] / 100)
                resp = client.read_input_registers(0x0017,2, unit=id)
                all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
                power3 = int(struct.unpack('>i', all.decode('hex'))[0] / 100)

                power_all= power1 + power2 + power3
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                power1 = 0
                power2 = 0
                power3 = 0
                power_all = 0

            #ampere
            try:
                resp = client.read_input_registers(0x0007, 2, unit=id)
                all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
                current1 = abs(float(struct.unpack('>i', all.decode('hex'))[0]) / 10000)
                resp = client.read_input_registers(0x0009, 2, unit=id)
                all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
                current2 = abs(float(struct.unpack('>i', all.decode('hex'))[0]) / 10000)
                resp = client.read_input_registers(0x000b, 2, unit=id)
                all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
                current3 = abs(float(struct.unpack('>i', all.decode('hex'))[0]) / 10000)
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                current1 = 0
                current2 = 0
                current3 = 0

            #evuhz
            try:
                resp = client.read_input_registers(0x0031,2, unit=id)
                frequency= float(resp.registers[1])
                frequency= float(frequency / 100)
                if frequency > 100:
                    frequency=float(frequency / 10)
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                frequency = 0

            #Power Factor
            try:
                resp = client.read_input_registers(0x0025,2, unit=id)
                power_factor1 = float(resp.registers[1]) / 10000
                resp = client.read_input_registers(0x0027,2, unit=id)
                power_factor2 = float(resp.registers[1]) / 10000
                resp = client.read_input_registers(0x0029,2, unit=id)
                power_factor3 = float(resp.registers[1]) / 10000
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                power_factor1 = 0
                power_factor2 = 0
                power_factor3 = 0

            if self.ramdisk == True:
                imported, exported = simcount.sim_count(power_all, ramdisk=True, pref="bezug")
            else:
                imported, exported = simcount.sim_count(power_all, topic="openWB/set/counter/"+str(self.counter_num)+"/", data=self.data["simulation"])

            values = [[voltage1, voltage2, voltage3],
                        [current1, current2, current3],
                        [power1, power2, power3],
                        [power_factor1, power_factor2, power_factor3],
                        [imported, exported],
                        power_all,
                        frequency]
            self.set(self.counter_num, values, self.ramdisk)
            
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))

    def _read_sdm(self):
        """ liest die Werte des openWB EVU Kit Version 2 - SDM.

        Return
        ------
        power_all: float
        """
        try:
            ip_address = self.data["config"]["ip_address"]
            id = self.data["config"]["id"]
            client = ModbusTcpClient(ip_address, port=8899)

            try:
                # Voltage
                resp = client.read_input_registers(0x00, 2, unit=id)
                voltage1 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
                resp = client.read_input_registers(0x02, 2, unit=id)
                voltage2 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
                resp = client.read_input_registers(0x04, 2, unit=id)
                voltage3 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                voltage1 = 0
                voltage2 = 0
                voltage3 = 0

            try:
                # phasen watt
                resp = client.read_input_registers(0x0C, 2, unit=id)
                power1 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
                resp = client.read_input_registers(0x0E, 2, unit=id)
                power2 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
                resp = client.read_input_registers(0x10, 2, unit=id)
                power3 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]

                power_all = power1 + power2 + power3
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                power1 = 0
                power2 = 0
                power3 = 0
                power_all = 0

            try:
                # ampere l1
                resp = client.read_input_registers(0x06, 2, unit=id)
                current1 = abs(float(struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]))
                resp = client.read_input_registers(0x08, 2, unit=id)
                current2 = abs(float(struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]))
                resp = client.read_input_registers(0x0A, 2, unit=id)
                current3 = abs(float(struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]))
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                current1 = 0
                current2 = 0
                current3 = 0

            try:
                # evuhz
                resp = client.read_input_registers(0x46, 2, unit=id)
                frequency = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
                if float(frequency) > 100:
                    frequency = float(frequency / 10)
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                frequency = 0

            try:
                # Power Factor
                resp = client.read_input_registers(0x1E, 2, unit=id)
                power_factor1 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
                resp = client.read_input_registers(0x20, 2, unit=id)
                power_factor2 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
                resp = client.read_input_registers(0x22, 2, unit=id)
                power_factor3 = struct.unpack('>f', struct.pack('>HH', *resp.registers))[0]
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                power_factor1 = 0
                power_factor2 = 0
                power_factor3 = 0

            if self.ramdisk == True:
                imported, exported = simcount.sim_count(power_all, ramdisk=True, pref="bezug")
            else:
                imported, exported = simcount.sim_count(power_all, topic="openWB/set/counter/"+str(self.counter_num)+"/", data=self.data["simulation"])
            values = [[voltage1, voltage2, voltage3],
                    [current1, current2, current3],
                    [power1, power2, power3],
                    [power_factor1, power_factor2, power_factor3],
                    [imported, exported],
                    power_all,
                    frequency]
            self.set(self.counter_num, values, self.ramdisk)
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))


if __name__ == "__main__":
    try:
        mod = module(0, True)
        mod.data["config"] = {}
        version = int(sys.argv[1])
        mod.data["config"]["version"] = version
        if version == 0:
            mod.data["config"]["ip_address"] = "192.168.193.15"
            mod.data["config"]["id"] = 5
        elif version == 1:
            mod.data["config"]["ip_address"] = "192.168.193.15"
            mod.data["config"]["id"] = 0x02
        elif version == 2:
            # mod.data["config"]["ip_address"] = "192.168.193.15"
            # mod.data["config"]["id"] = 115
            mod.data["config"]["ip_address"] = "192.168.1.101"
            mod.data["config"]["id"] = 105

        log.log_1_9('EVU-Kit Version: ' + str(version))
        log.log_1_9(str(os.environ))
        log.log_1_9(os.environ['HOME'])
        # if int(os.environ.get('debug')) >= 2:
        #     log.log_1_9('EVU-Kit Version: ' + str(version))

        mod.read()
    except Exception as e:
        log.log_exception_comp(e, True)
