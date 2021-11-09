#!/usr/bin/env python3
import time

try:
    from ...helpermodules import log
    from ..common import connect_tcp
    from ..common.abstract_component import AbstractBat
    from ..common.component_state import BatState
except:
    from pathlib import Path
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from helpermodules import log
    from modules.common import connect_tcp
    from modules.common.abstract_component import AbstractBat
    from modules.common.component_state import BatState


def get_default_config() -> dict:
    return {
        "name": "Alpha ESS Speicher",
        "id": 0,
        "type": "bat",
        "configuration":
        {
            "version": 1
        }
    }


class AlphaEssBat(AbstractBat):
    def __init__(self, device_id: int, component_config: dict, tcp_client: connect_tcp.ConnectTcp) -> None:
        try:
            super().__init__(device_id, component_config, tcp_client)
        except Exception as e:
            self.process_error(e)

    def get_values(self) -> BatState:
        log.MainLogger().debug("Komponente "+self.data["config"]["name"]+" auslesen.")
        # keine Unterschiede zwischen den Versionen
        sdmid = 85

        time.sleep(0.1)
        voltage = self.client.read_binary_registers_to_int(0x0100, sdmid, 16)
        time.sleep(0.1)
        current = self.client.read_binary_registers_to_int(0x0101, sdmid, 16)

        power = voltage * current * -1 / 100
        log.MainLogger().debug("Alpha Ess Leistung[W]: "+str(power)+", Speicher-Register: Spannung[V] "+str(voltage)+" Strom[A] "+str(current))
        time.sleep(0.1)
        soc_reg = self.client.read_binary_registers_to_int(0x0102, sdmid, 16)
        soc = int(soc_reg * 0.1)

        topic_str = "openWB/set/system/device/" + str(self.device_id)+"/component/"+str(self.data["config"]["id"])+"/"
        imported, exported = self.sim_count.sim_count(power, topic=topic_str, data=self.data["simulation"], prefix="speicher")
        bat_state = BatState(
            power=power,
            soc=soc,
            imported=imported,
            exported=exported
        )
        return bat_state
