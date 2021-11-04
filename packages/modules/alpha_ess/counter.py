#!/usr/bin/env python3
import time
from typing import List, Tuple

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
        "name": "Alpha ESS Zähler",
        "id": None,
        "type": "counter",
        "configuration":
        {
            "version": 1
        }
    }


class AlphaEssCounter(misc_component.MiscComponent):
    def __init__(self, device_id: int, component_config: dict, tcp_client: connect_tcp.ConnectTcp) -> None:
        try:
            super().__init__(device_id, component_config, tcp_client)
            self.tcp_client = tcp_client
        except Exception as e:
            self.process_error(e)

    def update_values(self):
        try:
            log.MainLogger().debug("Komponente "+self.data["config"]["name"]+" auslesen.")
            time.sleep(0.1)
            factory_method = self.__update_values_factory(self.data["config"]["configuration"]["version"])
            power_all, exported, imported, currents = factory_method(sdmid=85)

            self.value_store.set(voltages=[0, 0, 0], currents=currents, powers=[0, 0, 0], power_factors=[0, 0, 0], imported=imported, exported=exported, power_all=power_all, frequency=50)
        except ModuleError as e:
            e.store_error(self.data["config"]["id"], "counter", self.data["config"]["name"])
        except Exception as e:
            self.process_error(e)
        else:
            ModuleError("Kein Fehler.", ModuleErrorLevels.NO_ERROR).store_error(self.data["config"]["id"], "counter", self.data["config"]["name"])

    def __update_values_factory(self, version: int):
        try:
            if version == 0:
                return self.__update_values_before_v123
            else:
                return self.__update_values_since_v123
        except ModuleError as e:
            raise
        except Exception as e:
            self.process_error(e)

    def __update_values_before_v123(self, sdmid: int) -> Tuple[float, float, float, List[float]]:
        try:
            power_all = self.client.read_binary_registers_to_int(0x0006, sdmid, 32)
            exported = self.client.read_binary_registers_to_int(0x0008, sdmid, 32) * 10
            imported = self.client.read_binary_registers_to_int(0x000A, sdmid, 32) * 10
            currents = []
            regs = [0x0000, 0x0002, 0x0004]
            for register in regs:
                value = self.client.read_binary_registers_to_int(register, sdmid, 32) / 230
                currents.append(value)
            return power_all, exported, imported, currents
        except ModuleError as e:
            raise
        except Exception as e:
            self.process_error(e)

    def __update_values_since_v123(self, sdmid: int) -> Tuple[float, float, float, List[float]]:
        try:
            power_all = self.client.read_binary_registers_to_int(0x0021, sdmid, 32)
            exported = self.client.read_binary_registers_to_int(0x0010, sdmid, 32) * 10
            imported = self.client.read_binary_registers_to_int(0x0012, sdmid, 32) * 10
            currents = []
            regs = [0x0017, 0x0018, 0x0019]
            for register in regs:
                value = self.client.read_binary_registers_to_int(register, sdmid, 16) / 1000
                currents.append(value)
            return power_all, exported, imported, currents
        except ModuleError as e:
            raise
        except Exception as e:
            self.process_error(e)
