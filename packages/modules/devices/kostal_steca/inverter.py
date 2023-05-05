#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import re
from math import isnan

from modules.common import req
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_inverter_value_store
from modules.devices.kostal_steca.config import KostalStecaInverterSetup


class KostalStecaInverter:
    def __init__(self, component_config: KostalStecaInverterSetup, ip_address: str) -> None:
        self.ip_address = ip_address
        self.component_config = component_config
        self.store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self) -> None:
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
        power = float(ET.fromstring(measurements).find(
            ".//Measurement[@Type='AC_Power']").get("Value")) * -1
        power = 0 if isnan(power) else int(power)

        # call for XML file and parse it for total produced kwh
        yields_xml = "yields.xml"
        yields = req.get_http_session().get("http://" + self.ip_address + "/" + yields_xml, timeout=2).text

        if self.component_config.configuration.variant == 0:
            exported = int(float(ET.fromstring(yields).find(
                ".//Yield[@Type='Produced']/YieldValue").get("Value")))
        else:
            yields_js = "gen.yield.total.chart.js"
            # call for .js file and parse it for total produced Wh
            yields = req.get_http_session().get("http://" + self.ip_address + "/" + yields_js, timeout=2).text
            match = re.search(r'"data":\s*\[\s*([^\]]*)\s*]', yields)
            try:
                exported = int(sum(float(s) * 1e6 for s in match.group(1).split(',')))
            except AttributeError:
                log.debug("PVkWh: Could not find 'data' in " + yields_js + ".")

        if "pvkwh_kostal_piko_MP" not in locals() or re.search(regex, str(exported)) is None:
            log.debug("PVkWh: NaN get prev. Value")
            with open("/var/www/html/openWB/ramdisk/pv2kwh", "r") as f:
                exported = f.read()

        inverter_state = InverterState(
            power=power,
            exported=exported,
        )
        self.store.set(inverter_state)


component_descriptor = ComponentDescriptor(configuration_factory=KostalStecaInverterSetup)
