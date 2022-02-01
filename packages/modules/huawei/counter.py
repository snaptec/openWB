#!/usr/bin/env python3
import time

from helpermodules import log
from modules.common import modbus
from modules.common import simcount
from modules.common.component_state import CounterState
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType
from modules.common.store import get_counter_value_store


def get_default_config() -> dict:
    return {
        "name": "Huawei Zähler",
        "id": 0,
        "type": "counter",
        "configuration": {}
    }


class HuaweiCounter:
    def __init__(self, device_id: int, component_config: dict, tcp_client: modbus.ModbusClient, modbus_id: int) -> None:
        self.__device_id = device_id
        self.component_config = component_config
        self.__modbus_id = modbus_id
        self.__tcp_client = tcp_client
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.simulation = {}
        self.__store = get_counter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self):
        log.MainLogger().debug("Komponente "+self.component_config["name"]+" auslesen.")
        time.sleep(0.1)
        power = self.__tcp_client.read_holding_registers(37113, ModbusDataType.INT_32, unit=self.__modbus_id) * -1
        time.sleep(0.1)
        currents = [val / -100 for val in self.__tcp_client.read_holding_registers(
            37107, [ModbusDataType.INT_32] * 3, unit=self.__modbus_id)]

        topic_str = "openWB/set/system/device/{}/component/{}/".format(
            self.__device_id, self.component_config["id"]
        )
        imported, exported = self.__sim_count.sim_count(
            power,
            topic=topic_str,
            data=self.simulation,
            prefix="bezug"
        )

        counter_state = CounterState(
            currents=currents,
            imported=imported,
            exported=exported,
            power=power
        )
        self.__store.set(counter_state)
