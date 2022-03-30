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
        "name": "Alpha ESS Wechselrichter",
        "id": 0,
        "type": "inverter",
        "configuration": {
            "version": 1
        }
    }


class AlphaEssInverter:
    def __init__(self, device_id: int, component_config: dict, tcp_client: modbus.ModbusClient) -> None:
        self.__device_id = device_id
        self.component_config = component_config
        self.__tcp_client = tcp_client
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.__simulation = {}
        self.__store = get_inverter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self, unit_id: int) -> None:
        log.MainLogger().debug(
            "Komponente "+self.component_config["name"]+" auslesen.")
        reg_p = self.__version_factory(
            self.component_config["configuration"]["version"])
        power = self.__get_power(unit_id, reg_p)

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

    def __version_factory(self, version: int) -> int:
        return 0x0012 if version == 0 else 0x00A1

    def __get_power(self, unit: int, reg_p: int) -> int:
        with self.__tcp_client:
            powers = [
                self.__tcp_client.read_holding_registers(address, ModbusDataType.INT_32, unit=unit)
                for address in [reg_p, 0x041F, 0x0423, 0x0427]
            ]
        powers[0] = abs(powers[0])
        power = sum(powers) * -1
        log.MainLogger().debug("Alpha Ess Leistung: "+str(power)+", WR-Register: " + str(powers))
        return power
