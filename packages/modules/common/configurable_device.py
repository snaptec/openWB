import inspect
from typing import TypeVar, Generic, Dict, Any, Callable, Iterable, List

from dataclass_utils import dataclass_from_dict
from modules.common.abstract_device import AbstractDevice
from modules.common.component_context import SingleComponentUpdateContext, MultiComponentUpdateContext
from modules.common.fault_state import FaultState

T_DEVICE_CONFIG = TypeVar("T_DEVICE_CONFIG")
T_COMPONENT = TypeVar("T_COMPONENT")
T_COMPONENT_CONFIG = TypeVar("T_COMPONENT_CONFIG")

ComponentUpdater = Callable[[Iterable[T_COMPONENT]], None]
ComponentFactory = Callable[[T_COMPONENT_CONFIG], T_COMPONENT]


class IndependentComponentUpdater(Generic[T_COMPONENT]):
    def __init__(self, updater: Callable[[T_COMPONENT], None]):
        self.__updater = updater

    def __call__(self, components: Iterable[T_COMPONENT]) -> None:
        for component in components:
            with SingleComponentUpdateContext(component.component_info):
                self.__updater(component)


class MultiComponentUpdater:
    def __init__(self, updater: Callable[[List[T_COMPONENT]], None]):
        self.__updater = updater

    def __call__(self, components: Iterable[T_COMPONENT]) -> None:
        components_list = list(components)
        with MultiComponentUpdateContext(components_list):
            if not components:
                raise FaultState.warning("Keine Komponenten konfiguriert")
            self.__updater(components_list)


class ComponentFactoryByType(Generic[T_COMPONENT, T_COMPONENT_CONFIG]):
    def __init__(self, **type_to_factory: ComponentFactory[Any, T_COMPONENT]):
        self.__type_to_factory = type_to_factory

    def __call__(self, component_config: T_COMPONENT_CONFIG) -> T_COMPONENT:
        component_type = component_config["type"] if isinstance(component_config, dict) else component_config.type
        try:
            factory = self.__type_to_factory[component_type]
        except KeyError as e:
            raise Exception(
                "Unknown component type <%s>, known types are: <%s>", e, ','.join(self.__type_to_factory.keys())
            )
        arg_spec = inspect.getfullargspec(factory)
        if len(arg_spec.args) != 1:
            raise Exception(
                "Expected function with single argument, however factory for %s has args: %s" %
                (component_type, arg_spec.args)
            )
        required_type = arg_spec.annotations[arg_spec.args[0]]
        return factory(dataclass_from_dict(required_type, component_config))


class ConfigurableDevice(Generic[T_COMPONENT, T_DEVICE_CONFIG, T_COMPONENT_CONFIG], AbstractDevice):
    def __init__(self,
                 device_config: T_DEVICE_CONFIG,
                 component_factory: ComponentFactory[Any, T_COMPONENT],
                 component_updater: ComponentUpdater[T_COMPONENT]) -> None:
        self.__component_factory = component_factory
        self.__component_updater = component_updater
        self.device_config = device_config
        self.components = {}  # type: Dict[str, T_COMPONENT]

    def add_component(self, component_config: T_COMPONENT_CONFIG) -> None:
        self.components["component" + str(component_config.id)] = self.__component_factory(component_config)

    def update(self):
        self.__component_updater(self.components.values())
