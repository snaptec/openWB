#!/usr/bin/env python3
import time

try:
    from ...helpermodules import log
    from ..common import modbus
    from ..common.abstract_component import AbstractBat
    from ..common.component_state import BatState
except (ImportError, ValueError):
    from helpermodules import log
    from modules.common import modbus
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
    def __init__(self, device_id: int, component_config: dict, tcp_client: modbus.ModbusClient) -> None:
        try:
            super().__init__(device_id, component_config, tcp_client)
        except Exception as e:
            self.process_error(e)

    def get_values(self) -> BatState:
        log.MainLogger().debug("Komponente "+self.data["config"]["name"]+" auslesen.")
        # keine Unterschiede zwischen den Versionen
        sdmid = 85

        time.sleep(0.1)
        voltage = self.client.read_holding_registers(0x0100, modbus.ModbusDataType.INT_16, unit=sdmid)
        time.sleep(0.1)
        current = self.client.read_holding_registers(0x0101, modbus.ModbusDataType.INT_16, unit=sdmid)

        power = voltage * current * -1 / 100
        log.MainLogger().debug(
            "Alpha Ess Leistung[W]: %f, Speicher-Register: Spannung[V]: %f, Strom[A]: %f" % (power, voltage, current)
        )
        time.sleep(0.1)
        soc_reg = self.client.read_holding_registers(0x0102, modbus.ModbusDataType.INT_16, unit=sdmid)
        soc = int(soc_reg * 0.1)

        topic_str = "openWB/set/system/device/" + str(self.device_id)+"/component/"+str(self.data["config"]["id"])+"/"
        imported, exported = self.sim_count.sim_count(
            power, topic=topic_str, data=self.data["simulation"], prefix="speicher"
        )
        bat_state = BatState(
            power=power,
            soc=soc,
            imported=imported,
            exported=exported
        )
        return bat_state
