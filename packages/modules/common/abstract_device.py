from abc import abstractmethod
from typing import Type


class AbstractDevice:
    @abstractmethod
    def __init__(self, device_config: dict) -> None:
        pass

    @abstractmethod
    def add_component(self, component_config: dict) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass


class DeviceDescriptor:
    def __init__(self, configuration_factory: Type):
        self.configuration_factory = configuration_factory
