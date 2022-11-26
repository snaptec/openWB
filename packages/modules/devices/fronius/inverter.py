#!/usr/bin/env python3
from typing import Dict, Union

import requests

from dataclass_utils import dataclass_from_dict
from modules.common import req
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.simcount import SimCounter
from modules.common.store import get_inverter_value_store
from modules.devices.fronius.config import FroniusConfiguration, FroniusInverterSetup


class FroniusInverter:
    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, FroniusInverterSetup],
                 device_config: FroniusConfiguration) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(FroniusInverterSetup, component_config)
        self.device_config = device_config
        self.sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="pv")
        self.store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def read_power(self) -> float:
        # Rückgabewert ist die aktuelle Wirkleistung in [W].
        try:
            params = (
                ('Scope', 'System'),
            )
            response = req.get_http_session().get(
                'http://' + self.device_config.ip_address + '/solar_api/v1/GetPowerFlowRealtimeData.fcgi',
                params=params,
                timeout=3)
            try:
                power = float(response.json()["Body"]["Data"]["Site"]["P_PV"]) * -1
            except TypeError:
                # Ohne PV Produktion liefert der WR 'null', ersetze durch Zahl 0
                power = 0
        except (requests.ConnectTimeout, requests.ConnectionError):
            # Nachtmodus: WR ist ausgeschaltet
            power = 0
        return power

    def fill_inverter_state(self, power):
        _, exported = self.sim_counter.sim_count(power)

        return InverterState(
            power=power,
            exported=exported
        )

    def update(self) -> None:
        self.store.set(self.fill_inverter_state(self.read_power()))


component_descriptor = ComponentDescriptor(configuration_factory=FroniusInverterSetup)
