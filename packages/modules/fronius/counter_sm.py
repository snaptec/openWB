#!/usr/bin/env python3
from typing import Tuple
import requests

from helpermodules import log
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
        "configuration":
        {
            "variant": 0,
            "meter_location": MeterLocation.grid
        }
    }


class FroniusSmCounter:
    def __init__(self, device_id: int, component_config: dict, device_config: dict) -> None:
        self.__device_id = device_id
        self.component_config = component_config
        self.device_config = device_config
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.simulation = {}
        self.__store = get_counter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self, bat: bool) -> Tuple[CounterState, bool]:
        variant = self.component_config["configuration"]["variant"]
        log.MainLogger().debug("Komponente "+self.component_config["name"]+" auslesen.")

        if variant == 0 or variant == 1:
            counter_state, meter_location = self.__update_variant_0_1()
        elif variant == 2:
            counter_state, meter_location = self.__update_variant_2()
        else:
            raise FaultState.error("Unbekannte Variante: "+str(variant))

        if meter_location == MeterLocation.load:
            response = requests.get(
                'http://' + self.device_config["ip_address"] + '/solar_api/v1/GetPowerFlowRealtimeData.fcgi',
                params=(('Scope', 'System'),),
                timeout=5)
            response.raise_for_status()
            counter_state.power_all = float(response.json()["Body"]["Data"]["Site"]["P_Grid"])
            topic_str = "openWB/set/system/device/{}/component/{}/".format(
                self.__device_id, self.component_config["id"]
            )
            # Beim Energiebezug ist nicht klar, welcher Anteil aus dem Netz bezogen wurde, und was aus
            # dem Wechselrichter kam.
            # Beim Energieexport ist nicht klar, wie hoch der Eigenverbrauch während der Produktion war.
            counter_state.imported, counter_state.exported = self.__sim_count.sim_count(
                counter_state.power_all,
                topic=topic_str,
                data=self.simulation,
                prefix="bezug"
            )

        return counter_state, meter_location

    def set_counter_state(self, counter_state: CounterState) -> None:
        log.MainLogger().debug("Fronius SM Leistung[W]: " + str(counter_state.power_all))
        self.__store.set(counter_state)

    def __update_variant_0_1(self) -> Tuple[CounterState, bool]:
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
        response = requests.get(
            'http://' + self.device_config["ip_address"] + '/solar_api/v1/GetMeterRealtimeData.cgi',
            params=params,
            timeout=5)
        response.raise_for_status()
        response_json_id = response.json()["Body"]["Data"]
        # old request for variant == 1
        # params = (
        #     ('Scope', 'System'),
        # )
        # response = requests.get(
        #     'http://'+self.device_config["ip_address"]+'/solar_api/v1/GetMeterRealtimeData.cgi',
        #  params=params, timeout=5)
        # response.raise_for_status()
        # response_json_id = response.json()["Body"]["Data"][meter_id]
        meter_location = MeterLocation(response_json_id["Meter_Location_Current"])
        log.MainLogger().debug("Einbauort: "+str(meter_location))

        power_all = response_json_id["PowerReal_P_Sum"]
        voltages = [response_json_id["Voltage_AC_Phase_"+str(num)] for num in range(1, 4)]
        powers = [response_json_id["PowerReal_P_Phase_"+str(num)] for num in range(1, 4)]
        currents = [powers[i] / voltages[i] for i in range(0, 3)]
        power_factors = [response_json_id["PowerFactor_Phase_"+str(num)] for num in range(1, 4)]
        frequency = response_json_id["Frequency_Phase_Average"]
        imported = response_json_id["EnergyReal_WAC_Sum_Consumed"]
        exported = response_json_id["EnergyReal_WAC_Sum_Produced"]

        return CounterState(
            voltages=voltages,
            currents=currents,
            powers=powers,
            imported=imported,
            exported=exported,
            power_all=power_all,
            frequency=frequency,
            power_factors=power_factors
        ), meter_location

    def __update_variant_2(self) -> Tuple[CounterState, bool]:
        meter_id = str(self.device_config["meter_id"])
        response = requests.get(
            'http://' + self.device_config["ip_address"] + '/solar_api/v1/GetMeterRealtimeData.cgi',
            params=(('Scope', 'System'),),
            timeout=5)
        response.raise_for_status()
        response_json_id = dict(response.json()["Body"]["Data"]).get(meter_id)
        meter_location = self.component_config["configuration"]["meter_location"]

        power_all = response_json_id["SMARTMETER_POWERACTIVE_MEAN_SUM_F64"]
        voltages = [response_json_id["SMARTMETER_VOLTAGE_0"+str(num)+"_F64"] for num in range(1, 4)]
        powers = [response_json_id["SMARTMETER_POWERACTIVE_MEAN_0"+str(num)+"_F64"] for num in range(1, 4)]
        currents = [powers[i] / voltages[i] for i in range(0, 3)]
        power_factors = [response_json_id["SMARTMETER_FACTOR_POWER_0"+str(num)+"_F64"] for num in range(1, 4)]
        frequency = response_json_id["GRID_FREQUENCY_MEAN_F32"]
        imported = response_json_id["SMARTMETER_ENERGYACTIVE_CONSUMED_SUM_F64"]
        exported = response_json_id["SMARTMETER_ENERGYACTIVE_PRODUCED_SUM_F64"]

        return CounterState(
            voltages=voltages,
            currents=currents,
            powers=powers,
            imported=imported,
            exported=exported,
            power_all=power_all,
            frequency=frequency,
            power_factors=power_factors
        ), meter_location
