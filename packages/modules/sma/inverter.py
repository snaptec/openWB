#!/usr/bin/env python3

from helpermodules import log
from modules.common.component_state import InverterState
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_inverter_value_store


def get_default_config() -> dict:
    return {
        "name": "SMA Smarthome Manager Wechselrichter",
        "id": 0,
        "type": "inverter",
        "configuration":
        {
            "serials": None
        }
    }


class SmaInverter:
    def __init__(self, component_config: dict) -> None:
        self.component_config = component_config
        self.__store = get_inverter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self, sma_data) -> None:
        log.MainLogger().debug(
            "Komponente "+self.component_config["name"]+" auslesen.")

        # don't know what P,Q and S means:
        # http://en.wikipedia.org/wiki/AC_power or http://de.wikipedia.org/wiki/Scheinleistung
        # thd = Total_Harmonic_Distortion http://de.wikipedia.org/wiki/Total_Harmonic_Distortion
        # cos phi is always positive, no matter what quadrant
        inverter_state = InverterState(
            power=-int(sma_data['psupply']),
            counter=sma_data['psupplycounter'] * 1000
        )
        self.__store.set(inverter_state)
