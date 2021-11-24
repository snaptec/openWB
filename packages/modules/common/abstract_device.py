from abc import abstractmethod

from packages.modules.common.fault_state import FaultState, FaultStateLevel


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


def clear_all_error_states(device):
    for component in device._components:
        FaultState("Kein Fehler.", FaultStateLevel.NO_ERROR).store_error(component.get_component_info())


def process_component_error(e, component):
    if type(e) is FaultState:
        e.store_error(component.get_component_info())
    else:
        FaultState(str(type(e)) + " " + str(e), FaultStateLevel.ERROR).store_error(component.get_component_info())
