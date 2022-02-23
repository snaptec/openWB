#!/usr/bin/env python3
import jq

from helpermodules import log
from modules.common import simcount
from modules.common.component_state import BatState
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_bat_value_store


def get_default_config() -> dict:
    return {
        "name": "Json Speicher",
        "id": 0,
        "type": "bat",
        "configuration": {
            "jq_power": ".power | .[1]",
            "jq_soc": ".soc"
        }
    }


class JsonBat:
    def __init__(self, device_id: int, component_config: dict) -> None:
        self.__device_id = device_id
        self.component_config = component_config
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.__simulation = {}
        self.__store = get_bat_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self, response) -> None:
        log.MainLogger().debug("Komponente "+self.component_config["name"]+" auslesen.")
        config = self.component_config["configuration"]

        power = jq.compile(config["jq_power"]).input(response).first()
        if config["jq_soc"] != "":
            soc = jq.compile(config["jq_soc"]).input(response).first()
        else:
            soc = 0

        topic_str = "openWB/set/system/device/" + str(
            self.__device_id)+"/component/"+str(self.component_config["id"])+"/"
        imported, exported = self.__sim_count.sim_count(
            power, topic=topic_str, data=self.__simulation, prefix="speicher"
        )

        bat_state = BatState(
            power=power,
            soc=soc,
            imported=imported,
            exported=exported
        )
        self.__store.set(bat_state)
