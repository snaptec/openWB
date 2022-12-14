#!/usr/bin/env python3
import logging
from typing import Dict, List, NamedTuple, Optional, Union
import xml.etree.ElementTree as ET

from dataclass_utils import dataclass_from_dict
from modules.common import req
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_counter_value_store
from modules.devices.smartfox.config import SmartfoxCounterSetup

log = logging.getLogger(__name__)

AttributeKeys = NamedTuple("AttributeKeys", [("key_power", str),
                                             ("key_powers", List[str]),
                                             ("key_imported", str),
                                             ("key_exported", str),
                                             ("key_power_factors", Optional[List[str]]),
                                             ("key_voltages", List[str]),
                                             ("key_currents", List[str]),
                                             ])

ATTRIBUTEKEYS_NEW = AttributeKeys(
    key_power="detailsPowerValue",
    key_powers=["powerL1Value", "powerL2Value", "powerL3Value"],
    key_imported="energyValue",
    key_exported="eToGridValue",
    key_power_factors=None,
    key_voltages=["voltageL1Value", "voltageL2Value", "voltageL3Value"],
    key_currents=["ampereL1Value", "ampereL2Value", "ampereL3Value"],
)

ATTRIBUTEKEYS_OLD = AttributeKeys(
    key_power="u5790-41",
    key_powers=["u6017-41", "u6014-41", "u6011-41"],
    key_imported="u5827-41",
    key_exported="u5824-41",
    key_power_factors=["u6074-41", "u6083-41", "u6086-41"],
    key_voltages=["u5978-41", "u5981-41", "u5984-41"],
    key_currents=["u5999-41", "u5996-41", "u5993-41"],
)


class SmartfoxCounter:
    def __init__(self,
                 device_address: str,
                 component_config: Union[Dict, SmartfoxCounterSetup]) -> None:
        self.__device_address = device_address
        self.component_config = dataclass_from_dict(SmartfoxCounterSetup, component_config)
        self.store = get_counter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self) -> None:
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Host': self.__device_address,
            'Connection': 'keep-alive)',
        }

        response = req.get_http_session().get('http://'+self.__device_address+'/values.xml', headers=headers, timeout=5)
        response.encoding = 'utf-8'
        response = response.text.replace("\n", "")
        # Version ermitteln
        self.root = ET.fromstring(response)
        version = self.get_xml_text("version")
        if len(version) < 6:
            versionshort = version[:-6]
        else:
            versionshort = "oldversion"

        if versionshort != "EM2 00.01":
            keys = ATTRIBUTEKEYS_NEW
        else:
            keys = ATTRIBUTEKEYS_OLD

        # Powerfaktor ist nach dem Firmwareupgrade auf EM2 00.01.03.06 (04-2021)
        # nicht mehr in der values.xml daher fix auf 1

        self.store.set(CounterState(
            imported=(self.get_xml_text(keys.key_imported))[:-4] * 1000,
            exported=(self.get_xml_text(keys.key_exported))[:-4] * 1000,
            power=(self.get_xml_text(keys.key_power))[:-2],
            powers=[self.get_xml_text(key) for key in keys.key_powers],
            voltages=[self.get_xml_text(key) for key in keys.key_voltages],
            currents=[self.get_xml_text(key) for key in keys.key_currents],
            power_factors=[self.get_xml_text(key)
                           for key in keys.key_power_factors] if keys.key_power_factors else None
        ))

    def get_xml_text(self, attribute_value: str) -> float:
        value = None
        for element in self.root.iter("value"):
            if element.get("id") == attribute_value:
                value = element.text
        return float(value)


component_descriptor = ComponentDescriptor(configuration_factory=SmartfoxCounterSetup)
