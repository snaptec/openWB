#!/usr/bin/env python3

from helpermodules import log
from modules.common import modbus
from modules.common.component_state import InverterState
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType, Endian
from modules.common.store import get_inverter_value_store


def get_default_config() -> dict:
    return {
        "name": "Solax Wechselrichter",
        "id": 0,
        "type": "inverter",
        "configuration": {}
    }


class SolaxInverter:
    def __init__(self, device_id: int, component_config: dict, tcp_client: modbus.ModbusClient) -> None:
        self.component_config = component_config
        self.__tcp_client = tcp_client
        self.__store = get_inverter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self) -> None:
        log.MainLogger().debug("Komponente "+self.component_config["name"]+" auslesen.")
        with self.__tcp_client:
            power_temp = self.__tcp_client.read_input_registers(10, [ModbusDataType.UINT_16] * 2)
            power = sum(power_temp) * -1
            counter = self.__tcp_client.read_input_registers(82, ModbusDataType.UINT_32, wordorder=Endian.Little) * 100

        inverter_state = InverterState(
            power=power,
            counter=counter
        )
        self.__store.set(inverter_state)
