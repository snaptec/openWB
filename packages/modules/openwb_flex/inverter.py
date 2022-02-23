#!/usr/bin/env python3

from helpermodules import log
from modules.common import modbus
from modules.common.component_state import InverterState
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_inverter_value_store
from modules.openwb_flex.versions import kit_counter_inverter_version_factory


def get_default_config() -> dict:
    return {
        "name": "PV-Kit flex",
        "type": "inverter",
        "id": None,
        "configuration": {
            "version": 2,
            "id": 116
        }
    }


class PvKitFlex:
    def __init__(self, device_id: int, component_config: dict, tcp_client: modbus.ModbusClient) -> None:
        self.component_config = component_config
        factory = kit_counter_inverter_version_factory(
            component_config["configuration"]["version"])
        self.__client = factory(component_config["configuration"]["id"], tcp_client)
        self.__tcp_client = tcp_client
        self.__store = get_inverter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self) -> None:
        """ liest die Werte des Moduls aus.
        """
        with self.__tcp_client:
            counter = self.__client.get_counter()
            powers, power = self.__client.get_power()

            version = self.component_config["configuration"]["version"]
            if version == 1:
                power = sum(powers)
            if power > 10:
                power = power*-1
            currents = self.__client.get_currents()

        log.MainLogger().debug("PV-Kit Leistung[W]: "+str(power))
        inverter_state = InverterState(
            power=power,
            counter=counter,
            currents=currents
        )
        self.__store.set(inverter_state)
