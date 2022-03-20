#!/usr/bin/env python3

import requests

from helpermodules import log
from modules.common import req
from modules.common import simcount
from modules.common.component_state import InverterState
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_inverter_value_store


def get_default_config() -> dict:
    return {
        "name": "Fronius Wechselrichter",
        "id": 0,
        "type": "inverter",
        "configuration": {
            "ip_address2": "none"  # ToDo: add second component instead
        }
    }


class FroniusInverter:
    def __init__(self, device_id: int, component_config: dict, device_config: dict) -> None:
        self.__device_id = device_id
        self.component_config = component_config
        self.device_config = device_config
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.__simulation = {}
        self.__store = get_inverter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self) -> InverterState:
        log.MainLogger().debug("Komponente "+self.component_config["name"]+" auslesen.")

        # Rückgabewert ist die aktuelle Wirkleistung in [W].
        params = (
            ('Scope', 'System'),
        )
        response = req.get_http_session().get(
            'http://' + self.device_config["ip_address"] + '/solar_api/v1/GetPowerFlowRealtimeData.fcgi', params=params,
            timeout=3)
        try:
            power = float(response.json()["Body"]["Data"]["Site"]["P_PV"])
        except TypeError:
            # Ohne PV Produktion liefert der WR 'null', ersetze durch Zahl 0
            power = 0

        power2 = self.__get_wr2()
        power += power2
        power *= -1
        topic = "openWB/set/system/device/" + str(self.__device_id)+"/component/" + str(self.component_config["id"])+"/"
        _, counter = self.__sim_count.sim_count(power, topic=topic, data=self.__simulation, prefix="pv")

        inverter_state = InverterState(
            power=power,
            counter=counter
        )
        return inverter_state

    def __get_wr2(self) -> float:
        ip_address2 = self.component_config["configuration"]["ip_address2"]
        if ip_address2 != "none":
            try:
                params = (('Scope', 'System'),)
                response = req.get_http_session().get(
                    'http://' + ip_address2 + '/solar_api/v1/GetPowerFlowRealtimeData.fcgi', params=params, timeout=3)
                response.raise_for_status()
                try:
                    power2 = float(response.json()["Body"]["Data"]["Site"]["P_PV"])
                except TypeError:
                    # Ohne PV Produktion liefert der WR 'null', ersetze durch Zahl 0
                    power2 = 0
            except (requests.ConnectTimeout, requests.ConnectionError):
                # Nachtmodus: WR ist ausgeschaltet
                power2 = 0
        else:
            power2 = 0
        return power2

    def set_inverter_state(self, inverter_state: InverterState) -> None:
        log.MainLogger().debug("Fronius Inverter Leistung[W]: " + str(inverter_state.power))
        self.__store.set(inverter_state)
