#!/usr/bin/env python3
import requests

from helpermodules import log
from modules.common import simcount
from modules.common.component_state import CounterState
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_counter_value_store
from modules.common.fault_state import FaultState


def get_default_config() -> dict:
    return {
        "name": "SonnenBatterie Zähler",
        "id": 0,
        "type": "counter",
        "configuration": {}
    }


class SonnenbatterieCounter:
    def __init__(self, device_id: int, device_address: str, device_variant: int, component_config: dict) -> None:
        self.__device_id = device_id
        self.__device_address = device_address
        self.__device_variant = device_variant
        self.component_config = component_config
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.__simulation = {}
        self.__store = get_counter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def __read_variant_1(self):
        response = requests.get("http://" + self.__device_address + "/api/v1/status", timeout=5)
        response.raise_for_status()
        return response.json()

    def __update_variant_1(self) -> CounterState:
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
        counter_state = self.__read_variant_1()
        grid_power = -counter_state["GridFeedIn_W"]
        log.MainLogger().debug('EVU Leistung: ' + str(grid_power))
        # Es wird nur eine Spannung ausgegeben
        grid_voltage = counter_state["Uac"]
        log.MainLogger().debug('EVU Spannung: ' + str(grid_voltage))
        grid_frequency = counter_state["Fac"]
        log.MainLogger().debug('EVU Netzfrequenz: ' + str(grid_frequency))
        topic_str = "openWB/set/system/device/" + str(
            self.__device_id)+"/component/"+str(self.component_config["id"])+"/"
        imported, exported = self.__sim_count.sim_count(
            grid_power, topic=topic_str, data=self.__simulation, prefix="bezug"
        )
        return CounterState(
            power=grid_power,
            voltages=[grid_voltage]*3,
            frequency=grid_frequency,
            imported=imported,
            exported=exported,
        )

    def __read_variant_2_element(self, element: str) -> str:
        response = requests.get('http://' + self.__device_address + ':7979/rest/devices/battery/' + element, timeout=5)
        response.raise_for_status()
        response.encoding = 'utf-8'
        return response.text.strip(" \n\r")

    def __update_variant_2(self) -> CounterState:
        # Auslesen einer Sonnenbatterie Eco 6 über die integrierte REST-API des Batteriesystems
        grid_import_power = int(float(self.__read_variant_2_element("M39")))
        grid_export_power = int(float(self.__read_variant_2_element("M38")))
        grid_power = grid_import_power - grid_export_power
        topic_str = "openWB/set/system/device/" + str(
            self.__device_id)+"/component/"+str(self.component_config["id"])+"/"
        imported, exported = self.__sim_count.sim_count(
            grid_power, topic=topic_str, data=self.__simulation, prefix="bezug"
        )
        return CounterState(
            power=grid_power,
            imported=imported,
            exported=exported,
        )

    def update(self) -> None:
        log.MainLogger().debug("Komponente '" + str(self.component_config["id"]) + "' "
                               + self.component_config["name"] + " wird auslesen.")
        log.MainLogger().debug("Variante: " + str(self.__device_variant))
        if self.__device_variant == 0:
            log.MainLogger().debug("Die Variante '0' bietet keine EVU Daten!")
        elif self.__device_variant == 1:
            state = self.__update_variant_1()
        elif self.__device_variant == 2:
            state = self.__update_variant_2()
        else:
            raise FaultState.error("Unbekannte Variante: " + str(self.__device_variant))
        self.__store.set(state)
        log.MainLogger().debug("Komponente "+self.component_config["name"]+" wurde erfolgreich auslesen.")
