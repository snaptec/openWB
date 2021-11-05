#!/usr/bin/env python3
import time

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
        "name": "Alpha ESS Wechselrichter",
        "id": 0,
        "type": "inverter",
        "configuration":
        {
            "version": 1
        }
    }


class AlphaEssInverter(misc_component.MiscComponent):
    def __init__(self, device_id: int, component_config: dict, tcp_client: connect_tcp.ConnectTcp) -> None:
        try:
            super().__init__(device_id, component_config, tcp_client)
        except Exception as e:
            self.process_error(e)

    def update_values(self) -> None:
        try:
            log.MainLogger().debug("Komponente "+self.data["config"]["name"]+" auslesen.")
            reg_p = self.__version_factory(self.data["config"]["configuration"]["version"])
            power = self.__get_power(85, reg_p)

            topic_str = "openWB/set/system/device/" + str(self.device_id)+"/mmisc_component/"+str(self.data["config"]["id"])+"/"
            _, counter = self.sim_count.sim_count(power, topic=topic_str, data=self.data["simulation"], prefix="pv")
            self.value_store.set(power=power, counter=counter, currents=[0, 0, 0])
        except ModuleError as e:
            e.store_error(self.data["config"]["id"], "inverter", self.data["config"]["name"])
        except Exception as e:
            self.process_error(e)
        else:
            ModuleError("Kein Fehler.", ModuleErrorLevels.NO_ERROR).store_error(self.data["config"]["id"], "inverter", self.data["config"]["name"])

    def __version_factory(self, version: int) -> int:
        try:
            if version == 0:
                return 0x0012
            else:
                return 0x00A1
        except ModuleError as e:
            raise
        except Exception as e:
            self.process_error(e)

    def __get_power(self, sdmid: int, reg_p: int) -> int:
        try:
            p_reg = self.client.read_binary_registers_to_int(reg_p, sdmid, 32)
            if (p_reg < 0):
                p_reg = p_reg * -1
            time.sleep(0.1)
            p2_reg = self.client.read_binary_registers_to_int(0x041F, sdmid, 32)
            p3_reg = self.client.read_binary_registers_to_int(0x0423, sdmid, 32)
            p4_reg = self.client.read_binary_registers_to_int(0x0427, sdmid, 32)
            power = (p_reg + p2_reg + p3_reg + p4_reg) * -1
            log.MainLogger().debug("Alpha Ess Leistung: "+str(power)+", WR-Register: R1"+str(p_reg)+" R2 "+str(p2_reg)+" R3 "+str(p3_reg)+" R4 "+str(p4_reg))
            return power
        except ModuleError as e:
            raise
        except Exception as e:
            self.process_error(e)
