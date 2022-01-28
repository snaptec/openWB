#!/usr/bin/env python3

from helpermodules import log
from modules.common import modbus
from modules.common import simcount
from modules.common.component_state import InverterState
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType, Endian
from modules.common.store import get_inverter_value_store


def get_default_config() -> dict:
    return {
        "name": "Sungrow Wechselrichter",
        "id": 0,
        "type": "inverter",
        "configuration": {}
    }


class SungrowInverter:
    def __init__(self, device_id: int, component_config: dict, tcp_client: modbus.ModbusClient) -> None:
        self.__device_id = device_id
        self.component_config = component_config
        self.__tcp_client = tcp_client
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.__simulation = {}
        self.__store = get_inverter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self) -> None:
        log.MainLogger().debug("Komponente "+self.component_config["name"]+" auslesen.")
        with self.__tcp_client:
            power = self.__tcp_client.read_input_registers(5016, ModbusDataType.INT_32,
                                                           wordorder=Endian.Little, unit=1) * -1

        topic_str = "openWB/set/system/device/" + \
            str(self.__device_id)+"/component/" + \
            str(self.component_config["id"])+"/"
        _, counter = self.__sim_count.sim_count(
            power, topic=topic_str, data=self.__simulation, prefix="pv")

        inverter_state = InverterState(
            power=power,
            counter=counter
        )
        self.__store.set(inverter_state)
