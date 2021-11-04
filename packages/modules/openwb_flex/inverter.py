#!/usr/bin/env python3


try:
    from ...helpermodules import log
    from ..common import connect_tcp
    from ..common import misc_component
    from ..common.module_error import ModuleError, ModuleErrorLevels
except:
    from pathlib import Path
    import os
    import sys
    parentdir2 = str(Path(os.path.abspath(__file__)).parents[2])
    sys.path.insert(0, parentdir2)
    from helpermodules import log
    from modules.common import connect_tcp
    from modules.common import misc_component
    from modules.common.module_error import ModuleError, ModuleErrorLevels


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


class PvKitFlex(misc_component.MiscComponent):
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
            counter = self.client.get_counter()
            power_per_phase, power_all = self.client.get_power()

            version = self.data["config"]["configuration"]["version"]
            if version == 1:
                power_all = sum(power_per_phase)
            if (power_all > 10):
                power_all = power_all*-1
            currents = self.client.get_current()

            log.MainLogger().debug("PV-Kit Leistung[W]: "+str(power_all))
            self.tcp_client.close_connection()
            self.value_store.set(power=power_all, counter=counter, currents=currents)
        except ModuleError as e:
            e.store_error(self.data["config"]["id"], "inverter", self.data["config"]["name"])
        except Exception as e:
            self.process_error(e)
        else:
            ModuleError("Kein Fehler.", ModuleErrorLevels.NO_ERROR).store_error(self.data["config"]["id"], "inverter", self.data["config"]["name"])
