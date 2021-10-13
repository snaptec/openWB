#!/usr/bin/env python3
import time
from typing import Tuple

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


class AlphaEssBat():
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
            power, soc = factory_method(sdmid=85)

            imported, exported = self.sim_count.sim_count(power, topic="openWB/set/bat/"+str(self.component["id"])+"/", data=self.data["simulation"], prefix="speicher")
            self.value_store.set(self.component["id"], power=power, soc=soc, imported=imported, exported=exported)
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

    def __read_before_v123(self, sdmid: int) -> Tuple[float, int]:
        try:
            time.sleep(0.1)
            voltage = self.client.read_binary_registers_to_int(0x0100, 2, sdmid, 16)
            time.sleep(0.1)
            current = self.client.read_binary_registers_to_int(0x0100, 2, sdmid, 16)
            power = float(voltage * current * -1 / 100)
            time.sleep(0.1)
            w2 = self.client.read_binary_registers_to_int(0x0102, 2, sdmid, 16)
            soc = int(w2 * 0.1)
            return power, soc
        except Exception as e:
            log.MainLogger().error("Fehler im Modul "+self.component["name"], e)

    def __read_since_v123(self, sdmid: int) -> Tuple[float, int]:
        try:
            time.sleep(0.1)
            voltage = self.client.read_binary_registers_to_int(0x0100, 2, sdmid, 16)
            time.sleep(0.1)
            current = self.client.read_binary_registers_to_int(0x0101, 2, sdmid, 16)
            power = float(voltage * current * -1 / 100)
            time.sleep(0.1)
            w2 = self.client.read_binary_registers_to_int(0x0102, 2, sdmid, 16)
            soc = int(w2 * 0.1)
            return power, soc
        except Exception as e:
            log.MainLogger().error("Fehler im Modul "+self.component["name"], e)
