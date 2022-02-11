#!/usr/bin/env python3
from pymodbus.constants import Endian

from helpermodules import log
from modules.common import modbus
from modules.common import simcount
from modules.common.component_state import CounterState
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType
from modules.common.store import get_counter_value_store


def get_default_config() -> dict:
    return {
        "name": "Carlo Gavazzi Zähler",
        "id": 0,
        "type": "counter",
        "configuration": {}
    }


class CarloGavazziCounter:
    def __init__(self, device_id: int, component_config: dict, tcp_client: modbus.ModbusClient) -> None:
        self.__device_id = device_id
        self.component_config = component_config
        self.__tcp_client = tcp_client
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.__simulation = {}
        self.__store = get_counter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self):
        unit = 1
        log.MainLogger().debug(
            "Komponente "+self.component_config["name"]+" auslesen.")
        with self.__tcp_client:
            voltages = [val / 10 for val in self.__tcp_client.read_input_registers(
                0x00, [ModbusDataType.INT_32] * 3, wordorder=Endian.Little, unit=unit)]
            powers = [val / 10 for val in self.__tcp_client.read_input_registers(
                0x12, [ModbusDataType.INT_32] * 3, wordorder=Endian.Little, unit=unit)]
            power = sum(powers)
            currents = [abs(val / 1000) for val in self.__tcp_client.read_input_registers(
                0x0C, [ModbusDataType.INT_32] * 3, wordorder=Endian.Little, unit=unit)]
            frequency = self.__tcp_client.read_input_registers(0x33, ModbusDataType.INT_16, unit=unit) / 10
            if frequency > 100:
                frequency = frequency / 10

        topic_str = "openWB/set/system/device/{}/component/{}/".format(self.__device_id, self.component_config["id"])
        imported, exported = self.__sim_count.sim_count(
            power,
            topic=topic_str,
            data=self.__simulation,
            prefix="bezug"
        )

        counter_state = CounterState(
            voltages=voltages,
            currents=currents,
            powers=powers,
            imported=imported,
            exported=exported,
            power=power,
            frequency=frequency
        )
        log.MainLogger().debug("Carlo Gavazzi Leistung[W]: " + str(counter_state.power))
        self.__store.set(counter_state)
