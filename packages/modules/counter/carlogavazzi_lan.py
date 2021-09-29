import struct
from pymodbus.client.sync import ModbusTcpClient

if __name__ == "__main__":
    from pathlib import Path
    import os
    import sys
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
    def __init__(self, counter_num, ramdisk=False):
        super().__init__()
        self.ramdisk = ramdisk
        self.data = {}
        self.data["simulation"] = {}
        self.counter_num = counter_num

    def read(self):
        try:
            client = ModbusTcpClient(self.data["config"]["ip_address"], port=502)
            sdmid = 1

            # Voltage
            try:
                resp = client.read_input_registers(0x00, 2, unit=sdmid)
                all = format(resp.registers[1], '04x') + format(resp.registers[0], '04x')
                voltage1 = float(struct.unpack('>i', all.decode('hex'))[0])
                voltage1 = float(voltage1) / 10
                resp = client.read_input_registers(0x02, 2, unit=sdmid)
                all = format(resp.registers[1], '04x') + format(resp.registers[0], '04x')
                voltage2 = float(struct.unpack('>i', all.decode('hex'))[0])
                voltage2 = float(voltage2) / 10
                resp = client.read_input_registers(0x04, 2, unit=sdmid)
                all = format(resp.registers[1], '04x') + format(resp.registers[0], '04x')
                voltage3 = float(struct.unpack('>i', all.decode('hex'))[0])
                voltage3 = float(voltage3) / 10
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                voltage1 = 0
                voltage2 = 0
                voltage3 = 0

            # phasen watt
            try:
                resp = client.read_input_registers(0x12, 2, unit=sdmid)
                all = format(resp.registers[1], '04x') + format(resp.registers[0], '04x')
                power1 = int(struct.unpack('>i', all.decode('hex'))[0] / 10)
                resp = client.read_input_registers(0x14, 2, unit=sdmid)
                all = format(resp.registers[1], '04x') + format(resp.registers[0], '04x')
                power2 = int(struct.unpack('>i', all.decode('hex'))[0] / 10)
                resp = client.read_input_registers(0x16, 2, unit=sdmid)
                all = format(resp.registers[1], '04x') + format(resp.registers[0], '04x')
                power3 = int(struct.unpack('>i', all.decode('hex'))[0] / 10)

                power_all = power1 + power2 + power3
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                power1 = 0
                power2 = 0
                power3 = 0
                power_all = 0

            # ampere
            try:
                resp = client.read_input_registers(0x0C, 2, unit=sdmid)
                all = format(resp.registers[1], '04x') + format(resp.registers[0], '04x')
                current1 = float(struct.unpack('>i', all.decode('hex'))[0])
                current1 = abs(current1 / 1000)
                resp = client.read_input_registers(0x0E, 2, unit=sdmid)
                all = format(resp.registers[1], '04x') + format(resp.registers[0], '04x')
                current2 = float(struct.unpack('>i', all.decode('hex'))[0])
                current2 = abs(current2 / 1000)
                resp = client.read_input_registers(0x10, 2, unit=sdmid)
                all = format(resp.registers[1], '04x') + format(resp.registers[0], '04x')
                current3 = float(struct.unpack('>i', all.decode('hex'))[0])
                current3 = abs(current3 / 1000)
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                current1 = 0
                current2 = 0
                current3 = 0

            # evuhz
            try:
                resp = client.read_input_registers(0x33, 2, unit=sdmid)
                frequency = float(resp.registers[0] / 10)
                if frequency > 100:
                    frequency = float(frequency / 10)
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                frequency = 0

            if self.ramdisk == True:
                imported, exported = simcount.sim_count(power_all, ramdisk=True, pref="bezug")
            else:
                imported, exported = simcount.sim_count(power_all, topic="openWB/set/counter/"+str(self.counter_num)+"/", data=self.data["simulation"])
            values = [[voltage1, voltage2, voltage3],
                      [current1, current2, current3],
                      [power1, power2, power3],
                      [0, 0, 0],
                      [imported, exported],
                      power_all,
                      frequency]
            self.set(self.counter_num, values, self.ramdisk)
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))


if __name__ == "__main__":
    try:
        counter_num = 1
        mod = module(0, True)
        mod.data["config"] = {}
        ip_address = sys.argv[1]
        mod.data["config"]["ip_address"] = ip_address

        mod.read()
    except Exception as e:
        log.log_exception_comp(e, True)
