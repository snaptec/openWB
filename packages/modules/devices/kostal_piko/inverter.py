#!/usr/bin/env python3
from typing import Dict, Tuple, Union

from dataclass_utils import dataclass_from_dict
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_inverter_value_store
from modules.common import req
from modules.devices.kostal_piko.config import KostalPikoInverterSetup


class KostalPikoInverter:
    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, KostalPikoInverterSetup],
                 ip_address: str) -> None:
        self.component_config = dataclass_from_dict(KostalPikoInverterSetup, component_config)
        self.ip_address = ip_address
        self.store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def get_values(self) -> Tuple[float, float]:
        # Die Differenz der Einträge entspricht nicht der Batterieleistung.
        if self.component_config.configuration.bat_configured:
            params = (('dxsEntries', ['33556736', '251658753)']),)
        else:
            params = (('dxsEntries', ['67109120', '251658753)']),)
        resp = req.get_http_session().get('http://'+self.ip_address+'/api/dxs.json', params=params, timeout=3).json()
        power = float(resp["dxsEntries"][0]["value"])
        if power > 5:
            power = power*-1

        exported = float(resp["dxsEntries"][1]["value"]) * 1000
        return power, exported

    def update(self) -> None:
        power, exported = self.get_values()
        self.store.set(InverterState(
            exported=exported,
            power=power
        ))


component_descriptor = ComponentDescriptor(configuration_factory=KostalPikoInverterSetup)
