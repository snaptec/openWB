#!/usr/bin/env python3
import logging
import re

from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_inverter_value_store
from modules.devices.kostal_piko_old.config import KostalPikoOldInverterSetup

log = logging.getLogger(__name__)


class KostalPikoOldInverter:
    def __init__(self, component_config: KostalPikoOldInverterSetup) -> None:
        self.component_config = component_config
        self.store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, response) -> None:
        # power may be a string "xxx" when the inverter is offline, so we cannot match as a number
        # state is just for debugging currently known states:
        # - Aus
        # - Leerlauf
        result = re.search(
            r"aktuell</td>\s*<td[^>]*>\s*([^<]+).*"
            r"Gesamtenergie</td>\s*<td[^>]*>\s*(\d+).*"
            r"Status</td>\s*<td[^>]*>\s*([^<]+)",
            response,
            re.DOTALL
        )
        if result is None:
            raise Exception("Given HTML does not match the expected regular expression. Ignoring.")
        log.debug("Inverter data: state=%s, power=%s, exported=%s" %
                  (result.group(3), result.group(1), result.group(2)))
        try:
            power = -int(result.group(1))
        except ValueError:
            log.info("Inverter power is not a number! Inverter may be offline. Setting power to 0 W.")
            power = 0
        inverter_state = InverterState(
            exported=int(result.group(2)) * 1000,
            power=power
        )
        self.store.set(inverter_state)


component_descriptor = ComponentDescriptor(configuration_factory=KostalPikoOldInverterSetup)
