import logging
from typing import TypeVar, Generic, Callable, Optional

from modules.common.component_context import SingleComponentUpdateContext
from modules.common.fault_state import ComponentInfo
from modules.common.store import ValueStore

T = TypeVar("T")
log = logging.getLogger("SMA Speedwire")


def _create_serial_matcher(serial: Optional[int]) -> Callable[[dict], bool]:
    if isinstance(serial, int):
        return lambda sma_data: sma_data["serial"] == serial
    if serial is not None:
        log.error("Serial <%s> must bei an int or None, but is <%s>. Assuming None.", serial, type(serial))
    return lambda _: True


class SpeedwireComponent(Generic[T]):
    def __init__(self,
                 value_store_factory: Callable[[int], ValueStore[T]],
                 parser: Callable[[dict], T],
                 component_config: dict):
        self.__value_store = value_store_factory(component_config["id"])
        self.__parser = parser
        self.__serial_matcher = _create_serial_matcher(component_config["configuration"]["serials"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def read_datagram(self, datagram: dict) -> bool:
        if self.__serial_matcher(datagram):
            with SingleComponentUpdateContext(self.component_info):
                self.__value_store.set(self.__parser(datagram))
            return True
        return False
