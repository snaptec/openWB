#!/usr/bin/env python3
import logging
from typing import Dict, Union


from dataclass_utils import dataclass_from_dict
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_counter_value_store
from modules.devices.solar_log.config import SolarLogCounterSetup

log = logging.getLogger(__name__)


class SolarLogCounter:
    def __init__(self,
                 component_config: Union[Dict, SolarLogCounterSetup]) -> None:
        self.component_config = dataclass_from_dict(SolarLogCounterSetup, component_config)
        self.store = get_counter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, response: Dict) -> None:
        pvwatt = int(float(response["801"]["170"]["101"]))
        hausverbrauch = int(float(response["801"]["170"]["110"]))
        bezugwatt = hausverbrauch - pvwatt
        pvkwh = float(response["801"]["170"]["109"])

        if bezug_solarlog_speicherv == 1:
            with open("ramdisk/speicherleistung", "r") as f:
                speicherleistung = int(float(f.read()))
            bezugwatt = bezugwatt + speicherleistung

        self.store.set(CounterState(
            imported=float(response['A_Plus']),
            exported=float(response['A_Minus']),
            power=float(response['Watt'])
        ))


component_descriptor = ComponentDescriptor(configuration_factory=SolarLogCounterSetup)
