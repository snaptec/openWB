from typing import List

from modules.common.fault_state import ComponentInfo, FaultState


class BatState:
    def __init__(self, imported: float, exported: float, power: float, soc: int):
        self.imported = imported
        self.exported = exported
        self.power = power
        self.soc = soc


class CounterState:
    def __init__(self,
                 imported: float = 0,
                 exported: float = 0,
                 power_all: float = 0,
                 voltages: List[float] = None,
                 currents: List[float] = None,
                 powers: List[float] = None,
                 power_factors: List[float] = None,
                 frequency: float = 50):
        if voltages is None:
            voltages = [0]*3
        self.voltages = voltages
        if currents is None:
            currents = [0]*3
        self.currents = currents
        if powers is None:
            powers = [0]*3
        self.powers = powers
        if power_factors is None:
            power_factors = [0]*3
        self.power_factors = power_factors
        self.imported = imported
        self.exported = exported
        self.power_all = power_all
        self.frequency = frequency


class InverterState:
    def __init__(
        self,
        counter: float,
        power: float,
        currents: List[float] = None,
    ):
        if currents is None:
            currents = [0]*3
        self.currents = currents
        self.power = power
        self.counter = counter


class SingleComponentUpdateContext:
    """ Wenn die Werte der Komponenten nicht miteinander verrechnet werden, sollen, auch wenn bei einer Komponente ein
    Fehler auftritt, alle anderen dennnoch ausgelesen werden. WR-Werte dienen nur statistisichen Zwecken, ohne
    EVU-Werte ist aber keine Regelung möglich. Ein nicht antwortender WR soll dann nicht die Regelung verhindern.
        for component in self._components:
            with SingleComponentUpdateContext(component):
                component.update()
    """

    def __init__(self, component_info: ComponentInfo):
        self.__component_info = component_info

    def __enter__(self):
        return None

    def __exit__(self, exception_type, exception, exception_traceback) -> bool:
        fault_state = FaultState.from_exception(exception)
        fault_state.store_error(self.__component_info)
        return True


class MultiComponentUpdateContext:
    """ Wenn die Werte der Komponenten miteinander verrechnet werden, muss, wenn bei einer Komponente ein Fehler
    auftritt, für alle Komponenten der Fehlerzustand gesetzt werden, da aufgrund der Abhängigkeiten für alle Module
    keine Werte ermittelt werden können.
        with MultiComponentUpdateContext(self._components):
            for component in self._components:
                component.update()
    """

    def __init__(self, device_components: list):
        self.__device_components = device_components

    def __enter__(self):
        return None

    def __exit__(self, exception_type, exception, exception_traceback) -> bool:
        fault_state = FaultState.from_exception(exception)
        for component in self.__device_components:
            fault_state.store_error(component.component_info)
        return True
