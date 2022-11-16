#!/usr/bin/env python3
from typing import Dict, Union
from requests.auth import HTTPDigestAuth

from dataclass_utils import dataclass_from_dict
from modules.common import req
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_inverter_value_store
from modules.devices.sunways.config import SunwaysInverterSetup

"""Example Output for ajax.txt
109 W;103 W;111 VA;41 var;333.8;223.2;0.3;0.5;109.0;103.0;---;---;0.93 c;1.60;105.2;190.2;55342.2;132;0;0;NT 5000;1;
x
00200403;01;00000001
"""


class SunwaysInverter:
    def __init__(self,
                 component_config: Union[Dict, SunwaysInverterSetup],
                 ip_address: str,
                 password: str) -> None:

        self.component_config = dataclass_from_dict(SunwaysInverterSetup, component_config)
        self.ip_address = ip_address
        self.password = password
        self.store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self) -> None:
        params = (
            ('CAN', '1'),
            ('HASH', '00200403'),
            ('TYPE', '1'),
        )
        response = req.get_http_session().get("http://" + self.ip_address + "/data/ajax.txt", params=params,
                                              auth=HTTPDigestAuth("customer", self.password))
        values = response.text.split(';')

        inverter_state = InverterState(
            power=float(values[1].split(' ')[0])*-1,
            exported=float(values[16])*1000
        )
        self.store.set(inverter_state)


component_descriptor = ComponentDescriptor(configuration_factory=SunwaysInverterSetup)
