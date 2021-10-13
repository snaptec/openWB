#!/usr/bin/env python3
import time

try:
    from ...helpermodules import log
    from ...helpermodules import simcount
    from ..common import connect_tcp
    from ..common import store
except:
    from pathlib import Path
    import os
    import sys
    parentdir2 = str(Path(os.path.abspath(__file__)).parents[2])
    sys.path.insert(0, parentdir2)
    from helpermodules import log
    from helpermodules import simcount
    from modules.common import connect_tcp
    from modules.common import store


class AlphaEssInverter():
    def __init__(self, client: connect_tcp.ConnectTcp, component: dict) -> None:
        try:
            self.client = client
            self.component = component
            self.data = {}
            self.data["simulation"] = {}
            self.value_store = (store.ValueStoreFactory().get_storage("counter"))()
            simcount_factory = simcount.SimCountFactory().get_sim_counter()
            self.sim_count = simcount_factory()
        except Exception as e:
            log.MainLogger().error("Fehler im Modul "+self.component["name"], e)

    def read(self):
        try:
            factory_method = self.__version_factory(self.component["configuration"]["version"])
            power = factory_method(sdmid=85)

            _, counter = self.sim_count.sim_count(power, topic="openWB/set/pv/"+str(self.component["id"])+"/", data=self.data["simulation"], prefix="pv")
            self.value_store.set(self.component["id"], power=power, counter=counter, currents=[0, 0, 0])
        except Exception as e:
            log.MainLogger().error("Fehler im Modul "+self.component["name"], e)

    def __version_factory(self, version: int):
        try:
            if version == 0:
                return self.__read_before_v123
            else:
                return self.__read_since_v123
        except Exception as e:
            log.MainLogger().error("Fehler im Modul "+self.component["name"], e)

    def __read_before_v123(self, sdmid: int) -> float:
        try:
            pvw = self.client.read_binary_registers_to_int(0x0012, 4, sdmid, 32)
            if (pvw < 0):
                pvw = pvw * -1
            time.sleep(0.1)
            pvw2 = self.client.read_binary_registers_to_int(0x041F, 4, sdmid, 32)
            pvw3 = self.client.read_binary_registers_to_int(0x0423, 4, sdmid, 32)
            pvw4 = self.client.read_binary_registers_to_int(0x0427, 4, sdmid, 32)
            power = (pvw + pvw2 + pvw3 + pvw4) * -1
            return power
        except Exception as e:
            log.MainLogger().error("Fehler im Modul "+self.component["name"], e)

    def __read_since_v123(self, sdmid: int) -> float:
        try:
            pvw = self.client.read_binary_registers_to_int(0x00A1, 4, sdmid, 32)
            if (pvw < 0):
                pvw = pvw * -1
            time.sleep(0.1)
            pvw2 = self.client.read_binary_registers_to_int(0x041F, 4, sdmid, 32)
            pvw3 = self.client.read_binary_registers_to_int(0x0423, 4, sdmid, 32)
            pvw4 = self.client.read_binary_registers_to_int(0x0427, 4, sdmid, 32)
            power = (pvw + pvw2 + pvw3 + pvw4) * -1
            return power
        except Exception as e:
            log.MainLogger().error("Fehler im Modul "+self.component["name"], e)
