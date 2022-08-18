import logging
from typing import Dict, List, Union

from helpermodules.cli import run_using_positional_cli_args
from modules.common.abstract_device import AbstractDevice, DeviceDescriptor
from modules.common.component_context import SingleComponentUpdateContext
from modules.common.req import get_http_session
from modules.discovergy import counter, inverter
from modules.discovergy.utils import DiscovergyComponent
from modules.discovergy.config import (
    Discovergy,
    DiscovergyConfiguration,
    DiscovergyCounterConfiguration,
    DiscovergyCounterSetup,
    DiscovergyInverterConfiguration,
    DiscovergyInverterSetup)
from dataclass_utils import dataclass_from_dict


component_registry = {
    "counter": counter.create_component,
    "inverter": inverter.create_component
}

log = logging.getLogger(__name__)


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_MODULE = {
        "counter": counter,
        "inverter": inverter
    }

    def __init__(self, device_config: Union[Dict, Discovergy]) -> None:
        settings = dataclass_from_dict(Discovergy, device_config).configuration
        self.__session = get_http_session()
        self.__session.auth = (settings.user, settings.password)
        self.components = []  # type: List[DiscovergyComponent]

    def add_component(self, component_config: Union[Dict, DiscovergyCounterSetup, DiscovergyInverterSetup]) -> None:
        try:
            if isinstance(component_config, Dict):
                component_type = component_config["type"]
            else:
                component_type = component_config.type
            factory = component_registry[component_type]
            component_config = dataclass_from_dict(self.COMPONENT_TYPE_TO_MODULE[
                component_type].component_descriptor.configuration_factory, component_config)
        except KeyError as e:
            raise Exception(
                "Unknown component type <%s>, known types are: <%s>", e, ','.join(component_registry.keys())
            )
        self.components.append(factory(component_config))

    def update(self) -> None:
        for component in self.components:
            with SingleComponentUpdateContext(component.component_info):
                component.update(self.__session)


def read_legacy(user: str, password: str, meter_id_counter: str, meter_id_inverter: str):
    log.debug("Beginning update")
    device = Device(Discovergy(configuration=DiscovergyConfiguration(user=user, password=password))
                    )
    if meter_id_counter:
        device.add_component(DiscovergyCounterSetup(id=None,
                                                    configuration=DiscovergyCounterConfiguration(
                                                        meter_id=meter_id_counter)))
    if meter_id_inverter:
        device.add_component(DiscovergyInverterSetup(id=1,
                                                     configuration=DiscovergyInverterConfiguration(
                                                         meter_id=meter_id_inverter)))

    device.update()
    log.debug("Update completed")


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)


device_descriptor = DeviceDescriptor(configuration_factory=Discovergy)
