#!/usr/bin/env python3
import xml.etree.ElementTree as ET

from dataclass_utils import dataclass_from_dict
from modules.common import req
from modules.common.component_state import BatState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.simcount import SimCounter
from modules.common.store import get_bat_value_store
from modules.devices.varta.config import VartaBatApiSetup


class VartaBatApi:
    def __init__(self, device_id: int, component_config: VartaBatApiSetup, device_address: str) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(VartaBatApiSetup, component_config)
        self.__device_address = device_address
        self.sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="speicher")
        self.store = get_bat_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self) -> None:
        def get_xml_text(attribute_value: str) -> float:
            value = None
            for element in root[0].iter("var"):
                if element.attrib["name"] == attribute_value:
                    value = element.attrib["value"]
            try:
                return float(value)
            except ValueError:
                # Wenn Speicher aus bzw. im Standby (keine Antwort), ersetze leeren Wert durch eine 0.
                return 0

        response = req.get_http_session().get('http://'+self.__device_address+'/cgi/ems_data.xml',
                                              timeout=5)
        response.encoding = 'utf-8'
        response = response.text.replace("\n", "")
        root = ET.fromstring(response)

        power = get_xml_text("P")
        soc = get_xml_text("SOC") / 10

        imported, exported = self.sim_counter.sim_count(power)

        bat_state = BatState(
            power=power,
            soc=soc,
            imported=imported,
            exported=exported
        )
        self.store.set(bat_state)


component_descriptor = ComponentDescriptor(configuration_factory=VartaBatApiSetup)
