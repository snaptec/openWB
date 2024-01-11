#!/usr/bin/env python3
import logging
from typing import Optional, Tuple
import xml.etree.ElementTree as ET
import re

from modules.common import req
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_inverter_value_store
from modules.devices.kostal_steca.config import KostalStecaInverterSetup

log = logging.getLogger(__name__)


class KostalStecaInverter:
    def __init__(self, component_config: KostalStecaInverterSetup, ip_address: str) -> None:
        self.ip_address = ip_address
        self.component_config = component_config
        self.store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self) -> None:
        power, exported = self.get_values()
        self.store.set(InverterState(power=power, exported=exported))

    def get_values(self) -> Tuple[float, Optional[float]]:
        # RainerW 8th of April 2020
        # Unfortunately Kostal has introduced the third version of interface: XML
        # This script is for Kostal_Piko_MP_plus and StecaGrid coolcept (single phase inverter)
        # In fact Kostal is not developing own single phase inverter anymore but is sourcing them from Steca
        # If you have the chance to test this module for the latest three phase inverter from Kostal (Plenticore)
        # or Steca (coolcept3 or coolcept XL) let us know if it works
        # DetMoerk 20210323: Anpassung für ein- und dreiphasige WR der Serie. Anstatt eine feste Zeile aus
        # dem Ergebnis zu schneiden wird nach der Zeile mit AC_Power gesucht.

        # call for XML file and parse it for current PV power
        measurements = req.get_http_session().get("http://" + self.ip_address + "/measurements.xml", timeout=2).text
        power_raw = ET.fromstring(measurements).find(".//Measurement[@Type='AC_Power']").get("Value")
        power = 0 if power_raw is None else float(power_raw) * -1

        if self.component_config.configuration.variant_steca:
            # call for XML file and parse it for total produced kwh
            yields = req.get_http_session().get("http://" + self.ip_address + "/yields.xml", timeout=2).text
            exported = float(ET.fromstring(yields).find(".//Yield[@Type='Produced']/YieldValue").get("Value"))
        else:
            # call for .js file and parse it for total produced Wh
            yields = req.get_http_session().get("http://" + self.ip_address + "/gen.yield.total.chart.js",
                                                timeout=2).text
            match = re.search(r'"data":\s*\[\s*([^\]]*)\s*]', yields)
            try:
                exported = sum(float(s) * 1e6 for s in match.group(1).split(','))
            except AttributeError:
                log.debug("PVkWh: Could not find 'data' in gen.yield.total.chart.js.")
                exported = None

        return power, exported


component_descriptor = ComponentDescriptor(configuration_factory=KostalStecaInverterSetup)
