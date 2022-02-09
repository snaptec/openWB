#!/usr/bin/env python3
from requests import Session
from typing import Tuple

from helpermodules import log
from modules.common import req
from modules.common import simcount
from modules.common.component_state import CounterState
from modules.common.fault_state import ComponentInfo, FaultState
from modules.common.store import get_counter_value_store
from modules.fronius.meter import MeterLocation


def get_default_config() -> dict:
    return {
        "name": "Fronius SM Zähler",
        "id": 0,
        "type": "counter_sm",
        "configuration": {
            "variant": 0,
            "meter_location": MeterLocation.grid.value
        }
    }


class FroniusSmCounter:
    def __init__(self, device_id: int, component_config: dict, device_config: dict) -> None:
        self.__device_id = device_id
        self.component_config = component_config
        self.component_config["configuration"]["meter_location"] = MeterLocation(
            self.component_config["configuration"]["meter_location"])
        self.device_config = device_config
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.simulation = {}
        self.__store = get_counter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self) -> Tuple[CounterState, MeterLocation]:
        variant = self.component_config["configuration"]["variant"]
        log.MainLogger().debug("Komponente "+self.component_config["name"]+" auslesen.")

        session = req.get_http_session()

        if variant == 0 or variant == 1:
            counter_state, meter_location = self.__update_variant_0_1(session)
        elif variant == 2:
            counter_state, meter_location = self.__update_variant_2(session)
        else:
            raise FaultState.error("Unbekannte Variante: "+str(variant))

        topic_str = "openWB/set/system/device/{}/component/{}/".format(
            self.__device_id, self.component_config["id"]
        )
        counter_state.imported, counter_state.exported = self.__sim_count.sim_count(
            counter_state.power,
            topic=topic_str,
            data=self.simulation,
            prefix="bezug"
        )

        return counter_state, meter_location

    def set_counter_state(self, counter_state: CounterState) -> None:
        log.MainLogger().debug("Fronius SM Leistung[W]: " + str(counter_state.power))
        self.__store.set(counter_state)

    def __update_variant_0_1(self, session: Session) -> Tuple[CounterState, MeterLocation]:
        variant = self.component_config["configuration"]["variant"]
        meter_id = self.device_config["meter_id"]
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
            'http://' + self.device_config["ip_address"] + '/solar_api/v1/GetMeterRealtimeData.cgi',
            params=params,
            timeout=5)
        response_json_id = response.json()["Body"]["Data"]

        meter_location = MeterLocation(response_json_id["Meter_Location_Current"])
        log.MainLogger().debug("Einbauort: "+str(meter_location))

        if meter_location == MeterLocation.grid:
            power = response_json_id["PowerReal_P_Sum"]
        else:
            power = self.__get_flow_power(session)
        voltages = [response_json_id["Voltage_AC_Phase_"+str(num)] for num in range(1, 4)]
        powers = [response_json_id["PowerReal_P_Phase_"+str(num)] for num in range(1, 4)]
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
        ), meter_location

    def __update_variant_2(self, session: Session) -> Tuple[CounterState, MeterLocation]:
        meter_id = str(self.device_config["meter_id"])
        response = session.get(
            'http://' + self.device_config["ip_address"] + '/solar_api/v1/GetMeterRealtimeData.cgi',
            params=(('Scope', 'System'),),
            timeout=5)
        response_json_id = dict(response.json()["Body"]["Data"]).get(meter_id)
        meter_location = self.component_config["configuration"]["meter_location"]

        if meter_location == MeterLocation.grid:
            power = response_json_id["SMARTMETER_POWERACTIVE_MEAN_SUM_F64"]
        else:
            power = self.__get_flow_power(session)
        voltages = [response_json_id["SMARTMETER_VOLTAGE_0"+str(num)+"_F64"] for num in range(1, 4)]
        powers = [response_json_id["SMARTMETER_POWERACTIVE_MEAN_0"+str(num)+"_F64"] for num in range(1, 4)]
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
        ), meter_location

    def __get_flow_power(self, session: Session) -> float:
        # Beim Energiebezug ist nicht klar, welcher Anteil aus dem Netz bezogen wurde, und was aus
        # dem Wechselrichter kam.
        # Beim Energieexport ist nicht klar, wie hoch der Eigenverbrauch während der Produktion war.
        response = session.get(
            'http://' + self.device_config["ip_address"] + '/solar_api/v1/GetPowerFlowRealtimeData.fcgi',
            params=(('Scope', 'System'),),
            timeout=5)
        return float(response.json()["Body"]["Data"]["Site"]["P_Grid"])
