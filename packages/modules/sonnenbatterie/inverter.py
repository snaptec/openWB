#!/usr/bin/env python3
from typing import Dict, Union
import logging

from dataclass_utils import dataclass_from_dict
from modules.common import simcount
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_inverter_value_store
from modules.common.fault_state import FaultState
from modules.common import req
from modules.sonnenbatterie.config import SonnenbatterieInverterSetup

log = logging.getLogger(__name__)


class SonnenbatterieInverter:
    def __init__(self,
                 device_id: int,
                 device_address: str,
                 device_variant: int,
                 component_config: Union[Dict, SonnenbatterieInverterSetup]) -> None:
        self.__device_id = device_id
        self.__device_address = device_address
        self.__device_variant = device_variant
        self.component_config = dataclass_from_dict(SonnenbatterieInverterSetup, component_config)
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.simulation = {}
        self.__store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(component_config)

    def __read_variant_1(self):
        return req.get_http_session().get("http://" + self.__device_address + "/api/v1/status", timeout=5).json()

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
        log.debug('Speicher PV Leistung: ' + str(pv_power))
        topic_str = "openWB/set/system/device/" + str(
            self.__device_id)+"/component/"+str(self.component_config.id)+"/"
        _, exported = self.__sim_count.sim_count(pv_power,
                                                 topic=topic_str,
                                                 data=self.simulation,
                                                 prefix="pv%s" % ("" if self.component_config.id == 1 else "2"))
        return InverterState(
            exported=exported,
            power=pv_power
        )

    def __read_variant_2_element(self, element: str) -> str:
        response = req.get_http_session().get('http://' + self.__device_address +
                                              ':7979/rest/devices/battery/' + element, timeout=5)
        response.encoding = 'utf-8'
        return response.text.strip(" \n\r")

    def __update_variant_2(self) -> InverterState:
        # Auslesen einer Sonnenbatterie Eco 6 über die integrierte REST-API des Batteriesystems
        pv_power = -int(float(self.__read_variant_2_element("M03")))
        log.debug('Speicher PV Leistung: ' + str(pv_power))
        topic_str = "openWB/set/system/device/" + str(
            self.__device_id)+"/component/"+str(self.component_config.id)+"/"
        _, exported = self.__sim_count.sim_count(pv_power,
                                                 topic=topic_str,
                                                 data=self.simulation,
                                                 prefix="pv%s" % ("" if self.component_config.id == 1 else "2"))
        return InverterState(
            exported=exported,
            power=pv_power
        )

    def update(self) -> None:
        log.debug("Variante: " + str(self.__device_variant))
        if self.__device_variant == 0:
            log.debug("Die Variante '0' bietet keine PV Daten!")
        elif self.__device_variant == 1:
            state = self.__update_variant_1()
        elif self.__device_variant == 2:
            state = self.__update_variant_2()
        else:
            raise FaultState.error("Unbekannte Variante: " + str(self.__device_variant))
        self.__store.set(state)


component_descriptor = ComponentDescriptor(configuration_factory=SonnenbatterieInverterSetup)
