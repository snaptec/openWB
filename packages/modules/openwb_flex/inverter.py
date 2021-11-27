#!/usr/bin/env python3

from helpermodules import log
from modules.common import modbus
from modules.common.component_state import InverterState
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_inverter_value_store
from modules.openwb_flex.versions import kit_version_factory


def get_default_config() -> dict:
    return {
        "name": "PV-Kit flex",
        "type": "inverter",
        "id": None,
        "configuration":
            {
                "version": 2,
                "id": 116
            }
    }


class PvKitFlex:
    def __init__(self, device_id: int, component_config: dict, tcp_client: modbus.ModbusClient) -> None:
        self.component_config = component_config
        factory = kit_version_factory(
            component_config["configuration"]["version"])
        self.__client = factory(component_config["configuration"]["id"],
                                tcp_client)
        self.__tcp_client = tcp_client
        self.__store = get_inverter_value_store(component_config["id"])
        self.component_info = ComponentInfo(self.component_config["id"],
                                            self.component_config["name"],
                                            self.component_config["type"])

    def update(self) -> None:
        """ liest die Werte des Moduls aus.
        """
        try:
            counter = self.__client.get_counter()
            power_per_phase, power_all = self.__client.get_power()

            version = self.component_config["configuration"]["version"]
            if version == 1:
                power_all = sum(power_per_phase)
            if power_all > 10:
                power_all = power_all*-1
            currents = self.__client.get_current()
        finally:
            self.__tcp_client.close_connection()

        log.MainLogger().debug("PV-Kit Leistung[W]: "+str(power_all))
        inverter_state = InverterState(
            power=power_all,
            counter=counter,
            currents=currents
        )
        self.__store.set(inverter_state)
