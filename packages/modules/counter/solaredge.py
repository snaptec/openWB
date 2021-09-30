#!/usr/bin/env python3
import sys
import struct
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
            slave_id = self.data["config"]["slave_id"]

            client = ModbusTcpClient(self.data["config"]["ip_address"], port=self.data["config"]["modbus_port"])

            try:
                resp = client.read_holding_registers(40206, 5, unit=slave_id)
                value1 = resp.registers[0]
                all = format(value1, '04x')
                final = int(struct.unpack('>h', all.decode('hex'))[0]) * -1

                sf = resp.registers[4]
                sf = format(sf, '04x')
                fsf = int(struct.unpack('>h', sf.decode('hex'))[0])
                if fsf == 4:
                    power_all = final * 10000
                if fsf == 3:
                    power_all = final * 1000
                if fsf == 2:
                    power_all = final * 100
                if fsf == 1:
                    power_all = final * 10
                if fsf == -1:
                    power_all = final / 10
                if fsf == -2:
                    power_all = final / 100
                if fsf == -3:
                    power_all = final / 1000
                if fsf == -4:
                    power_all = final / 10000
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                power_all = 0

            try:
                resp = client.read_holding_registers(40194, 2, unit=slave_id)
                multipli = resp.registers[0]
                multiplint = format(multipli, '04x')
                fmultiplint = int(struct.unpack('>h', multiplint.decode('hex'))[0])
                resp = client.read_holding_registers(40191, 1, unit=slave_id)
                value1 = resp.registers[0]
                all = format(value1, '04x')
                current1 = int(struct.unpack('>h', all.decode('hex'))[0])
                resp = client.read_holding_registers(40192, 1, unit=slave_id)
                value1 = resp.registers[0]
                all = format(value1, '04x')
                current2 = int(struct.unpack('>h', all.decode('hex'))[0])
                resp = client.read_holding_registers(40193, 1, unit=slave_id)
                value1 = resp.registers[0]
                all = format(value1, '04x')
                current3 = int(struct.unpack('>h', all.decode('hex'))[0])

                resp = client.read_holding_registers(40194, 2, unit=slave_id)
                mult2ipli = resp.registers[0]
                mult2iplint = format(mult2ipli, '04x')
                fmult2iplint = int(struct.unpack('>h', mult2iplint.decode('hex'))[0])

                if fmultiplint == fmult2iplint:
                    if fmultiplint == 4:
                        current1 = current1 * 10000
                        current2 = current2 * 10000
                        current3 = current3 * 10000
                    if fmultiplint == 3:
                        current1 = current1 * 1000
                        current2 = current2 * 1000
                        current3 = current3 * 1000
                    if fmultiplint == 2:
                        current1 = current1 * 100
                        current2 = current2 * 100
                        current3 = current3 * 100
                    if fmultiplint == 1:
                        current1 = current1 * 10
                        current2 = current2 * 10
                        current3 = current3 * 10
                    if fmultiplint == 0:
                        current1 = current1
                        current2 = current2
                        current3 = current3
                    if fmultiplint == -1:
                        current1 = current1 / 10
                        current2 = current2 / 10
                        current3 = current3 / 10
                    if fmultiplint == -2:
                        current1 = current1 / 100
                        current2 = current2 / 100
                        current3 = current3 / 100
                    if fmultiplint == -3:
                        current1 = current1 / 1000
                        current2 = current2 / 1000
                        current3 = current3 / 1000
                    if fmultiplint == -4:
                        current1 = current1 / 10000
                        current2 = current2 / 10000
                        current3 = current3 / 10000
                    if fmultiplint == -5:
                        current1 = current1 / 100000
                        current2 = current2 / 100000
                        current3 = current3 / 100000
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                current1 = 0
                current2 = 0
                current3 = 0

            # voltage
            try:
                resp = client.read_holding_registers(40196, 1, unit=slave_id)
                value1 = resp.registers[0]
                all = format(value1, '04x')
                voltage1 = int(struct.unpack('>h', all.decode('hex'))[0]) / 100
                resp = client.read_holding_registers(40197, 1, unit=slave_id)
                value1 = resp.registers[0]
                all = format(value1, '04x')
                voltage2 = int(struct.unpack('>h', all.decode('hex'))[0]) / 100
                resp = client.read_holding_registers(40198, 1, unit=slave_id)
                value1 = resp.registers[0]
                all = format(value1, '04x')
                voltage3 = int(struct.unpack('>h', all.decode('hex'))[0]) / 100
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                voltage1 = 0
                voltage2 = 0
                voltage3 = 0

            # watt pro phase
            try:
                resp = client.read_holding_registers(40207, 1, unit=slave_id)
                value1 = resp.registers[0]
                all = format(value1, '04x')
                power1 = int(struct.unpack('>h', all.decode('hex'))[0]) * -1
                resp = client.read_holding_registers(40208, 1, unit=slave_id)
                value1 = resp.registers[0]
                all = format(value1, '04x')
                power2 = int(struct.unpack('>h', all.decode('hex'))[0]) * -1
                resp = client.read_holding_registers(40209, 1, unit=slave_id)
                value1 = resp.registers[0]
                all = format(value1, '04x')
                power3 = int(struct.unpack('>h', all.decode('hex'))[0]) * -1
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                power1 = 0
                power2 = 0
                power3 = 0

            # hz
            try:
                resp = client.read_holding_registers(40204, 1, unit=slave_id)
                value1 = resp.registers[0]
                all = format(value1, '04x')
                frequency = int(struct.unpack('>h', all.decode('hex'))[0])

                resp = client.read_holding_registers(40205, 1, unit=slave_id)
                multipli = resp.registers[0]
                multiplint = format(multipli, '04x')
                fmuliplint = int(struct.unpack('>h', multiplint.decode('hex'))[0])

                if fmultiplint == 4:
                    frequency = frequency * 1000
                if fmultiplint == 3:
                    frequency = frequency * 100
                if fmultiplint == 2:
                    frequency = frequency * 10
                if fmultiplint == 1:
                    frequency = frequency * 1
                if fmultiplint == 0:
                    frequency = frequency / 10
                if fmultiplint == -1:
                    frequency = frequency / 100
                if fmultiplint == -2:
                    frequency = frequency / 1000
                if fmultiplint == -3:
                    frequency = frequency / 10000
                if fmultiplint == -4:
                    frequency = frequency / 100000
                if fmultiplint == -5:
                    frequency = frequency / 1000000
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                frequency = 0

            try:
                resp = client.read_holding_registers(40234, 2, unit=slave_id)
                value1 = resp.registers[0]
                value2 = resp.registers[1]
                all = format(value1, '04x') + format(value2, '04x')
                imported = int(struct.unpack('>i', all.decode('hex'))[0])
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                imported = 0

            try:
                resp = client.read_holding_registers(40226, 2, unit=slave_id)
                value1 = resp.registers[0]
                value2 = resp.registers[1]
                all = format(value1, '04x') + format(value2, '04x')
                final = int(struct.unpack('>i', all.decode('hex'))[0])
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                exported = 0

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
        mod = module(0, True)
        mod.data["config"] = {}
        ip_address = str(sys.argv[1])
        mod.data["config"]["ip_address"] = ip_address
        modbus_port = int(sys.argv[2])
        mod.data["config"]["modbus_port"] = modbus_port
        slave_id = int(sys.argv[3])
        mod.data["config"]["slave_id"] = slave_id

        if int(os.environ.get('debug')) >= 2:
            log.log_1_9('Counter-Module solaredge ip_address: ' + str(ip_address))
            log.log_1_9('Counter-Module solaredge modbus_port: ' + str(modbus_port))
            log.log_1_9('Counter-Module solaredge slave_id: ' + str(slave_id))

        mod.read()
    except Exception as e:
        log.log_exception_comp(e, True)
