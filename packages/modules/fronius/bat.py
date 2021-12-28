#!/usr/bin/env python3
import requests

from helpermodules import log
from modules.common import simcount
from modules.common.component_state import BatState
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_bat_value_store


def get_default_config() -> dict:
    return {
        "name": "Fronius Speicher",
        "id": 0,
        "type": "bat",
        "configuration":
        {
            "gen24": 0
        }
    }


class FroniusBat:
    def __init__(self, device_id: int, component_config: dict, device_config: dict) -> None:
        self.__device_id = device_id
        self.component_config = component_config
        self.device_config = device_config
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.__simulation = {}
        self.__store = get_bat_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self, bat: bool) -> None:
        log.MainLogger().debug("Komponente "+self.component_config["name"]+" auslesen.")
        gen24 = self.component_config["configuration"]["gen24"]
        meter_id = self.device_config["meter_id"]

        response = requests.get(
            'http://' + self.device_config["ip_address"] + '/solar_api/v1/GetPowerFlowRealtimeData.fcgi',
            params=(('Scope', 'System'),),
            timeout=5)
        response.raise_for_status()
        resp_json = response.json()
        try:
            power = int(resp_json["Body"]["Data"]["Site"]["P_Akku"]) * -1
        except TypeError:
            # Wenn WR aus bzw. im Standby (keine Antwort), ersetze leeren Wert durch eine 0.
            power = 0

        try:
            if gen24 == 1:
                soc = float(resp_json["Body"]["Data"][meter_id]["Controller"]["StateOfCharge_Relative"])
            else:
                soc = float(resp_json["Body"]["Data"]["Inverters"]["1"]["SOC"])
        except TypeError:
            # Wenn WR aus bzw. im Standby (keine Antwort), ersetze leeren Wert durch eine 0.
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
