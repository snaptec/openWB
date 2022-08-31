import logging
import threading
from typing import Optional, List, Union, Any, Dict

from modules.common.fault_state import ComponentInfo, FaultState

log = logging.getLogger("soc."+__name__)


class SingleComponentUpdateContext:
    """ Wenn die Werte der Komponenten nicht miteinander verrechnet werden, sollen, auch wenn bei einer Komponente ein
    Fehler auftritt, alle anderen dennoch ausgelesen werden. WR-Werte dienen nur statistischen Zwecken, ohne
    EVU-Werte ist aber keine Regelung möglich. Ein nicht antwortender WR soll dann nicht die Regelung verhindern.
        for component in self.components:
            with SingleComponentUpdateContext(component):
                component.update()
    """

    def __init__(self, component_info: ComponentInfo, update_always: bool = True):
        self.__component_info = component_info
        self.update_always = update_always

    def __enter__(self):
        log.debug("Update Komponente ['"+self.__component_info.name+"']")
        return None

    def __exit__(self, exception_type, exception, exception_traceback) -> bool:
        MultiComponentUpdateContext.override_subcomponent_state(self.__component_info, exception, self.update_always)
        return True


class MultiComponentUpdateContext:
    """ Wenn die Werte der Komponenten miteinander verrechnet werden, muss, wenn bei einer Komponente ein Fehler
    auftritt, für alle Komponenten der Fehlerzustand gesetzt werden, da aufgrund der Abhängigkeiten für alle Module
    keine Werte ermittelt werden können.
        with MultiComponentUpdateContext(self.components):
            for component in self.components:
                component.update()
    """
    __thread_local = threading.local()

    def __init__(self, device_components: Union[Dict[Any, Any], List[Any]]):
        self.__device_components = \
            device_components.values() if isinstance(device_components, dict) else device_components
        self.__ignored_components = []  # type: List[ComponentInfo]

    def __enter__(self):
        if hasattr(self.__thread_local, "active_context"):
            raise Exception("Nesting MultiComponentUpdateContext is not supported")
        MultiComponentUpdateContext.__thread_local.active_context = self
        log.debug("Update Komponenten " +
                  str([component.component_info.name for component in self.__device_components]))
        return None

    def __exit__(self, exception_type, exception, exception_traceback) -> bool:
        fault_state = FaultState.from_exception(exception)
        for component in self.__device_components:
            component_info = component.component_info
            if component_info not in self.__ignored_components:
                fault_state.store_error(component_info)
        delattr(MultiComponentUpdateContext.__thread_local, "active_context")
        return True

    def ignore_subcomponent_state(self, component: ComponentInfo):
        self.__ignored_components.append(component)

    @staticmethod
    def override_subcomponent_state(component_info: ComponentInfo, exception, update_always: bool):
        active_context = getattr(
            MultiComponentUpdateContext.__thread_local, "active_context", None
        )  # type: Optional[MultiComponentUpdateContext]
        if active_context:
            # If a MultiComponentUpdateContext is active, we need make sure that it will not override
            # the value for the individual component
            active_context.ignore_subcomponent_state(component_info)

        if exception:
            fault_state = FaultState.from_exception(exception)
        else:
            # Fehlerstatus nicht überschreiben
            if update_always:
                fault_state = FaultState.no_error()
            else:
                return
        fault_state.store_error(component_info)


class ErrorCounterContext:
    def __init__(self, exceeded_msg: str):
        self.__error_counter = 0
        self.__exceeded_msg = exceeded_msg

    def __enter__(self):
        return None

    def __exit__(self, exception_type, exception, exception_traceback) -> bool:
        if exception:
            self.__error_counter += 1
            raise exception
        return True

    def error_counter_exceeded(self) -> bool:
        if self.__error_counter > 5:
            log.error(self.__exceeded_msg)
            return True
        else:
            return False

    def reset_error_counter(self):
        self.__error_counter = 0
