from typing import Union, List

from dataclass_utils import dataclass_from_dict
from helpermodules.cli import run_using_positional_cli_args
from modules.common import store
from modules.common.abstract_device import DeviceDescriptor
from modules.common.abstract_soc import AbstractSoc
from modules.common.component_context import SingleComponentUpdateContext
from modules.common.component_state import CarState
from modules.common.fault_state import ComponentInfo
from modules.vehicles.evnotify import api
from modules.vehicles.evnotify.config import EVNotify, EVNotifyConfiguration


class Soc(AbstractSoc):
    def __init__(self, device_config: Union[dict, EVNotify], vehicle: int):
        self.config = dataclass_from_dict(EVNotify, device_config)
        self.vehicle = vehicle
        self.store = store.get_car_value_store(self.vehicle)
        self.component_info = ComponentInfo(self.vehicle, self.config.name, "vehicle")

    def update(self, charge_state: bool = False) -> None:
        with SingleComponentUpdateContext(self.component_info):
            self.store.set(CarState(soc=api.fetch_soc(
                self.config.configuration.akey, self.config.configuration.token)))


def evnotify_update(akey: str, token: str, charge_point: int):
    Soc(EVNotify(configuration=EVNotifyConfiguration(charge_point, akey, token)), charge_point).update(False)


def main(argv: List[str]):
    run_using_positional_cli_args(evnotify_update, argv)


device_descriptor = DeviceDescriptor(configuration_factory=EVNotify)
