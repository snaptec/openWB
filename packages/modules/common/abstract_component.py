from abc import abstractmethod
from typing import Generic, TypeVar

try:
    from ..common.module_error import ComponentInfo, ModuleError, ModuleErrorLevel
    from ..common.store import ValueStore
except (ImportError, ValueError, SystemError):
    from modules.common.module_error import ComponentInfo, ModuleError, ModuleErrorLevel
    from modules.common.store import ValueStore

T = TypeVar("T")


class AbstractComponent(Generic[T]):
    @abstractmethod
    def __init__(self, device_id: int, component_config: dict, tcp_client) -> None:
        pass

    @abstractmethod
    def get_values(self) -> T:
        pass

    @abstractmethod
    def get_component_info(self) -> ComponentInfo:
        pass


class ComponentUpdater(Generic[T]):
    def __init__(self, component: AbstractComponent[T],
                 value_store: ValueStore[T]) -> None:
        self.component = component
        self.value_store = value_store

    def get_values(self) -> T:
        try:
            state = self.component.get_values()
        except Exception as e:
            self.process_error(e)
        else:
            ModuleError("Kein Fehler.", ModuleErrorLevel.NO_ERROR).store_error(self.component.get_component_info())
            return state

    def set_values(self, state: T) -> None:
        try:
            self.value_store.set(state)
        except Exception as e:
            self.process_error(e)

    def process_error(self, e):
        if type(e) == ModuleError:
            e.store_error(self.component.get_component_info())
            raise ModuleError("", ModuleErrorLevel.ERROR)
        else:
            ModuleError(
                str(type(e)) + " " + str(e),
                ModuleErrorLevel.ERROR).store_error(
                self.component.get_component_info())
            raise ModuleError("", ModuleErrorLevel.ERROR)
