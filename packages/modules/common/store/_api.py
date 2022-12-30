import logging
from abc import abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")
log = logging.getLogger("soc."+__name__)


class ValueStore(Generic[T]):
    @abstractmethod
    def set(self, state: T) -> None:
        pass


class LoggingValueStore(Generic[T], ValueStore[T]):
    def __init__(self, delegate: ValueStore[T]):
        self.delegate = delegate

    def set(self, state: T) -> None:
        log.debug("Saving %s", state)
        self.delegate.set(state)
