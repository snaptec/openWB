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
            self.value_store = (store.ValueStoreFactory().get_storage("bat"))()
            simcount_factory = simcount.SimCountFactory().get_sim_counter()
            self.sim_count = simcount_factory()
        except Exception as e:
            log.MainLogger().error("Fehler im Modul "+self.component["name"], e)

    def read(self):
        try: 
            log.MainLogger().debug("Komponente "+self.component["name"]+" auslesen.")
            # keine Unterschiede zwischen den Versionen
            sdmid=85

            time.sleep(0.1)
            voltage = self.client.read_binary_registers_to_int(0x0100, 2, sdmid, 16)
            time.sleep(0.1)
            current = self.client.read_binary_registers_to_int(0x0101, 2, sdmid, 16)
            
            if voltage != None and current != None:
                power = float(voltage * current * -1 / 100)
            else:
                power = None
            log.MainLogger().debug("Alpha Ess Leistung[W]: "+str(power)+", Speicher-Register: Spannung[V] "+str(voltage)+" Strom[A] "+str(current))
            time.sleep(0.1)
            soc_reg = self.client.read_binary_registers_to_int(0x0102, 2, sdmid, 16)
            if soc_reg != None:
                soc = int(soc_reg * 0.1)
            else:
                soc = None

            imported, exported = self.sim_count.sim_count(power, topic="openWB/set/bat/"+str(self.component["id"])+"/", data=self.data["simulation"], prefix="speicher")
            self.value_store.set(self.component["id"], power=power, soc=soc, imported=imported, exported=exported)
        except Exception as e:
            log.MainLogger().error("Fehler im Modul "+self.component["name"], e)
