#!/usr/bin/env python3
from helpermodules import log
from modules.common import modbus
from modules.common.component_state import CounterState
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType, Endian
from modules.common.store import get_counter_value_store


def get_default_config() -> dict:
    return {
        "name": "Solax Zähler",
        "id": 0,
        "type": "counter",
        "configuration": {}
    }


class SolaxCounter:
    def __init__(self, device_id: int, component_config: dict, tcp_client: modbus.ModbusClient) -> None:
        self.component_config = component_config
        self.__tcp_client = tcp_client
        self.__store = get_counter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self):
        log.MainLogger().debug("Komponente "+self.component_config["name"]+" auslesen.")
        with self.__tcp_client:
            power = self.__tcp_client.read_input_registers(70, ModbusDataType.INT_32, wordorder=Endian.Little) * -1
            frequency = self.__tcp_client.read_input_registers(7, ModbusDataType.UINT_16) / 100
            try:
                powers = [-value for value in self.__tcp_client.read_input_registers(
                    130, [ModbusDataType.INT_32] * 3, wordorder=Endian.Little
                )]
            except Exception:
                powers = None
            exported, imported = [value * 10
                                  for value in self.__tcp_client.read_input_registers(
                                      72, [ModbusDataType.UINT_32] * 2, wordorder=Endian.Little
                                  )]

        counter_state = CounterState(
            imported=imported,
            exported=exported,
            power=power,
            powers=powers,
            frequency=frequency
        )
        log.MainLogger().debug("Solax Leistung[W]: " + str(counter_state.power))
        self.__store.set(counter_state)
