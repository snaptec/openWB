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
        "name": "Victron Wechselrichter",
        "id": 0,
        "type": "inverter",
        "configuration": {
            "ip_address": "192.168.193.15",
            "modbus_id": 100,
            "mppt": False
        }
    }


class VictronInverter:
    def __init__(self, device_id: int, component_config: dict) -> None:
        self.__device_id = device_id
        self.component_config = component_config
        ip_address = self.component_config["configuration"]["ip_address"]
        self.__tcp_client = modbus.ModbusClient(ip_address, 502)
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.__simulation = {}
        self.__store = get_inverter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self) -> None:
        log.MainLogger().debug("Komponente "+self.component_config["name"]+" auslesen.")
        modbus_id = self.component_config["configuration"]["modbus_id"]

        if self.component_config["configuration"]["mppt"]:
            power = self.__tcp_client.read_holding_registers(789, ModbusDataType.UINT_16, unit=modbus_id) / -10
        else:
            # Adresse 808-810 ac output connected pv
            # Adresse 811-813 ac input connected pv
            # Adresse 850 mppt Leistung
            power_temp1 = self.__tcp_client.read_holding_registers(808, [ModbusDataType.UINT_16]*6, unit=100)
            power_temp2 = self.__tcp_client.read_holding_registers(850, ModbusDataType.UINT_16, unit=100)
            power = (sum(power_temp1)+power_temp2) * -1

        topic_str = "openWB/set/system/device/" + str(self.__device_id)+"/component/" + \
            str(self.component_config["id"])+"/"
        _, counter = self.__sim_count.sim_count(power, topic=topic_str, data=self.__simulation, prefix="pv")
        inverter_state = InverterState(
            power=power,
            counter=counter
        )
        self.__store.set(inverter_state)
