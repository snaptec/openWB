#!/usr/bin/env python3

from modules.common import modbus
from modules.common import simcount
from modules.common.component_state import InverterState
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_inverter_value_store
from modules.openwb_flex.versions import kit_counter_inverter_version_factory
from modules.common.lovato import Lovato


def get_default_config() -> dict:
    return {
        "name": "PV-Kit flex",
        "type": "inverter",
        "id": None,
        "configuration": {
            "version": 2,
            "id": 116
        }
    }


class PvKitFlex:
    def __init__(self, device_id: int, component_config: dict, tcp_client: modbus.ModbusClient) -> None:
        self.__device_id = device_id
        self.component_config = component_config
        factory = kit_counter_inverter_version_factory(
            component_config["configuration"]["version"])
        self.__client = factory(component_config["configuration"]["id"], tcp_client)
        self.__tcp_client = tcp_client
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.simulation = {}
        self.__store = get_inverter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self) -> None:
        """ liest die Werte des Moduls aus.
        """
        with self.__tcp_client:
            powers, power = self.__client.get_power()

            version = self.component_config["configuration"]["version"]
            if version == 1:
                power = sum(powers)
            if power > 10:
                power = power*-1
            currents = self.__client.get_currents()

        if isinstance(self.__client, Lovato):
            topic_str = "openWB/set/system/device/" + \
                str(self.__device_id)+"/component/" + \
                str(self.component_config["id"])+"/"
            _, exported = self.__sim_count.sim_count(power,
                                                     topic=topic_str,
                                                     data=self.simulation,
                                                     prefix="pv%s" % ("" if self.component_config["id"] == 1 else "2"))
        else:
            exported = self.__client.get_exported()

        inverter_state = InverterState(
            power=power,
            exported=exported,
            currents=currents
        )
        self.__store.set(inverter_state)
