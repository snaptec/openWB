#!/usr/bin/env python3
from helpermodules import log
from modules.common import modbus
from modules.common.component_state import CounterState
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType
from modules.common.store import get_counter_value_store


def get_default_config() -> dict:
    return {
        "name": "Victron Zähler",
        "id": 0,
        "type": "counter",
        "configuration":
        {
            "modbus_id": 1
        }
    }


class VictronCounter:
    def __init__(self, device_id: int, component_config: dict, tcp_client: modbus.ModbusClient) -> None:
        self.component_config = component_config
        self.__tcp_client = tcp_client
        self.__store = get_counter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self):
        log.MainLogger().debug("Komponente "+self.component_config["name"]+" auslesen.")
        unit = self.component_config["configuration"]["modbus_id"]
        power_all = sum(self.__tcp_client.read_holding_registers(2600, [ModbusDataType.INT_16]*3, unit=unit))
        currents_voltages = [val / 10
                             for val in self.__tcp_client.read_holding_registers(
                                 2616, [ModbusDataType.INT_16] * 6, unit=unit)]
        voltages = [currents_voltages[0], currents_voltages[2], currents_voltages[4]]
        currents = [currents_voltages[1], currents_voltages[3], currents_voltages[5]]
        imported = sum(self.__tcp_client.read_holding_registers(2622, [ModbusDataType.UINT_32]*3, unit=unit)) * 10
        exported = sum(self.__tcp_client.read_holding_registers(2628, [ModbusDataType.UINT_32]*3, unit=unit)) * 10

        counter_state = CounterState(
            voltages=voltages,
            currents=currents,
            imported=imported,
            exported=exported,
            power_all=power_all
        )
        log.MainLogger().debug("Victron Leistung[W]: " + str(counter_state.power_all))
        self.__store.set(counter_state)
