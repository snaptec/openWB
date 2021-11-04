#!/usr/bin/env python3


try:
    from ...helpermodules import log
    from ..common import lovato
    from ..common import mpm3pm
    from ..common import sdm630
    from ..common import store
except:
    from pathlib import Path
    import os
    import sys
    parentdir2 = str(Path(os.path.abspath(__file__)).parents[2])
    sys.path.insert(0, parentdir2)
    from helpermodules import log
    from modules.common import lovato
    from modules.common import mpm3pm
    from modules.common import sdm630
    from modules.common import store


def get_default_config() -> dict:
    return {
        "name": "PV-Kit flex",
        "type": "inverter",
        "id": None,
        "configuration":
            {
                "version": 2,
                "id": 116
            }
    }


class PvKitFlex():
    def __init__(self, device_id: int, component_config: dict, tcp_client) -> None:
        try:
            self.data = {}
            self.data["config"] = component_config
            self.device_id = device_id
            version = self.data["config"]["configuration"]["version"]
            self.data["simulation"] = {}
            factory = self.__inverter_factory(version)
            self.tcp_client = tcp_client
            self.counter = factory(self.data["config"], self.tcp_client)
            self.value_store = (store.ValueStoreFactory().get_storage("inverter"))(self.data["config"]["id"])
        except:
            log.MainLogger().exception("Fehler im Modul "+self.data["config"]["name"])

    def __inverter_factory(self, version: int):
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
            counter = self.counter.get_counter()
            power_per_phase, power_all = self.counter.get_power()

            version = self.data["config"]["configuration"]["version"]
            if version == 1:
                if all(isinstance(x, (int, float)) for x in power_per_phase):
                    power_all = sum(power_per_phase)
                else:
                    power_all = power_per_phase[0] # enthält Fehlermeldung
            if isinstance(power_all, (int, float)) and (version == 1 or version == 2):
                if (power_all > 10):
                    power_all = power_all*-1
            currents = self.counter.get_current()

            log.MainLogger().debug("PV-Kit Leistung[W]: "+str(power_all))
            self.tcp_client.close_connection()
            self.value_store.set(power=power_all, counter=counter, currents=currents)
        except Exception as e:
            log.MainLogger().exception("Fehler im Modul "+self.data["config"]["name"])
