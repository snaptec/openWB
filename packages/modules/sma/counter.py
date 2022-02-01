#!/usr/bin/env python3
from math import copysign


from helpermodules import log
from modules.common.component_state import CounterState
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_counter_value_store


def get_default_config() -> dict:
    return {
        "name": "SMA Smarthome Manager Zähler",
        "id": 0,
        "type": "counter",
        "configuration":
        {
            "serials": None
        }
    }


class SmaCounter:
    def __init__(self, component_config: dict) -> None:
        self.component_config = component_config
        self.__store = get_counter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self, sma_data):
        log.MainLogger().debug(
            "Komponente "+self.component_config["name"]+" auslesen.")

        def get_power(phase_str: str = ""):
            # "consume" and "supply" are always >= 0. Thus we need to check both "supply" and "consume":
            power_import = sma_data["p" + phase_str + "consume"]
            return -sma_data["p" + phase_str + "supply"] if power_import == 0 else power_import

        powers = [get_power(str(phase)) for phase in range(1, 4)]

        self.__store.set(CounterState(
            imported=sma_data['pconsumecounter'] * 1000,
            exported=sma_data['psupplycounter'] * 1000,
            power=get_power(),
            voltages=[sma_data["u" + str(phase)] for phase in range(1, 4)],
            # currents reported are always absolute values. We get the sign from power:
            currents=[copysign(sma_data["i" + str(phase)], powers[phase - 1]) for phase in range(1, 4)],
            powers=powers,
            power_factors=[sma_data["cosphi" + str(phase)] for phase in range(1, 4)],
            frequency=sma_data.get("frequency")
        ))
