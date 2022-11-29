#!/usr/bin/env python3
from typing import Union

from modules.common import modbus
from modules.common.fault_state import FaultState
from modules.common.component_type import ComponentDescriptor
from modules.devices.openwb_evu_kit.config import EvuKitInverterSetup
from modules.devices.openwb_flex.config import convert_to_flex_setup
from modules.devices.openwb_flex.inverter import PvKitFlex
from modules.devices.openwb_pv_kit.config import PvKitInverterSetup


class PvKit(PvKitFlex):
    def __init__(self,
                 device_id: int,
                 component_config: Union[EvuKitInverterSetup, PvKitInverterSetup],
                 tcp_client: modbus.ModbusTcpClient_) -> None:
        self.component_config = component_config
        version = self.component_config.configuration.version
        if version == 0 or version == 1:
            id = 8
        elif version == 2:
            id = 116
        else:
            raise FaultState.error("Version "+str(version) + " unbekannt.")

        super().__init__(device_id, convert_to_flex_setup(self.component_config, id), tcp_client)


component_descriptor = ComponentDescriptor(configuration_factory=PvKitInverterSetup)
