from typing import Union, List

from helpermodules.cli import run_using_positional_cli_args
from modules.common import store
from modules.common.abstract_device import AbstractDevice
from modules.common.component_context import SingleComponentUpdateContext
from modules.common.component_state import CarState
from modules.common.fault_state import ComponentInfo
from modules.evnotify import api


class EVNotifyConfiguration:
    def __init__(self, id: int, akey: str, token: str):
        self.id = id
        self.akey = akey
        self.token = token

    @staticmethod
    def from_dict(device_config: dict):
        keys = ["id", "akey", "token"]
        try:
            values = [device_config[key] for key in keys]
        except KeyError as e:
            raise Exception(
                "Illegal configuration <{}>: Expected object with properties: {}".format(device_config, keys)
            ) from e
        return EVNotifyConfiguration(*values)


class EVNotify(AbstractDevice):
    def __init__(self, device_config: Union[dict, EVNotifyConfiguration]):
        self.config = device_config \
            if isinstance(device_config, EVNotifyConfiguration) \
            else EVNotifyConfiguration.from_dict(device_config)
        self.value_store = store.get_car_value_store(self.config.id)
        self.component_info = ComponentInfo(self.config.id, "EVNotify", "vehicle")

    def add_component(self, component_config: dict) -> None:
        pass  # EVNotify does not have any components

    def update(self) -> None:
        with SingleComponentUpdateContext(self.component_info):
            self.value_store.set(CarState(soc=api.fetch_soc(self.config.akey, self.config.token)))


def evnotify_update(akey: str, token: str, charge_point: int):
    EVNotify(EVNotifyConfiguration(charge_point, akey, token)).update()


def main(argv: List[str]):
    run_using_positional_cli_args(evnotify_update, argv)
