#!/usr/bin/env python3
import jq

from helpermodules import log
from modules.common import simcount
from modules.common.component_state import CounterState
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_counter_value_store


def get_default_config() -> dict:
    return {
        "name": "Json Zähler",
        "id": 0,
        "type": "counter",
        "configuration": {
            "jq_power": ".power | .[1]",
            "jq_imported": ".imported",
            "jq_exported": ".exported"
        }
    }


class JsonCounter:
    def __init__(self, device_id: int, component_config: dict) -> None:
        self.__device_id = device_id
        self.component_config = component_config
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.simulation = {}
        self.__store = get_counter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self, response):
        log.MainLogger().debug("Komponente "+self.component_config["name"]+" auslesen.")
        config = self.component_config["configuration"]

        power = jq.compile(config["jq_power"]).input(response).first()
        if config["jq_imported"] == "" or config["jq_exported"] == "":
            topic_str = "openWB/set/system/device/{}/component/{}/".format(
                self.__device_id, self.component_config["id"]
            )
            imported, exported = self.__sim_count.sim_count(
                power,
                topic=topic_str,
                data=self.simulation,
                prefix="bezug"
            )
        else:
            imported = jq.compile(config["jq_imported"]).input(response).first()
            exported = jq.compile(config["jq_exported"]).input(response).first()

        counter_state = CounterState(
            imported=imported,
            exported=exported,
            power=power
        )
        self.__store.set(counter_state)
