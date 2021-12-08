#!/usr/bin/env python3

from helpermodules import log
from modules.common import modbus
from modules.common import simcount
from modules.common.component_state import InverterState
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType
from modules.common.store import get_inverter_value_store


def get_default_config() -> dict:
    return {
        "name": "Siemens Wechselrichter",
        "id": 0,
        "type": "inverter",
        "configuration":
        {
            "ip_address": "192.168.0.12"
        }
    }


class SiemensInverter:
    def __init__(self, device_id: int, component_config: dict) -> None:
        self.__device_id = device_id
        self.component_config = component_config
        ip_address = component_config["configuration"]["ip_address"]
        self.__tcp_client = modbus.ModbusClient(ip_address, 502)
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.__simulation = {}
        self.__store = get_inverter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self) -> None:
        log.MainLogger().debug("Komponente "+self.component_config["name"]+" auslesen.")
        power = self.__tcp_client.read_holding_registers(16, ModbusDataType.INT_32, unit=1) * -1

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
