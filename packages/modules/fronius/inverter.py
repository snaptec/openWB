#!/usr/bin/env python3
import requests

from modules.common import req
from modules.common import simcount
from modules.common.component_state import InverterState
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_inverter_value_store
from modules.fronius.abstract_config import FroniusConfiguration


def get_default_config() -> dict:
    return {
        "name": "Fronius Wechselrichter",
        "id": 0,
        "type": "inverter",
        "configuration": {}
    }


class FroniusInverter:
    def __init__(self, device_id: int, component_config: dict, device_config: FroniusConfiguration) -> None:
        self.__device_id = device_id
        self.component_config = component_config
        self.device_config = device_config
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.simulation = {}
        self.__store = get_inverter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def read_power(self) -> float:
        # Rückgabewert ist die aktuelle Wirkleistung in [W].
        try:
            params = (
                ('Scope', 'System'),
            )
            response = req.get_http_session().get(
                'http://' + self.device_config.ip_address + '/solar_api/v1/GetPowerFlowRealtimeData.fcgi',
                params=params,
                timeout=3)
            try:
                power = float(response.json()["Body"]["Data"]["Site"]["P_PV"]) * -1
            except TypeError:
                # Ohne PV Produktion liefert der WR 'null', ersetze durch Zahl 0
                power = 0
        except (requests.ConnectTimeout, requests.ConnectionError):
            # Nachtmodus: WR ist ausgeschaltet
            power = 0
        return power

    def fill_inverter_state(self, power):
        topic = "openWB/set/system/device/" + str(self.__device_id)+"/component/" + str(self.component_config["id"])+"/"
        _, counter = self.__sim_count.sim_count(power, topic=topic, data=self.simulation, prefix="pv")

        return InverterState(
            power=power,
            counter=counter
        )

    def update(self) -> None:
        self.__store.set(self.fill_inverter_state(self.read_power()))
