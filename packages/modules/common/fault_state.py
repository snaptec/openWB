import functools
import logging
import traceback
from enum import IntEnum
from typing import Optional, Callable, TypeVar

from helpermodules import compatibility, exceptions, pub
from modules.common import component_type
from modules.common.component_setup import ComponentSetup

log = logging.getLogger(__name__)


class FaultStateLevel(IntEnum):
    NO_ERROR = 0
    WARNING = 1
    ERROR = 2


class ComponentInfo:
    def __init__(self,
                 id: int,
                 name: str,
                 type: str,
                 hostname: str = "localhost",
                 parent_hostname: Optional[str] = None) -> None:
        self.id = id
        self.name = name
        self.type = type
        self.hostname = hostname
        self.parent_hostname = parent_hostname

    @staticmethod
    def from_component_config(component_config: ComponentSetup,
                              hostname: str = "localhost",
                              parent_hostname: Optional[str] = None):
        return ComponentInfo(component_config.id,
                             component_config.name,
                             component_config.type,
                             hostname,
                             parent_hostname)


class FaultState(Exception):
    def __init__(self, fault_str: str, fault_state: FaultStateLevel) -> None:
        self.fault_str = fault_str
        self.fault_state = fault_state

    def store_error(self, component_info: ComponentInfo) -> None:
        try:
            if self.fault_state != FaultStateLevel.NO_ERROR:
                log.error(component_info.name + ": FaultState " +
                          str(self.fault_state) + ", FaultStr " +
                          self.fault_str + ", Traceback: \n" +
                          traceback.format_exc())
            ramdisk = compatibility.is_ramdisk_in_use()
            if ramdisk:
                topic = component_type.type_topic_mapping_comp(component_info.type)
                prefix = "openWB/set/" + topic + "/"
                if component_info.type != "counter" and component_info.type != "bat":
                    if component_type == "vehicle":
                        prefix += str(component_info.id) + "/socFault"
                    else:
                        prefix += str(component_info.id) + "/fault"
                else:
                    prefix += "fault"
                pub.pub_single(prefix + "Str", self.fault_str, hostname=component_info.hostname)
                pub.pub_single(prefix + "State", self.fault_state.value, hostname=component_info.hostname)
                if "chargepoint" in component_info.type:
                    pub.pub_single("openWB/set/" + topic + "/" + str(component_info.id) +
                                   "/get/fault_str", self.fault_str, hostname=component_info.hostname)
                    pub.pub_single("openWB/set/" + topic + "/" + str(component_info.id) +
                                   "/get/fault_state", self.fault_state.value, hostname=component_info.hostname)
            else:
                topic = component_type.type_to_topic_mapping(component_info.type)
                pub.Pub().pub("openWB/set/" + topic + "/" + str(component_info.id) + "/get/fault_str", self.fault_str)
                pub.Pub().pub(
                    "openWB/set/" + topic + "/" + str(component_info.id) + "/get/fault_state", self.fault_state.value)
                if component_info.parent_hostname:
                    pub.pub_single("openWB/set/" + topic + "/" + str(component_info.id) +
                                   "/get/fault_str", self.fault_str, hostname=component_info.parent_hostname)
                    pub.pub_single(
                        "openWB/set/" + topic + "/" + str(component_info.id) + "/get/fault_state",
                        self.fault_state.value, hostname=component_info.parent_hostname)
        except Exception:
            log.exception("Fehler im Modul fault_state")

    @staticmethod
    def error(message: str) -> "FaultState":
        return FaultState(message, FaultStateLevel.ERROR)

    @staticmethod
    def warning(message: str) -> "FaultState":
        return FaultState(message, FaultStateLevel.WARNING)

    @staticmethod
    def no_error() -> "FaultState":
        return FaultState("Kein Fehler.", FaultStateLevel.NO_ERROR)

    @staticmethod
    def from_exception(exception: Optional[Exception] = None) -> "FaultState":
        if exception is None:
            return FaultState.no_error()
        if isinstance(exception, FaultState):
            return exception
        return exceptions.get_default_exception_registry().translate_exception(exception)


T_C = TypeVar("T_C", bound=Callable)


def exceptions_to_fault_state(module_name: str) -> Callable[[T_C], T_C]:
    def decorate(delegate: T_C) -> T_C:
        @functools.wraps(delegate)
        def wrapper(*args, **kwargs):
            try:
                return delegate(*args, **kwargs)
            except Exception as e:
                if isinstance(e, FaultState):
                    raise
                else:
                    raise FaultState.error(module_name + " " + str(type(e)) + " " + str(e)) from e
        return wrapper
    return decorate
