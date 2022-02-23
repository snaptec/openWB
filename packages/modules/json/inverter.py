#!/usr/bin/env python3
import jq

from helpermodules import log
from modules.common import simcount
from modules.common.component_state import InverterState
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_inverter_value_store


def get_default_config() -> dict:
    return {
        "name": "Json Wechselrichter",
        "id": 0,
        "type": "inverter",
        "configuration": {
            "jq_power": ".power | .[1]",
            "jq_counter": ".counter"
        }
    }


class JsonInverter:
    def __init__(self, device_id: int, component_config: dict) -> None:
        self.__device_id = device_id
        self.component_config = component_config
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.simulation = {}
        self.__store = get_inverter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self, response) -> None:
        log.MainLogger().debug("Komponente "+self.component_config["name"]+" auslesen.")
        config = self.component_config["configuration"]

        power = float(jq.compile(config["jq_power"]).input(response).first())
        if power >= 0:
            power = power * -1
        if config["jq_counter"] == "":
            topic_str = "openWB/set/system/device/" + \
                str(self.__device_id)+"/component/" + \
                str(self.component_config["id"])+"/"
            _, counter = self.__sim_count.sim_count(
                power, topic=topic_str, data=self.simulation, prefix="pv")
        else:
            counter = jq.compile(config["jq_counter"]).input(response).first()

        inverter_state = InverterState(
            power=power,
            counter=counter
        )
        self.__store.set(inverter_state)
