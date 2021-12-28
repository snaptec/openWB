#!/usr/bin/env python3
import requests
from helpermodules import log
from modules.common.component_state import CounterState
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_counter_value_store


def get_default_config() -> dict:
    return {
        "name": "Fronius S0 Zähler",
        "id": 0,
        "type": "counter_s0",
        "configuration":
        {
            "primo": False
        }
    }


class FroniusS0Counter:
    def __init__(self, device_id: int, component_config: dict, device_config: dict) -> None:
        self.component_config = component_config
        self.device_config = device_config
        self.__store = get_counter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self, bat: bool) -> CounterState:
        primo = self.component_config["configuration"]["primo"]
        log.MainLogger().debug("Komponente "+self.component_config["name"]+" auslesen.")

        response = requests.get(
            'http://'+self.device_config["ip_address"]+'/solar_api/v1/GetPowerFlowRealtimeData.cgi', timeout=5)
        response.raise_for_status()
        try:
            if primo:
                power_all = float(response.json()["Body"]["Data"]["Site"]["P_Grid"])
            else:
                power_all = float(response.json()["Body"]["Data"]["PowerReal_P_Sum"])
        except TypeError:
            # Wenn WR aus bzw. im Standby (keine Antwort), ersetze leeren Wert durch eine 0.
            power_all = 0

        # Summe der vom Netz bezogene Energie total in Wh
        # nur für Smartmeter  im Einspeisepunkt!
        # bei Smartmeter im Verbrauchszweig  entspricht das dem Gesamtverbrauch
        response = requests.get(
            'http://' + self.device_config["ip_address"] + '/solar_api/v1/GetMeterRealtimeData.cgi',
            params=(('Scope', 'System'),),
            timeout=5)
        response.raise_for_status()
        imported = float(response.json()["Body"]["Data"]["0"]["EnergyReal_WAC_Minus_Absolute"])
        exported = float(response.json()["Body"]["Data"]["0"]["EnergyReal_WAC_Plus_Absolute"])

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
