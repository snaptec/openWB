from abc import abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class ValueStore(Generic[T]):
    @abstractmethod
    def set(self, state: T) -> None:
        pass
