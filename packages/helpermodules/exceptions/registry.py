import sys
from typing import Type, Optional, Callable, TypeVar, Generic, List, Union, Any

from modules.common import fault_state

T = TypeVar("T", bound=Exception)


def distance_to_type(base: Type, sub: Type):
    try:
        return sub.__mro__.index(base)
    except ValueError:
        return sys.maxsize


class RegistryEntry(Generic[T]):
    def __init__(self, type: Type[T], handler: Callable[[T], Any]):
        self.type = type
        self.handler = handler


class ExceptionRegistry:
    registry = []  # type: List[RegistryEntry]

    def translate_exception(self, exception: Exception) -> "fault_state.FaultState":
        entry = self.find_registry_entry(exception)
        if entry is None:
            return fault_state.FaultState.error("{} {}".format(type(exception), exception))
        if isinstance(entry.handler, str):
            return fault_state.FaultState.error(entry.handler)
        result = entry.handler(exception)
        if isinstance(result, fault_state.FaultState):
            return result
        return fault_state.FaultState.error(str(result))

    def find_registry_entry(self, exception: Exception) -> Optional[RegistryEntry]:
        score = sys.maxsize
        result = None
        for candidate in self.registry:
            candidate_score = distance_to_type(candidate.type, exception.__class__)
            if candidate_score < score:
                score = candidate_score
                result = candidate
        return result

    def add(self, type: Type[T], handler: Union[str, Callable[[T], Any]]):
        self.registry.append(RegistryEntry(type, handler))
