from modules.common.fault_state import ComponentInfo, FaultState


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

    def __init__(self, device_components: dict):
        self.__device_components = device_components

    def __enter__(self):
        return None

    def __exit__(self, exception_type, exception, exception_traceback) -> bool:
        fault_state = FaultState.from_exception(exception)
        for component in self.__device_components:
            fault_state.store_error(self.__device_components[component].component_info)
        return True
