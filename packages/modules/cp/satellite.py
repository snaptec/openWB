#!/usr/bin/python3
from pymodbus.client.sync import ModbusTcpClient
import re
import struct
import time

from ...helpermodules import log
from ...helpermodules import pub


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
    def __init__(self, cp_num, ramdisk=False) -> None:
        super().__init__()
        self.ramdisk = ramdisk
        self.data = {}
        self.data["simulation"] = {}
        self.cp_num = cp_num

    def read(self):
        try:

            ip_address = self.data["config"]["ip_address"]
            id = self.data["config"]["id"]

            client = ModbusTcpClient(ip_address, port=8899)
            rq = client.read_holding_registers(1002, 1, unit=id)
            state = int(rq.registers[0])

            if state == "" or re.search("^[0-9]+$", state) == None:
                # vorherigen Steckerstatus beibehalten (nichts publishen)
                log.message_debug_log("error", "Modbus EVSE read CP"+str(self.cp_num)+" issue - using previous state")
            if state > 1:
                plug_state = True
            else:
                plug_state = False
            if state > 2:
                charge_state = True
            else:
                charge_state = False

            if ( id < 100 ): 
                #resp = client.read_input_registers(0x0002,2, unit=id)
                #counter = resp.registers[1]
                resp = client.read_input_registers(0x0002,4, unit=id)
                value1 = resp.registers[0] 
                value2 = resp.registers[1] 
                all = format(value1, '04x') + format(value2, '04x')
                counter = int(struct.unpack('>i', all.decode('hex'))[0]) 
                counter = float(counter) /100

                resp = client.read_input_registers(0x0E,2, unit=id)
                current1 = resp.registers[1]
                current1 = float(current1) / 100

                resp = client.read_input_registers(0x10,2, unit=id)
                current2 = resp.registers[1]
                current2 = float(current2) / 100

                resp = client.read_input_registers(0x12,2, unit=id)
                current3 = resp.registers[1]
                current3 = float(current3) / 100

                resp = client.read_input_registers(0x26,2, unit=id)
                value1 = resp.registers[0] 
                value2 = resp.registers[1] 
                all = format(value1, '04x') + format(value2, '04x')
                power = int(struct.unpack('>i', all.decode('hex'))[0]) / 100
                if power < 10:
                    power = 0

                resp = client.read_input_registers(0x08,4, unit=id)
                voltage1 = resp.registers[1]
                voltage1 = float(voltage1) / 10

                resp = client.read_input_registers(0x0A,4, unit=id)
                voltage2 = resp.registers[1]
                voltage2 = float(voltage2) / 10

                resp = client.read_input_registers(0x0C,4, unit=id)
                voltage3 = resp.registers[1]
                voltage3 = float(voltage3) / 10
            else:
                resp = client.read_input_registers(0x00,2, unit=id)
                voltage1 = float(struct.unpack('>f',struct.pack('>HH',*resp.registers))[0])

                resp = client.read_input_registers(0x02,2, unit=id)
                voltage2 = float(struct.unpack('>f',struct.pack('>HH',*resp.registers))[0])

                resp = client.read_input_registers(0x04,2, unit=id)
                voltage3 = float(struct.unpack('>f',struct.pack('>HH',*resp.registers))[0])

                resp = client.read_input_registers(0x06,2, unit=id)
                current1 = float(struct.unpack('>f',struct.pack('>HH',*resp.registers))[0])

                resp = client.read_input_registers(0x08,2, unit=id)
                current2 = float(struct.unpack('>f',struct.pack('>HH',*resp.registers))[0])

                resp = client.read_input_registers(0x0A,2, unit=id)
                current3 = float(struct.unpack('>f',struct.pack('>HH',*resp.registers))[0])

                resp = client.read_input_registers(0x0156,2, unit=id)
                counter = float(struct.unpack('>f',struct.pack('>HH',*resp.registers))[0])

                resp = client.read_input_registers(0x0C,2, unit=id)
                llw1 = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
                llw1 = int(llw1)
                resp = client.read_input_registers(0x0E,2, unit=id)
                llw2 = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
                llw2 = int(llw2)
                resp = client.read_input_registers(0x10,2, unit=id)
                llw3 = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
                llw3 = int(llw3)
                power= llw1 + llw2 + llw3
                if power < 10:
                    power = 0

            values = [[voltage1, voltage2, voltage3],
                        [current1, current2, current3],
                        counter,
                        power,
                        plug_state,
                        charge_state]
            self.set(self.counter_num, values, self.ramdisk)
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk, "Ladepunkt "+str(self.cp_num))

    def write(self, current):
        try:
            client = ModbusTcpClient(self.data["config"]["ip_address"], port=8899)
            rq = client.write_registers(1000, current, unit=self.data["config"]["id"])
        except Exception as e:
            log.exception_logging(e)

    def perform_phase_switch(self, duration, phases_to_use):
        client = ModbusTcpClient(self.data["config"]["ip_address"], port=8899)
        if ( phases_to_use == 1 ):
            rq = client.write_register(0x0001, 256, unit=self.data["config"]["id"])
            time.sleep(duration)
            rq = client.write_register(0x0001, 512, unit=self.data["config"]["id"])

        elif ( phases_to_use == 3 ):
            rq = client.write_register(0x0002, 256, unit=self.data["config"]["id"])
            time.sleep(duration)
            rq = client.write_register(0x0002, 512, unit=self.data["config"]["id"])

    def perform_cp_interruption(self, duration):
        client = ModbusTcpClient(self.data["config"]["ip_address"], port=8899)
        rq = client.write_register(0x0001, 256, unit=self.data["config"]["id"])
        time.sleep(duration)
        rq = client.write_register(0x0001, 512, unit=self.data["config"]["id"])

if __name__ == "__main__":
    try:
        mod = module(0, True)
        mod.data["config"] = {}
        mode = int(sys.argv[1])
        ip_address = str(sys.argv[2])
        mod.data["config"]["ip_address"] = ip_address
        id = str(sys.argv[3])
        mod.data["config"]["id"] = id

        if int(os.environ.get('debug')) >= 2:
            log.log_1_9('Chargepoint-Module satellite(ip evse) mode: ' + str(mode))
            log.log_1_9('Chargepoint-Module satellite(ip evse) ip_address: ' + str(ip_address))
            log.log_1_9('Chargepoint-Module satellite(ip evse) id: ' + str(id))

        if mode == 1:
            mod.read()
        elif mode == 2:
            current = int(sys.argv[4])
            if int(os.environ.get('debug')) >= 2:
                log.log_1_9('Chargepoint-Module satellite(ip evse) current: ' + str(current))
            mod.write(current)
        elif mode == 3:
            phases_to_use = int(sys.argv[4])
            duration = int(sys.argv[5])
            if int(os.environ.get('debug')) >= 2:
                log.log_1_9('Chargepoint-Module satellite(ip evse) phases_to_use: ' + str(phases_to_use))
                log.log_1_9('Chargepoint-Module satellite(ip evse) duration: ' + str(duration))
            mod.perform_phase_switch(duration, phases_to_use)
        else:
            duration = int(sys.argv[4])
            if int(os.environ.get('debug')) >= 2:
                log.log_1_9('Chargepoint-Module satellite(ip evse) duration: ' + str(duration))
            mod.perform_cp_interruption(duration)
    except Exception as e:
        log.log_exception_comp(e, True)