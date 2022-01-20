#!/usr/bin/env python3
import requests

from helpermodules import log
from modules.common import simcount
from modules.common.component_state import InverterState
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_inverter_value_store
from modules.common.fault_state import FaultState


def get_default_config() -> dict:
    return {
        "name": "SonnenBatterie Wechselrichter",
        "id": 0,
        "type": "inverter",
        "configuration": {}
    }


class SonnenbatterieInverter:
    def __init__(self, device_id: int, device_address: str, device_variant: int, component_config: dict) -> None:
        self.__device_id = device_id
        self.__device_address = device_address
        self.__device_variant = device_variant
        self.component_config = component_config
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.__simulation = {}
        self.__store = get_inverter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def __read_variant_1(self):
        response = requests.get("http://" + self.__device_address + "/api/v1/status", timeout=5)
        response.raise_for_status()
        return response.json()

    def __update_variant_1(self) -> InverterState:
        # Auslesen einer Sonnenbatterie 8 oder 10 über die integrierte JSON-API v1 des Batteriesystems
        '''
        example data:
        {
            "Apparent_output": 225,
            "BackupBuffer": "0",
            "BatteryCharging": false,
            "BatteryDischarging": false,
            "Consumption_Avg": 2114,
            "Consumption_W": 2101,
            "Fac": 49.97200393676758,
            "FlowConsumptionBattery": false,
            "FlowConsumptionGrid": true,
            "FlowConsumptionProduction": false,
            "FlowGridBattery": false,
            "FlowProductionBattery": false,
            "FlowProductionGrid": false,
            "GridFeedIn_W": -2106,
            "IsSystemInstalled": 1,
            "OperatingMode": "2",
            "Pac_total_W": -5,
            "Production_W": 0,
            "RSOC": 6,
            "RemainingCapacity_Wh": 2377,
            "Sac1": 75,
            "Sac2": 75,
            "Sac3": 75,
            "SystemStatus": "OnGrid",
            "Timestamp": "2021-12-13 07:54:48",
            "USOC": 0,
            "Uac": 231,
            "Ubat": 48,
            "dischargeNotAllowed": true,
            "generator_autostart": false,
            "NVM_REINIT_STATUS": 0
        }
        '''
        inverter_state = self.__read_variant_1()
        pv_power = -inverter_state["Production_W"]
        log.MainLogger().debug('Speicher PV Leistung: ' + str(pv_power))
        topic_str = "openWB/set/system/device/" + str(
            self.__device_id)+"/component/"+str(self.component_config["id"])+"/"
        _, exported = self.__sim_count.sim_count(
            pv_power, topic=topic_str, data=self.__simulation, prefix="pv"
        )
        return InverterState(
            counter=exported,
            power=pv_power
        )

    def __read_variant_2_element(self, element: str) -> str:
        response = requests.get('http://' + self.__device_address + ':7979/rest/devices/battery/' + element, timeout=5)
        response.raise_for_status()
        response.encoding = 'utf-8'
        return response.text.replace("\n", "")

    def __update_variant_2(self) -> InverterState:
        # Auslesen einer Sonnenbatterie Eco 6 über die integrierte REST-API des Batteriesystems
        pv_power = -int(self.__read_variant_2_element("M03"))
        log.MainLogger().debug('Speicher PV Leistung: ' + str(pv_power))
        topic_str = "openWB/set/system/device/" + str(
            self.__device_id)+"/component/"+str(self.component_config["id"])+"/"
        _, exported = self.__sim_count.sim_count(
            pv_power, topic=topic_str, data=self.__simulation, prefix="pv"
        )
        return InverterState(
            counter=exported,
            power=pv_power
        )

    def update(self) -> None:
        log.MainLogger().debug("Komponente '" + str(self.component_config["id"]) + "' "
                               + self.component_config["name"] + " wird auslesen.")
        log.MainLogger().debug("Variante: " + str(self.__device_variant))
        if self.__device_variant == 0:
            log.MainLogger().debug("Die Variante '0' bietet keine PV Daten!")
        elif self.__device_variant == 1:
            state = self.__update_variant_1()
        elif self.__device_variant == 2:
            state = self.__update_variant_2()
        else:
            raise FaultState.error("Unbekannte Variante: " + str(self.__device_variant))
        self.__store.set(state)
        log.MainLogger().debug("Komponente "+self.component_config["name"]+" wurde erfolgreich auslesen.")
