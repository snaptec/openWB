#!/usr/bin/env python3
from modules.common.component_type import ComponentDescriptor
from modules.openwb_evu_kit.config import EvuKitInverterSetup


component_descriptor = ComponentDescriptor(configuration_factory=EvuKitInverterSetup)
