#!/usr/bin/env python3
from modules.common.store import get_counter_value_store
from modules.common.fault_state import ComponentInfo
from modules.common.component_state import CounterState
from modules.common import req
from modules.common import simcount
from helpermodules import log


def get_default_config() -> dict:
    return {
        "name": "Fronius S0 Zähler",
        "id": 0,
        "type": "counter_s0"
    }


class FroniusS0Counter:
    def __init__(self, device_id: int, component_config: dict, device_config: dict) -> None:
        self.__device_id = device_id
        self.component_config = component_config
        self.device_config = device_config
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.simulation = {}
        self.__store = get_counter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self, bat: bool) -> CounterState:
        log.MainLogger().debug("Komponente "+self.component_config["name"]+" auslesen.")

        session = req.get_http_session()
        response = session.get(
            'http://'+self.device_config["ip_address"]+'/solar_api/v1/GetPowerFlowRealtimeData.fcgi',
            timeout=5)
        # Wenn WR aus bzw. im Standby (keine Antwort), ersetze leeren Wert durch eine 0.
        power_all = float(response.json()["Body"]["Data"]["Site"]["P_Grid"]) or 0

        # Summe der vom Netz bezogene Energie total in Wh
        # nur für Smartmeter  im Einspeisepunkt!
        # bei Smartmeter im Verbrauchszweig  entspricht das dem Gesamtverbrauch
        response = session.get(
            'http://' + self.device_config["ip_address"] + '/solar_api/v1/GetMeterRealtimeData.cgi',
            params=(('Scope', 'System'),),
            timeout=5)
        meter_id = str(self.device_config["meter_id"])
        response_json_id = dict(response.json()["Body"]["Data"]).get(meter_id)
        if "EnergyReal_WAC_Minus_Absolute" in response_json_id and \
           "EnergyReal_WAC_Plus_Absolute" in response_json_id:
            imported = float(response_json_id["EnergyReal_WAC_Minus_Absolute"])
            exported = float(response_json_id["EnergyReal_WAC_Plus_Absolute"])
        else:
            topic_str = "openWB/set/system/device/{}/component/{}/".format(
                self.__device_id, self.component_config["id"]
            )
            imported, exported = self.__sim_count.sim_count(
                power_all,
                topic=topic_str,
                data=self.simulation,
                prefix="bezug"
            )

        counter_state = CounterState(
            imported=imported,
            exported=exported,
            power_all=power_all
        )
        log.MainLogger().debug("Fronius SM Leistung[W]: " + str(counter_state.power_all))
        return counter_state

    def set_counter_state(self, counter_state: CounterState) -> None:
        log.MainLogger().debug("Fronius SM Leistung[W]: " + str(counter_state.power_all))
        self.__store.set(counter_state)
