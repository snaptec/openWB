#!/usr/bin/env python3
import logging
from typing import Dict, Tuple, Union

from requests import Session

from dataclass_utils import dataclass_from_dict
from modules.common import req
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo, FaultState
from modules.common.simcount import SimCounter
from modules.common.store import get_counter_value_store
from modules.devices.fronius.config import FroniusConfiguration, MeterLocation
from modules.devices.fronius.config import FroniusSmCounterSetup

log = logging.getLogger(__name__)


class FroniusSmCounter:
    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, FroniusSmCounterSetup],
                 device_config: FroniusConfiguration) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(FroniusSmCounterSetup, component_config)
        self.device_config = device_config
        self.sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="bezug")
        self.store = get_counter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self) -> None:
        session = req.get_http_session()
        variant = self.component_config.configuration.variant
        if variant == 0 or variant == 1:
            counter_state = self.__update_variant_0_1(session)
        elif variant == 2:
            counter_state = self.__update_variant_2(session)
        else:
            raise FaultState.error("Unbekannte Variante: "+str(variant))
        counter_state.imported, counter_state.exported = self.sim_counter.sim_count(counter_state.power)
        self.store.set(counter_state)

    def __update_variant_0_1(self, session: Session) -> CounterState:
        variant = self.component_config.configuration.variant
        meter_id = self.component_config.configuration.meter_id
        if variant == 0:
            params = (
                ('Scope', 'Device'),
                ('DeviceId', meter_id),
            )
        elif variant == 1:
            params = (
                ('Scope', 'Device'),
                ('DeviceId', meter_id),
                ('DataCollection', 'MeterRealtimeData'),
            )
        else:
            raise FaultState.error("Unbekannte Generation: "+str(variant))
        response = session.get(
            'http://' + self.device_config.ip_address + '/solar_api/v1/GetMeterRealtimeData.cgi',
            params=params,
            timeout=5)
        response_json_id = response.json()["Body"]["Data"]

        meter_location = MeterLocation.get(response_json_id["Meter_Location_Current"])
        log.debug("Einbauort: "+str(meter_location))

        powers = [response_json_id["PowerReal_P_Phase_"+str(num)] for num in range(1, 4)]
        if meter_location == MeterLocation.load:
            power, power_inverter = self.__get_flow_power(session)
            # wenn SmartMeter im Verbrauchszweig sitzt sind folgende Annahmen getroffen:
            # PV Leistung wird gleichmäßig auf alle Phasen verteilt
            # Spannungen und Leistungsfaktoren sind am Verbrauchszweig == Einspeisepunkt
            # Hier gehen wir mal davon aus, dass der Wechselrichter seine PV-Leistung gleichmäßig
            # auf alle Phasen aufteilt.
            powers = [-1 * power - power_inverter/3 for power in powers]
        else:
            power = response_json_id["PowerReal_P_Sum"]
        voltages = [response_json_id["Voltage_AC_Phase_"+str(num)] for num in range(1, 4)]
        currents = [powers[i] / voltages[i] for i in range(0, 3)]
        power_factors = [response_json_id["PowerFactor_Phase_"+str(num)] for num in range(1, 4)]
        frequency = response_json_id["Frequency_Phase_Average"]

        return CounterState(
            voltages=voltages,
            currents=currents,
            powers=powers,
            power=power,
            frequency=frequency,
            power_factors=power_factors
        )

    def __update_variant_2(self, session: Session) -> CounterState:
        meter_id = str(self.component_config.configuration.meter_id)
        response = session.get(
            'http://' + self.device_config.ip_address + '/solar_api/v1/GetMeterRealtimeData.cgi',
            params=(('Scope', 'System'),),
            timeout=5)
        response_json_id = dict(response.json()["Body"]["Data"]).get(meter_id)

        meter_location = MeterLocation.get(response_json_id["SMARTMETER_VALUE_LOCATION_U16"])
        log.debug("Einbauort: "+str(meter_location))

        powers = [response_json_id["SMARTMETER_POWERACTIVE_MEAN_0"+str(num)+"_F64"] for num in range(1, 4)]
        if meter_location == MeterLocation.load:
            power, power_inverter = self.__get_flow_power(session)
            # wenn SmartMeter im Verbrauchszweig sitzt sind folgende Annahmen getroffen:
            # PV Leistung wird gleichmäßig auf alle Phasen verteilt
            # Spannungen und Leistungsfaktoren sind am Verbrauchszweig == Einspeisepunkt
            # Hier gehen wir mal davon aus, dass der Wechselrichter seine PV-Leistung gleichmäßig
            # auf alle Phasen aufteilt.
            powers = [-1 * power - power_inverter/3 for power in powers]
        else:
            power = response_json_id["SMARTMETER_POWERACTIVE_MEAN_SUM_F64"]
        voltages = [response_json_id["SMARTMETER_VOLTAGE_0"+str(num)+"_F64"] for num in range(1, 4)]
        currents = [powers[i] / voltages[i] for i in range(0, 3)]
        power_factors = [response_json_id["SMARTMETER_FACTOR_POWER_0"+str(num)+"_F64"] for num in range(1, 4)]
        frequency = response_json_id["GRID_FREQUENCY_MEAN_F32"]

        return CounterState(
            voltages=voltages,
            currents=currents,
            powers=powers,
            power=power,
            frequency=frequency,
            power_factors=power_factors
        )

    def __get_flow_power(self, session: Session) -> Tuple[float, float]:
        # Beim Energiebezug ist nicht klar, welcher Anteil aus dem Netz bezogen wurde, und was aus
        # dem Wechselrichter kam.
        # Beim Energieexport ist nicht klar, wie hoch der Eigenverbrauch während der Produktion war.
        response = session.get(
            'http://' + self.device_config.ip_address + '/solar_api/v1/GetPowerFlowRealtimeData.fcgi',
            params=(('Scope', 'System'),),
            timeout=5)
        power_load = float(response.json()["Body"]["Data"]["Site"]["P_Grid"])
        power_inverter = float(response.json()["Body"]["Data"]["Site"]["P_PV"] or 0)
        return power_load, power_inverter


component_descriptor = ComponentDescriptor(configuration_factory=FroniusSmCounterSetup)
