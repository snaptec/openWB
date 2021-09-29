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
        try:
            params = (
                ('meterId', self.data["config"]["id"]),
            )
            username = self.data["config"]["username"]
            password = self.data["config"]["password"]
            response = requests.get('https://api.discovergy.com/public/v1/last_reading', params=params, auth=(username, password), timeout=3).json()

            try:
                voltage1 = response["values"]["phase1Voltage"] / 1000
                voltage2 = response["values"]["phase2Voltage"] / 1000
                voltage3 = response["values"]["phase3Voltage"] / 1000
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                voltage1 = 0
                voltage2 = 0
                voltage3 = 0

            try:
                imported = response["values"]["energy"] / 10000000
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                imported = 0

            try:
                exported = response["values"]["energyOut"] / 10000000
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                exported = 0

            try:
                power_all = response["values"]["power"] / 1000
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                power_all = 0
            try:
                power1 = response["values"]["phase1Power"] / 1000
            except KeyError:
                power1 = response["values"]["power1"] / 1000
            try:
                power2 = response["values"]["phase2Power"] / 1000
            except KeyError:
                power2 = response["values"]["power2"] / 1000
            try:
                power3 = response["values"]["phase3Power"] / 1000
            except KeyError:
                power3 = response["values"]["power3"] / 1000

            try:
                if voltage1 > 150:
                    current1 = power1 / voltage1
                else:
                    current1 = power1 / 230
                if voltage2 > 150:
                    current2 = power2 / voltage2
                else:
                    current2 = power2 / 230
                if voltage3 > 150:
                    current3 = power3 / voltage3
                else:
                    current3 = power3 / 230
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                current1 = 0
                current2 = 0
                current3 = 0

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
        username = str(sys.argv[1])
        password = str(sys.argv[2])
        id = str(sys.argv[3])
        mod.data["config"]["username"] = username
        mod.data["config"]["password"] = password
        mod.data["config"]["id"] = id

        mod.read()
    except Exception as e:
        log.log_exception_comp(e, True)
