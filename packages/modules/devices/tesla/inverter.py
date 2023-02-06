#!/usr/bin/env python3
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_inverter_value_store
from modules.devices.tesla.http_client import PowerwallHttpClient
from modules.devices.tesla.config import TeslaInverterSetup


class TeslaInverter:
    def __init__(self, component_config: Union[Dict, TeslaInverterSetup]) -> None:
        self.component_config = dataclass_from_dict(TeslaInverterSetup, component_config)
        self.store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, client: PowerwallHttpClient, aggregate) -> None:
        pv_watt = aggregate["solar"]["instant_power"]
        if pv_watt > 5:
            pv_watt = pv_watt*-1
        self.store.set(InverterState(
            exported=aggregate["solar"]["energy_exported"],
            power=pv_watt
        ))


component_descriptor = ComponentDescriptor(configuration_factory=TeslaInverterSetup)
