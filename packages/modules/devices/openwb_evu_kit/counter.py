# !/usr/bin/env python3
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common import modbus
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import FaultState
from modules.devices.openwb_evu_kit.config import EvuKitCounterSetup
from modules.devices.openwb_flex.counter import EvuKitFlex
from modules.devices.openwb_flex.config import convert_to_flex_setup


class EvuKit(EvuKitFlex):
    def __init__(self,
                 device_id: int,
                 component_config:  Union[Dict, EvuKitCounterSetup],
                 tcp_client: modbus.ModbusTcpClient_) -> None:
        self.component_config = dataclass_from_dict(EvuKitCounterSetup, component_config)
        version = self.component_config.configuration.version
        if version == 0:
            id = 5
        elif version == 1:
            id = 2
        elif version == 2:
            id = 115
        else:
            raise FaultState.error("Version " + str(version) + " unbekannt.")

        super().__init__(device_id, convert_to_flex_setup(self.component_config, id), tcp_client)


component_descriptor = ComponentDescriptor(configuration_factory=EvuKitCounterSetup)
