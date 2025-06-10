#!/usr/bin/env python3
import json
import logging
from typing import Iterable, List, Optional, Union

from helpermodules.cli import run_using_positional_cli_args
from modules.common.abstract_device import DeviceDescriptor
from modules.common.component_context import SingleComponentUpdateContext
from modules.common.configurable_device import ComponentFactoryByType, ConfigurableDevice, MultiComponentUpdater
from modules.common import req
from modules.devices.solar_log.counter import SolarLogCounter
from modules.devices.solar_log.config import SolarLog, SolarLogCounterSetup, SolarLogInverterSetup
from modules.devices.solar_log.inverter import SolarLogInverter
log = logging.getLogger(__name__)


def create_device(device_config: SolarLog):
    def create_counter_component(component_config: SolarLogCounterSetup):
        return SolarLogCounter(device_config.id, component_config)

    def create_inverter_component(component_config: SolarLogInverterSetup):
        return SolarLogInverter(device_config.id, component_config)

    def update_components(components: Iterable[Union[SolarLogCounter, SolarLogInverter]]):
        response = req.get_http_session().post('http://'+device_config.ip_adress+'/getjp',
                                               data=json.dumps({"801": {"170": None}}), timeout=5).json()
        for component in components:
            component.update(response)

    return ConfigurableDevice(
        device_config=device_config,
        component_factory=ComponentFactoryByType(
            counter=create_counter_component,
            inverter=create_inverter_component,
        ),
        component_updater=MultiComponentUpdater(update_components)
    )


def read_legacy(component_type: str, ip_address: str, note_bat: Optional[int] = 0) -> None:
    log.debug('Solar-Log ip_address: ' + ip_address)
    if component_type == "inverter":
        inverter = SolarLogInverter(None, SolarLogInverterSetup(id=1))
        with SingleComponentUpdateContext(inverter.component_info):
            response = req.get_http_session().post('http://'+ip_address+'/getjp',
                                                   data=json.dumps({"801": {"170": None}}), timeout=5).json()
            inverter.update(response)
    elif component_type == "counter":
        inverter = SolarLogInverter(None, SolarLogInverterSetup(id=1))
        counter = SolarLogCounter(None, SolarLogCounterSetup(id=None))
        with SingleComponentUpdateContext(counter.component_info):
            # WR bei WR oder EVU-Modul immer auslesen
            response = req.get_http_session().post('http://'+ip_address+'/getjp',
                                                   data=json.dumps({"801": {"170": None}}), timeout=5).json()
            inverter.update(response)
            power = counter.get_power(response)
            pvwatt = int(float(response["801"]["170"]["101"]))
            power = power - pvwatt

            if note_bat == 1:
                with open("ramdisk/speicherleistung", "r") as f:
                    speicherleistung = int(float(f.read()))
                power = power + speicherleistung
            counter.store_values(power)


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)


device_descriptor = DeviceDescriptor(configuration_factory=SolarLog)
