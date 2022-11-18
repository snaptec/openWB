#!/usr/bin/env python3
import logging
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_inverter_value_store
from modules.devices.enphase.config import EnphaseInverterSetup

log = logging.getLogger(__name__)


class EnphaseInverter:
    def __init__(self, device_id: int, component_config: Union[Dict, EnphaseInverterSetup]) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(EnphaseInverterSetup, component_config)
        self.__store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, response) -> None:
        config = self.component_config.configuration

        meter = None
        for m in response:
            if m['eid'] == int(config.eid):
                meter = m
                break

        if meter is None:
            # configuration wrong or error
            log.warning(
                self.device_config.name +
                ": Es konnten keine Daten vom Messgerät gelesen werden."
            )
            return

        power = meter['activePower']

        if power >= 0:
            power = power * -1
        else:
            power = 0

        inverter_state = InverterState(
            power=power,
            exported=meter['actEnergyDlvd']
        )
        self.__store.set(inverter_state)


component_descriptor = ComponentDescriptor(configuration_factory=EnphaseInverterSetup)
