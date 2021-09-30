#!/usr/bin/env python3

import requests
import sys
import traceback

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
            password = self.data["config"]["password"]
            ip_address = self.data["config"]["ip_address"]

            # Grid meter values
            try:
                response = requests.get('http://x:'+password+'@'+ip_address+':8084/rest/channel/meter0/(ActivePower.*|VoltageL.|Frequency)', timeout=1).json()
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))

            voltage1 = 0
            voltage2 = 0
            voltage3 = 0
            power1 = 0
            power2 = 0
            power3 = 0
            frequency = 0
            power_all = 0
            for singleValue in response:
                address = singleValue['address']
                if (address == 'meter0/Frequency'):
                    frequency = singleValue['value']
                elif (address == 'meter0/ActivePower'):
                    power_all = singleValue['value']
                elif (address == 'meter0/ActivePowerL1'):
                    power1 = singleValue['value']
                    p1 = singleValue['value']
                elif (address == 'meter0/ActivePowerL2'):
                    power2 = singleValue['value']
                    p2 = singleValue['value']
                elif (address == 'meter0/ActivePowerL3'):
                    power3 = singleValue['value']
                    p3 = singleValue['value']
                elif (address == 'meter0/VoltageL1'):
                    voltage1 = singleValue['value']
                    v1 = singleValue['value']
                elif (address == 'meter0/VoltageL2'):
                    voltage2 = singleValue['value']
                    v2 = singleValue['value']
                elif (address == 'meter0/VoltageL3'):
                    voltage3 = singleValue['value']
                    v3 = singleValue['value']

            if (v1 != 0):
                current1 = p1 / v1
            if (v2 != 0):
                current2 = p2 / v2
            if (v3 != 0):
                current3 = p3 / v3

            # Grid total energy sums
            try:
                response = requests.get('http://x:'+password+'@'+ip_address+':8084/rest/channel/_sum/Grid.+ActiveEnergy', timeout=1).json()
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))

            for singleValue in response:
                address = singleValue['address']
                if (address == '_sum/GridBuyActiveEnergy'):
                    imported = singleValue['value']
                elif (address == '_sum/GridSellActiveEnergy'):
                    exported = singleValue['value']

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
        password = str(sys.argv[1])
        mod.data["config"]["password"] = password
        ip_address = str(sys.argv[2])
        mod.data["config"]["ip_address"] = ip_address

        if int(os.environ.get('debug')) >= 2:
            log.log_1_9('Counter-Module fems password: ' + str(password))
            log.log_1_9('Counter-Module fems ip_address: ' + str(ip_address))

        mod.read()
    except Exception as e:
        log.log_exception_comp(e, True)
