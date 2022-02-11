#!/usr/bin/env python3
import time

from helpermodules import log
from modules.common import modbus
from modules.common import simcount
from modules.common.component_state import BatState
from modules.common.modbus import ModbusDataType
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_bat_value_store


def get_default_config() -> dict:
    return {
        "name": "Alpha ESS Speicher",
        "id": 0,
        "type": "bat",
        "configuration": {
            "version": 1
        }
    }


class AlphaEssBat:
    def __init__(self, device_id: int, component_config: dict, tcp_client: modbus.ModbusClient) -> None:
        self.__device_id = device_id
        self.component_config = component_config
        self.__tcp_client = tcp_client
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.__simulation = {}
        self.__store = get_bat_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self, unit_id: int) -> None:
        log.MainLogger().debug("Komponente "+self.component_config["name"]+" auslesen.")
        # keine Unterschiede zwischen den Versionen

        with self.__tcp_client:
            time.sleep(0.1)
            voltage = self.__tcp_client.read_holding_registers(0x0100, ModbusDataType.INT_16, unit=unit_id)
            time.sleep(0.1)
            current = self.__tcp_client.read_holding_registers(0x0101, ModbusDataType.INT_16, unit=unit_id)

            power = voltage * current * -1 / 100
            log.MainLogger().debug(
                "Alpha Ess Leistung[W]: %f, Speicher-Register: Spannung[V]: %f, Strom[A]: %f" %
                (power, voltage, current)
            )
            time.sleep(0.1)
            soc_reg = self.__tcp_client.read_holding_registers(0x0102, ModbusDataType.INT_16, unit=unit_id)
            soc = int(soc_reg * 0.1)

        topic_str = "openWB/set/system/device/" + str(
            self.__device_id)+"/component/"+str(self.component_config["id"])+"/"
        imported, exported = self.__sim_count.sim_count(
            power, topic=topic_str, data=self.__simulation, prefix="speicher"
        )
        bat_state = BatState(
            power=power,
            soc=soc,
            imported=imported,
            exported=exported
        )
        self.__store.set(bat_state)
