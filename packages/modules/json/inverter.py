#!/usr/bin/env python3
import jq
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common import simcount
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_inverter_value_store
from modules.json.config import JsonInverterSetup


class JsonInverter:
    def __init__(self, device_id: int, component_config: Union[Dict, JsonInverterSetup]) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(JsonInverterSetup, component_config)
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.simulation = {}
        self.__store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, response) -> None:
        config = self.component_config.configuration

        power = float(jq.compile(config.jq_power).input(response).first())
        if power >= 0:
            power = power * -1
        if config.jq_exported == "":
            topic_str = "openWB/set/system/device/" + \
                str(self.__device_id)+"/component/" + \
                str(self.component_config.id)+"/"
            _, exported = self.__sim_count.sim_count(power,
                                                     topic=topic_str,
                                                     data=self.simulation,
                                                     prefix="pv%s" % ("" if self.component_config.id == 1 else "2"))
        else:
            exported = jq.compile(config.jq_exported).input(response).first()

        inverter_state = InverterState(
            power=power,
            exported=exported
        )
        self.__store.set(inverter_state)


component_descriptor = ComponentDescriptor(configuration_factory=JsonInverterSetup)
