#!/usr/bin/env python3
import sys


try:
    from ...helpermodules import log
    from ..common import connect_tcp
    from ..common import misc_component
    from ..common.module_error import ModuleError, ModuleErrorLevels
except:
    from pathlib import Path
    import os
    parentdir2 = str(Path(os.path.abspath(__file__)).parents[2])
    sys.path.insert(0, parentdir2)
    from helpermodules import log
    from modules.common import connect_tcp
    from modules.common import misc_component
    from modules.common.module_error import ModuleError, ModuleErrorLevels


def get_default_config() -> dict:
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


class EvuKitFlex(misc_component.MiscComponent):
    def __init__(self, device_id: int, component_config: dict, tcp_client: connect_tcp.ConnectTcp) -> None:
        try:
            client = self.kit_version_factory(component_config["configuration"]["version"], component_config["configuration"]["id"], tcp_client)
            super().__init__(device_id, component_config, client)
            self.tcp_client = tcp_client
        except Exception as e:
            self.process_error(e)

    def update_values(self) -> None:
        """ liest die Werte des Moduls aus.
        """
        try:
            log.MainLogger().debug("Start kit reading")
            voltages = self.client.get_voltage()
            power_per_phase, power_all = self.client.get_power()
            frequency = self.client.get_frequency()
            power_factors = self.client.get_power_factor()

            version = self.data["config"]["configuration"]["version"]
            if version == 0:
                currents = [(power_per_phase[i]/voltages[i]) for i in range(3)]
                imported = self.client.get_imported()
                exported = self.client.get_exported()
            else:
                if version == 1:
                    power_all = sum(power_per_phase)
                currents = self.client.get_current()
                currents = [abs(currents[i]) for i in range(3)]
                topic_str = "openWB/set/system/device/" + str(self.device_id)+"/mmisc_component/"+str(self.data["config"]["id"])+"/"
                imported, exported = self.sim_count.sim_count(power_all, topic=topic_str, data=self.data["simulation"], prefix="bezug")
            log.MainLogger().debug("EVU-Kit Leistung[W]: "+str(power_all))
            self.tcp_client.close_connection()
            self.value_store.set(voltages=voltages, currents=currents, powers=power_per_phase,
                                 power_factors=power_factors, imported=imported, exported=exported, power_all=power_all, frequency=frequency)
            log.MainLogger().debug("Stop kit reading "+str(power_all))
        except ModuleError as e:
            e.store_error(self.data["config"]["id"], "counter", self.data["config"]["name"])
        except Exception as e:
            self.process_error(e)
        else:
            ModuleError("Kein Fehler.", ModuleErrorLevels.NO_ERROR).store_error(self.data["config"]["id"], "counter", self.data["config"]["name"])
