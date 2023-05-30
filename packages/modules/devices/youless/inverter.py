#!/usr/bin/env python3
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_inverter_value_store
from modules.devices.youless.config import YoulessInverterSetup


class YoulessInverter:
    def __init__(self, component_config: YoulessInverterSetup) -> None:
        self.component_config = component_config
        self.store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, response) -> None:
        if self.component_config.configuration.source_s0:
            power = int(response["ps0"])
            exported = int(response["cs0"].replace(",", ""))
        else:
            power = int(response["pwr"])
            exported = int(response["cnt"].replace(",", ""))

        inverter_state = InverterState(
            power=-abs(power),
            exported=exported,
        )
        self.store.set(inverter_state)


component_descriptor = ComponentDescriptor(configuration_factory=YoulessInverterSetup)
