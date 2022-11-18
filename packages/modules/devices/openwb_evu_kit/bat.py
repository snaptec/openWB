#!/usr/bin/env python3
from modules.common.component_type import ComponentDescriptor
from modules.devices.openwb_evu_kit.config import EvuKitBatSetup


component_descriptor = ComponentDescriptor(configuration_factory=EvuKitBatSetup)
