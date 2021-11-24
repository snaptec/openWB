from abc import abstractmethod
from typing import Union

from modules.common.fault_state import FaultState, FaultStateLevel


class AbstractDevice:
    @abstractmethod
    def __init__(self, device_config: dict) -> None:
        pass

    @abstractmethod
    def add_component(self, component_config: dict) -> None:
        pass

    @abstractmethod
    def get_values(self) -> None:
        pass


def clear_all_error_states(components) -> None:
    for component in components:
        FaultState("Kein Fehler.", FaultStateLevel.NO_ERROR).store_error(component.component_info)


def process_component_error(e: Union[FaultState, Exception], component) -> None:
    if type(e) is FaultState:
        e.store_error(component.component_info)
    else:
        FaultState(str(type(e)) + " " + str(e), FaultStateLevel.ERROR).store_error(component.component_info)
