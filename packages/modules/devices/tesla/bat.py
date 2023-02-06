#!/usr/bin/env python3
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common.component_state import BatState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_bat_value_store
from modules.devices.tesla.http_client import PowerwallHttpClient
from modules.devices.tesla.config import TeslaBatSetup


class TeslaBat:
    def __init__(self, component_config: Union[Dict, TeslaBatSetup]) -> None:
        self.component_config = dataclass_from_dict(TeslaBatSetup, component_config)
        self.store = get_bat_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, client: PowerwallHttpClient, aggregate) -> None:
        self.store.set(BatState(
            imported=aggregate["battery"]["energy_imported"],
            exported=aggregate["battery"]["energy_exported"],
            power=-aggregate["battery"]["instant_power"],
            soc=client.get_json("/api/system_status/soe")["percentage"]
        ))


component_descriptor = ComponentDescriptor(configuration_factory=TeslaBatSetup)
