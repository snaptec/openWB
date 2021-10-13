#!/usr/bin/env python3
import sys


try:
    from ...helpermodules import log
    from ...helpermodules import simcount
    from ..common import connect_tcp
    from ..common import lovato
    from ..common import mpm3pm
    from ..common import sdm630
    from ..common import store
except:
    from pathlib import Path
    import os
    parentdir2 = str(Path(os.path.abspath(__file__)).parents[2])
    sys.path.insert(0, parentdir2)
    from helpermodules import log
    from helpermodules import simcount
    from modules.common import store
    from modules.common import connect_tcp
    from modules.common import lovato
    from modules.common import mpm3pm
    from modules.common import sdm630


class EvuKitFlex():
    def __init__(self, device_config: dict) -> None:
        try:
            self.data = {}
            self.data["config"] = device_config
            version = self.data["config"]["components"]["component0"]["configuration"]["version"]
            ip_address = self.data["config"]["configuration"]["ip_address"]
            port = self.data["config"]["configuration"]["port"]
            self.data["simulation"] = {}
            client = connect_tcp.ConnectTcp(self.data["config"]["name"], ip_address, port)
            factory = self.__counter_factory(version)
            self.counter = factory(self.data["config"], client)
            self.value_store = (store.ValueStoreFactory().get_storage("counter"))()
            simcount_factory = simcount.SimCountFactory().get_sim_counter()
            self.sim_count = simcount_factory()
        except Exception as e:
            log.MainLogger().error("Fehler im Modul "+self.data["config"]["components"]["component0"]["name"], e)

    def __counter_factory(self, version: int):
        try:
            if version == 0:
                return mpm3pm.Mpm3pm
            elif version == 1:
                return lovato.Lovato
            elif version == 2:
                return sdm630.Sdm630
        except Exception as e:
            log.MainLogger().error("Fehler im Modul "+self.data["config"]["components"]["component0"]["name"], e)

    def read(self):
        """ liest die Werte des Moduls aus.
        """
        try:
            voltages = self.counter.get_voltage()
            power_per_phase, power_all = self.counter.get_power()
            frequency = self.counter.get_frequency()
            power_factors = self.counter.get_power_factor()

            if self.data["config"]["components"]["component0"]["configuration"]["version"] == 0:
                try:
                    currents = [(power_per_phase[i]/voltages[i]) for i in range(3)]
                except Exception as e:
                    log.MainLogger().error("Fehler im Modul "+self.data["config"]["components"]["component0"]["name"], e)
                    currents = [0, 0, 0]
                imported = self.counter.get_imported()
                exported = self.counter.get_exported()
            else:
                currents = self.counter.get_current()
                currents = [abs(currents[i]) for i in range(3)]
                imported, exported = self.sim_count.sim_count(power_all, topic="openWB/set/system/devices/" +
                                                              str(self.data["config"]["id"])+"/components/"+str(self.data["config"]["components"]["component0"]["id"])+"/", data=self.data["simulation"], prefix="bezug")

            self.value_store.set(self.data["config"]["components"]["component0"]["id"], voltages=voltages, currents=currents, powers=power_per_phase, power_factors=power_factors, imported=imported, exported=exported, power_all=power_all, frequency=frequency)
        except Exception as e:
            log.MainLogger().error("Fehler im Modul "+self.data["config"]["components"]["component0"]["name"], e)
