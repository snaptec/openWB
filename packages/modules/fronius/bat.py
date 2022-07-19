#!/usr/bin/env python3
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common import req
from modules.common import simcount
from modules.common.component_state import BatState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_bat_value_store
from modules.fronius.config import FroniusConfiguration
from modules.fronius.config import FroniusBatSetup


class FroniusBat:
    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, FroniusBatSetup],
                 device_config: FroniusConfiguration) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(FroniusBatSetup, component_config)
        self.device_config = device_config
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.simulation = {}
        self.__store = get_bat_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self) -> None:
        meter_id = str(self.component_config.configuration.meter_id)

        resp_json = req.get_http_session().get(
            'http://' + self.device_config.ip_address + '/solar_api/v1/GetPowerFlowRealtimeData.fcgi',
            params=(('Scope', 'System'),),
            timeout=5).json()
        try:
            power = int(resp_json["Body"]["Data"]["Site"]["P_Akku"]) * -1
        except TypeError:
            # Wenn WR aus bzw. im Standby (keine Antwort), ersetze leeren Wert durch eine 0.
            power = 0

        try:
            resp_json_id = dict(resp_json["Body"]["Data"])
            if "Inverters" in resp_json_id:
                soc = float(resp_json_id["Inverters"]["1"]["SOC"])
            else:
                soc = float(resp_json_id.get(meter_id)["Controller"]["StateOfCharge_Relative"])
        except TypeError:
            # Wenn WR aus bzw. im Standby (keine Antwort), ersetze leeren Wert durch eine 0.
            soc = 0

        topic_str = "openWB/set/system/device/" + str(
            self.__device_id)+"/component/"+str(self.component_config.id)+"/"
        imported, exported = self.__sim_count.sim_count(
            power, topic=topic_str, data=self.simulation, prefix="speicher"
        )
        bat_state = BatState(
            power=power,
            soc=soc,
            imported=imported,
            exported=exported
        )
        self.__store.set(bat_state)


component_descriptor = ComponentDescriptor(configuration_factory=FroniusBatSetup)
