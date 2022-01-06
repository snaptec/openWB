#!/usr/bin/env python3
from helpermodules import log
from modules.common import modbus
from modules.common import simcount
from modules.common.component_state import CounterState
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType
from modules.common.store import get_counter_value_store


def get_default_config() -> dict:
    return {
        "name": "Sungrow Zähler",
        "id": 0,
        "type": "counter",
        "configuration":
        {
            "version": 1
        }
    }


class SungrowCounter:
    def __init__(self, device_id: int, component_config: dict, tcp_client: modbus.ModbusClient) -> None:
        self.__device_id = device_id
        self.component_config = component_config
        self.__tcp_client = tcp_client
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.__simulation = {}
        self.__store = get_counter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self):
        log.MainLogger().debug("Komponente "+self.component_config["name"]+" auslesen.")
        unit = 1
        if self.component_config["configuration"]["version"] == 1:
            power_all = self.__tcp_client.read_input_registers(5082, ModbusDataType.INT_32, unit=unit)
        else:
            power_all = self.__tcp_client.read_input_registers(13009, ModbusDataType.INT_32, unit=unit) * -1

        topic_str = "openWB/counter/" + str(self.component_config["id"]) + "/get/"
        imported, exported = self.__sim_count.sim_count(
            power_all,
            topic=topic_str,
            data=self.__simulation,
            prefix="bezug"
        )

        counter_state = CounterState(
            imported=imported,
            exported=exported,
            power_all=power_all
        )
        log.MainLogger().debug("Sungrow Leistung[W]: " + str(counter_state.power_all))
        self.__store.set(counter_state)
