#!/usr/bin/env python3
import logging
from typing import Dict, List, Union

from dataclass_utils import dataclass_from_dict
from helpermodules.cli import run_using_positional_cli_args
from modules.common import req
from modules.common.abstract_device import AbstractDevice, DeviceDescriptor
from modules.common.component_context import MultiComponentUpdateContext
from modules.json import bat, counter, inverter
from modules.json.config import (Json,
                                 JsonBatConfiguration,
                                 JsonBatSetup,
                                 JsonConfiguration,
                                 JsonCounterConfiguration,
                                 JsonCounterSetup,
                                 JsonInverterConfiguration,
                                 JsonInverterSetup)

log = logging.getLogger(__name__)


json_component_classes = Union[bat.JsonBat, counter.JsonCounter, inverter.JsonInverter]


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        "bat": bat.JsonBat,
        "counter": counter.JsonCounter,
        "inverter": inverter.JsonInverter
    }

    def __init__(self, device_config: Union[Dict, Json]) -> None:
        self.components = {}  # type: Dict[str, json_component_classes]
        try:
            self.device_config = dataclass_from_dict(Json, device_config)
        except Exception:
            log.exception("Fehler im Modul "+self.device_config.name)

    def add_component(self, component_config: Union[Dict, JsonBatSetup, JsonCounterSetup, JsonInverterSetup]) -> None:
        if isinstance(component_config, Dict):
            component_type = component_config["type"]
        else:
            component_type = component_config.type
        component_config = dataclass_from_dict(COMPONENT_TYPE_TO_MODULE[
            component_type].component_descriptor.configuration_factory, component_config)
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self.components["component"+str(component_config.id)] = self.COMPONENT_TYPE_TO_CLASS[component_type](
                self.device_config.id, component_config)
        else:
            raise Exception(
                "illegal component type " + component_type + ". Allowed values: " +
                ','.join(self.COMPONENT_TYPE_TO_CLASS.keys())
            )

    def update(self) -> None:
        log.debug("Start device reading " + str(self.components))
        if self.components:
            with MultiComponentUpdateContext(self.components):
                response = req.get_http_session().get(self.device_config.configuration.url, timeout=5)
                for component in self.components:
                    self.components[component].update(response.json())
        else:
            log.warning(
                self.device_config.name +
                ": Es konnten keine Werte gelesen werden, da noch keine Komponenten konfiguriert wurden."
            )


COMPONENT_TYPE_TO_MODULE = {
    "bat": bat,
    "counter": counter,
    "inverter": inverter
}


def read_legacy(url: str, component_config: Union[JsonBatSetup, JsonCounterSetup, JsonInverterSetup]) -> None:
    dev = Device(Json(configuration=JsonConfiguration(url=url)))
    dev.add_component(component_config)
    dev.update()


def read_legacy_bat(ip_address: str, jq_power: str, jq_soc: str):
    config = JsonBatConfiguration(jq_power=jq_power, jq_soc=jq_soc)
    read_legacy(ip_address, bat.component_descriptor.configuration_factory(id=None, configuration=config))


def read_legacy_counter(ip_address: str, jq_power: str, jq_imported: str, jq_exported: str):
    config = JsonCounterConfiguration(jq_power=jq_power, jq_imported=jq_imported, jq_exported=jq_exported)
    read_legacy(
        ip_address,
        counter.component_descriptor.configuration_factory(id=None, configuration=config))


def read_legacy_inverter(ip_address: str, jq_power: str, jq_exported: str, num: int):
    config = JsonInverterConfiguration(jq_power=jq_power, jq_exported=jq_exported)
    read_legacy(ip_address, inverter.component_descriptor.configuration_factory(id=num, configuration=config))


def main(argv: List[str]):
    run_using_positional_cli_args(
        {"bat": read_legacy_bat, "counter": read_legacy_counter, "inverter": read_legacy_inverter}, argv
    )


device_descriptor = DeviceDescriptor(configuration_factory=Json)
