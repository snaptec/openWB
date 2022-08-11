#!/usr/bin/env python3
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common import modbus
from modules.common import simcount
from modules.common.component_state import BatState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.lovato import Lovato
from modules.common.sdm import Sdm630
from modules.common.store import get_bat_value_store
from modules.openwb_flex.config import BatKitFlexSetup
from modules.openwb_flex.versions import kit_bat_version_factory


class BatKitFlex:
    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, BatKitFlexSetup],
                 tcp_client: modbus.ModbusTcpClient_) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(BatKitFlexSetup, component_config)
        factory = kit_bat_version_factory(
            self.component_config.configuration.version)
        self.__client = factory(self.component_config.configuration.id,
                                tcp_client)
        self.__tcp_client = tcp_client
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.simulation = {}
        self.__store = get_bat_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self):
        # TCP-Verbindung schließen möglichst bevor etwas anderes gemacht wird, um im Fehlerfall zu verhindern,
        # dass offene Verbindungen den Modbus-Adapter blockieren.
        with self.__tcp_client:
            if isinstance(self.__client, Sdm630):
                _, power = self.__client.get_power()
                power = power * -1
            else:
                _, power = self.__client.get_power()
            if isinstance(self.__client, Lovato):
                topic_str = "openWB/set/system/device/" + str(
                    self.__device_id)+"/component/"+str(self.component_config.id)+"/"
                imported, exported = self.__sim_count.sim_count(
                    power, topic=topic_str, data=self.simulation, prefix="speicher"
                )
            else:
                imported = self.__client.get_imported()
                exported = self.__client.get_exported()

        bat_state = BatState(
            imported=imported,
            exported=exported,
            power=power
        )
        self.__store.set(bat_state)


component_descriptor = ComponentDescriptor(configuration_factory=BatKitFlexSetup)
