#!/usr/bin/env python3
import sys


try:
    from ...helpermodules import log
    from ...helpermodules import simcount
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

    from modules.common import lovato
    from modules.common import mpm3pm
    from modules.common import sdm630


def get_default() -> dict:
    return {
        "name": "EVU-Kit flex",
        "type": "counter",
        "id": None,
        "configuration":
            {
                "version": 2,
                "id": 115
            }
    }


class EvuKitFlex():
    def __init__(self, device_id: int, component_config: dict, tcp_client) -> None:
        try:
            self.data = {}
            self.data["config"] = component_config
            self.device_id = device_id
            version = self.data["config"]["configuration"]["version"]
            self.data["simulation"] = {}
            factory = self.__counter_factory(version)
            self.tcp_client = tcp_client
            self.counter = factory(self.data["config"], self.tcp_client)
            self.value_store = (store.ValueStoreFactory().get_storage("counter"))(self.data["config"]["id"])
            simcount_factory = simcount.SimCountFactory().get_sim_counter()
            self.sim_count = simcount_factory()
        except:
            log.MainLogger().exception("Fehler im Modul "+self.data["config"]["name"])

    def __counter_factory(self, version: int):
        try:
            if version == 0:
                return mpm3pm.Mpm3pm
            elif version == 1:
                return lovato.Lovato
            elif version == 2:
                return sdm630.Sdm630
        except:
            log.MainLogger().exception("Fehler im Modul "+self.data["config"]["name"])

    def read(self):
        """ liest die Werte des Moduls aus.
        """
        try:
            log.MainLogger().debug("Start kit reading")
            voltages = self.counter.get_voltage()
            power_per_phase, power_all = self.counter.get_power()
            frequency = self.counter.get_frequency()
            power_factors = self.counter.get_power_factor()

            version = self.data["config"]["configuration"]["version"]
            if version == 0:
                try:
                    if None not in power_per_phase and None not in voltages:
                        currents = [(power_per_phase[i]/voltages[i]) for i in range(3)]
                    else:
                        currents = [0, 0, 0]
                except:
                    log.MainLogger().exception("Fehler im Modul "+self.data["config"]["name"])
                    currents = [0, 0, 0]
                imported = self.counter.get_imported()
                exported = self.counter.get_exported()
            else:
                if version == 1:
                    if all(isinstance(x, (int, float)) for x in power_per_phase):
                        power_all = sum(power_per_phase)
                    else:
                        power_all = power_per_phase[0]  # enthält Fehlermeldung
                currents = self.counter.get_current()
                if None not in currents:
                    currents = [abs(currents[i]) for i in range(3)]
                else:
                    currents = [0, 0, 0]
                topic_str = "openWB/set/system/device/" + str(self.device_id)+"/component/"+str(self.data["config"]["id"])+"/"
                if power_all != None:
                    imported, exported = self.sim_count.sim_count(power_all, topic=topic_str, data=self.data["simulation"], prefix="bezug")
                else:
                    imported, exported = None, None
            log.MainLogger().debug("EVU-Kit Leistung[W]: "+str(power_all))
            self.tcp_client.close_connection()
            self.value_store.set(voltages=voltages, currents=currents, powers=power_per_phase,
                                 power_factors=power_factors, imported=imported, exported=exported, power_all=power_all, frequency=frequency)
            log.MainLogger().debug("Stop kit reading "+str(power_all))
        except:
            log.MainLogger().exception("Fehler im Modul "+self.data["config"]["name"])
