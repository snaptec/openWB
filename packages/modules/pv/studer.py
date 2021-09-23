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
    def __init__(self, pv_num, ramdisk=False) -> None:
        super().__init__()
        self.ramdisk = ramdisk
        self.data = {}
        self.data["simulation"] = {}
        self.pv_num = pv_num

    def read(self):
        try:
            vc_count = mod.data["module"]["config"]["vc_count"]
            vc_type = mod.data["module"]["config"]["vc_type"]
            client = ModbusTcpClient(self.data["module"]["config"]["ip_address"], port=502)
            connection = client.connect()

            # loop for power
            try:
                if vc_type == 'VS':
                    mb_unit = int(40)
                    mb_register = int(20)  # MB:20; ID: 15010; PV power kW
                elif vc_type == 'VT':
                    mb_unit = int(20)
                    mb_register = int(8)  # MB:8; ID: 11004; Power of the PV generator kW
                power = 0
                i = 1
                while i < vc_count+1:
                    mb_unit_dev = mb_unit+i
                    request = client.read_input_registers(mb_register, 2, unit=mb_unit_dev)
                    if request.isError():
                        log.log_1_9('Modbus Error:', request)
                    else:
                        result = request.registers
                    decoder = BinaryPayloadDecoder.fromRegisters(result, byteorder=Endian.Big)
                    power = power+decoder.decode_32bit_float()  # type: float
                    i += 1

                power = power*1000*-1  # openWB need the values as negative Values in W
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk)
                power = 0

            # loop for counter
            try:
                if vc_type == 'VS':
                    mb_unit = int(40)
                    mb_register = int(46)  # MB:46; ID: 15023; Desc: Total PV produced energy MWh
                elif vc_type == 'VT':
                    mb_unit = int(20)
                    mb_register = int(18)  # MB:18; ID: 11009; Desc: Total produced energy MWh
                counter = 0
                i = 1
                while i < vc_count + 1:
                    mb_unit_dev = mb_unit + i
                    request = client.read_input_registers(mb_register, 2, unit=mb_unit_dev)
                    if request.isError():
                        log.log_1_9('Modbus Error:', request)
                    else:
                        result = request.registers
                    decoder = BinaryPayloadDecoder.fromRegisters(result, byteorder=Endian.Big)
                    counter = counter + decoder.decode_32bit_float()  # type: float
                    i += 1
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk)
                counter = 0

            client.close()
            values = [power,
                      counter,
                      [0, 0, 0]]
            self.set(self.pv_num, values, self.ramdisk)
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk)


if __name__ == "__main__":
    try:
        mod = module(0, True)
        mod.data["module"] = {}
        mod.data["module"]["config"] = {}
        ip_address = str(sys.argv[1])
        mod.data["module"]["config"]["ip_address"] = ip_address
        xt_count = int(sys.argv[2])  # studer_xt (count XT* Devices)
        mod.data["module"]["config"]["xt_count"] = xt_count
        vc_count = int(sys.argv[3])  # studer_vc (count MPPT Devices)
        mod.data["module"]["config"]["vc_count"] = vc_count
        vc_type = str(sys.argv[4])  # studer_vc_type (MPPT type VS or VT)
        mod.data["module"]["config"]["vc_type"] = vc_type

        mod.read()
    except Exception as e:
        log.log_exception_comp(e, True)
