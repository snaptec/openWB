import logging
from typing import List

from helpermodules.cli import run_using_positional_cli_args
from modules.common.abstract_device import AbstractDevice
from modules.common.component_context import SingleComponentUpdateContext
from modules.common.req import get_http_session
from modules.discovergy import counter, inverter
from modules.discovergy.utils import DiscovergyComponent


def get_default_config(id: int = 0, **configuration) -> dict:
    return {
        "name": "Discovergy",
        "type": "discovergy",
        "id": id,
        "configuration": {
            "user": None,
            "password": None,
            **configuration
        }
    }


component_registry = {
    "counter": counter.create_component,
    "inverter": inverter.create_component
}

log = logging.getLogger(__name__)


class Device(AbstractDevice):
    def __init__(self, device_config: dict) -> None:
        settings = device_config["configuration"]
        self.__session = get_http_session()
        self.__session.auth = (settings["user"], settings["password"])
        self.components = []  # type: List[DiscovergyComponent]

    def add_component(self, component_config: dict) -> None:
        try:
            factory = component_registry[component_config["type"]]
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
    device = Device(get_default_config(user=user, password=password))

    if meter_id_counter:
        device.add_component(counter.get_default_config(meter_id=meter_id_counter))
    if meter_id_inverter:
        device.add_component(inverter.get_default_config(1, meter_id=meter_id_inverter))

    device.update()
    log.debug("Update completed")


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)
