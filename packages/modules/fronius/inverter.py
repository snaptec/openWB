#!/usr/bin/env python3
import requests
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common import req
from modules.common import simcount
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_inverter_value_store
from modules.fronius.config import FroniusConfiguration, FroniusInverterSetup


class FroniusInverter:
    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, FroniusInverterSetup],
                 device_config: FroniusConfiguration) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(FroniusInverterSetup, component_config)
        self.device_config = device_config
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.simulation = {}
        self.__store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(component_config)

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
        topic_str = "openWB/set/system/device/" + str(self.__device_id) + \
            "/component/" + str(self.component_config.id)+"/"
        _, exported = self.__sim_count.sim_count(power,
                                                 topic=topic_str,
                                                 data=self.simulation,
                                                 prefix="pv%s" % ("" if self.component_config.id == 1 else "2"))

        return InverterState(
            power=power,
            exported=exported
        )

    def update(self) -> None:
        self.__store.set(self.fill_inverter_state(self.read_power()))


component_descriptor = ComponentDescriptor(configuration_factory=FroniusInverterSetup)
