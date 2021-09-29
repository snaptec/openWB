#!/usr/bin/env python3
import sys
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
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
    def __init__(self, bat_num, ramdisk=False) -> None:
        super().__init__()
        self.ramdisk = ramdisk
        self.data = {}
        self.data["simulation"] = {}
        self.bat_num = bat_num

    def read(self):
        try:
            client = ModbusTcpClient(self.data["config"]["ip_address"], port=502)
            connection = client.connect()

            # Studer Battery Power
            try:
                request = client.read_input_registers(6, 2, unit=60)
                if request.isError():
                    # handle error, log?
                    log.log_1_9('Modbus Error:', request)
                else:
                    result = request.registers
                decoder = BinaryPayloadDecoder.fromRegisters(result, byteorder=Endian.Big)
                power = decoder.decode_32bit_float()  # type: float
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Bat"+str(self.bat_num))
                power = 0

            # Studer SOC
            try:
                request = client.read_input_registers(4, 2, unit=60)
                if request.isError():
                    # handle error, log?
                    log.log_1_9('Modbus Error:', request)
                else:
                    result = request.registers
                decoder = BinaryPayloadDecoder.fromRegisters(result, byteorder=Endian.Big)
                soc = decoder.decode_32bit_float()  # type: float
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Bat"+str(self.bat_num))
                soc = 0

            # Studer charged Energy
            try:
                request = client.read_input_registers(14, 2, unit=60)
                if request.isError():
                    # handle error, log?
                    log.log_1_9('Modbus Error:', request)
                else:
                    result = request.registers
                decoder = BinaryPayloadDecoder.fromRegisters(result, byteorder=Endian.Big)
                imported = decoder.decode_32bit_float()*48  # type: float
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Bat"+str(self.bat_num))
                imported = 0

            # Studer discharged Energy
            try:
                request = client.read_input_registers(16, 2, unit=60)
                if request.isError():
                    # handle error, log?
                    log.log_1_9('Modbus Error:', request)
                else:
                    result = request.registers
                decoder = BinaryPayloadDecoder.fromRegisters(result, byteorder=Endian.Big)
                exported = decoder.decode_32bit_float()*48  # type: float
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Bat"+str(self.bat_num))
                exported = 0

            client.close()

            values = [power,
                      soc,
                      [imported, exported]]
            self.set(self.bat_num, values, self.ramdisk)
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk, "Bat"+str(self.bat_num))


if __name__ == "__main__":
    try:
        mod = module(0, True)
        mod.data["config"] = {}
        ip_address = str(sys.argv[1])
        mod.data["config"]["ip_address"] = ip_address

        mod.read()
    except Exception as e:
        log.log_exception_comp(e, True)
