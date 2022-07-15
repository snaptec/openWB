#!/usr/bin/env python3
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common import modbus
from modules.common import simcount
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.lovato import Lovato
from modules.common.store import get_inverter_value_store
from modules.openwb_flex.config import PvKitFlexSetup
from modules.openwb_flex.versions import kit_counter_inverter_version_factory


class PvKitFlex:
    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, PvKitFlexSetup],
                 tcp_client: modbus.ModbusTcpClient_) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(PvKitFlexSetup, component_config)
        factory = kit_counter_inverter_version_factory(
            self.component_config.configuration.version)
        self.__client = factory(self.component_config.configuration.id, tcp_client)
        self.__tcp_client = tcp_client
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.simulation = {}
        self.__store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self) -> None:
        """ liest die Werte des Moduls aus.
        """
        with self.__tcp_client:
            powers, power = self.__client.get_power()

            version = self.component_config.configuration.version
            if version == 1:
                power = sum(powers)
            if power > 10:
                power = power*-1
            currents = self.__client.get_currents()

            if isinstance(self.__client, Lovato):
                topic_str = "openWB/set/system/device/" + \
                    str(self.__device_id)+"/component/" + \
                    str(self.component_config.id)+"/"
                prefix = "pv%s" % ("" if self.component_config.id == 1 else "2")
                _, exported = self.__sim_count.sim_count(power, topic=topic_str, data=self.simulation, prefix=prefix)
            else:
                exported = self.__client.get_exported()

        inverter_state = InverterState(
            power=power,
            exported=exported,
            currents=currents
        )
        self.__store.set(inverter_state)


component_descriptor = ComponentDescriptor(configuration_factory=PvKitFlexSetup)
