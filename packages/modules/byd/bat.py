#!/usr/bin/env python3
from html.parser import HTMLParser
import logging
from typing import List, Tuple

from modules.common import req
from modules.common import simcount
from modules.common.component_state import BatState
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_bat_value_store

log = logging.getLogger(__name__)


def get_default_config() -> dict:
    return {
        "name": "BYD Speicher",
        "id": 0,
        "type": "bat",
        "configuration": {}
    }


class BYDBat:
    def __init__(self,
                 component_config: dict,
                 device_config) -> None:
        self.__device_config = device_config
        self.component_config = component_config
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.simulation = {}
        self.__store = get_bat_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self) -> None:
        power, soc = self.get_values()

        topic_str = "openWB/set/system/device/" + str(
            self.__device_config.id)+"/component/"+str(self.component_config["id"])+"/"
        imported, exported = self.__sim_count.sim_count(
            power, topic=topic_str, data=self.simulation, prefix="speicher"
        )
        bat_state = BatState(
            power=power,
            soc=soc,
            imported=imported,
            exported=exported
        )
        self.__store.set(bat_state)

    def get_values(self) -> Tuple[float, float]:
        '''BYD Speicher bieten zwei HTML-Seiten, auf denen Informationen abgegriffen werden können:
        /asp/Home.asp und /asp/RunData.asp. Aktuell (2022-03) ist die Leistungsangabe (Power) auf der
        RunData.asp auf ganze kW gerundet und somit für openWB nicht brauchbar.
        '''
        resp = req.get_http_session().get(
            'http://' + self.__device_config.configuration.ip_address + '/asp/Home.asp',
            auth=(self.__device_config.configuration.username,  self.__device_config.configuration.password))
        return BydParser.parse(resp.text)


class BydParser(HTMLParser):
    values = {"SOC:": 0, "Power:": 0}
    armed = None

    @staticmethod
    def parse(html: str):
        parser = BydParser()
        parser.feed(html)
        return parser.get_bat_state()

    def handle_starttag(self, tag, attrs: List[Tuple[str, str]]):
        if tag == "input" and self.armed is not None:
            for key, value in attrs:
                if key == "value":
                    self.values[self.armed] = value
                    break
            self.armed = None

    def handle_data(self, data: str):
        if data in self.values:
            self.armed = data

    def get_bat_state(self) -> Tuple[float, float]:
        return float(self.values["Power:"]) * 1000, float(self.values["SOC:"][:-1])
