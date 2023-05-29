#!/usr/bin/env python3
import logging
from typing import Dict, Union
import xml.etree.ElementTree as ET

from dataclass_utils import dataclass_from_dict
from modules.common import req
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_counter_value_store
from modules.devices.smartfox.config import SmartfoxCounterSetup

log = logging.getLogger(__name__)


class SmartfoxCounter:
    def __init__(self,
                 device_address: str,
                 component_config: Union[Dict, SmartfoxCounterSetup]) -> None:
        self.__device_address = device_address
        self.component_config = dataclass_from_dict(SmartfoxCounterSetup, component_config)
        self.store = get_counter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self) -> None:
        def get_xml_text(attribute_value: str) -> str:
            value = None
            for element in self.root.iter("value"):
                if element.get("id") == attribute_value:
                    value = element.text
            return value

        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Host': self.__device_address,
            'Connection': 'keep-alive)',
        }

        response = req.get_http_session().get('http://'+self.__device_address+'/values.xml',
                                              headers=headers,
                                              timeout=5)
        response.encoding = 'utf-8'
        response = response.text.replace("\n", "")
        # Version ermitteln
        self.root = ET.fromstring(response)

        # Powerfaktor ist nach dem Firmwareupgrade auf EM2 00.01.03.06 (04-2021)
        # nicht mehr in der values.xml daher fix auf 1

        p1 = float((get_xml_text("powerL1Value"))[:-2])
        p2 = float((get_xml_text("powerL2Value"))[:-2])
        p3 = float((get_xml_text("powerL3Value"))[:-2])
        v1 = float((get_xml_text("voltageL1Value"))[:-2])
        v2 = float((get_xml_text("voltageL2Value"))[:-2])
        v3 = float((get_xml_text("voltageL3Value"))[:-2])
        c1 = float((get_xml_text("ampereL1Value"))[:-2])
        c2 = float((get_xml_text("ampereL2Value"))[:-2])
        c3 = float((get_xml_text("ampereL3Value"))[:-2])
        self.store.set(CounterState(
            imported=float((get_xml_text("energyValue"))[:-4]) * 1000,
            exported=float((get_xml_text("eToGridValue"))[:-4]) * 1000,
            power=float((get_xml_text("detailsPowerValue"))[:-2]),
            powers=[p1, p2, p3],
            voltages=[v1, v2, v3],
            currents=[c1, c2, c3]        
        ))
        

component_descriptor = ComponentDescriptor(configuration_factory=SmartfoxCounterSetup)
