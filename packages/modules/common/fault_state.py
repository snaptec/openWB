from enum import Enum
import traceback
from typing import Optional

from helpermodules import compatibility
from helpermodules import log
from helpermodules import pub


class FaultStateLevel(Enum):
    NO_ERROR = 0
    WARNING = 1
    ERROR = 2


class ComponentInfo:
    def __init__(self, id: int, name: str, type: str) -> None:
        self.id = id
        self.name = name
        self.type = type


class FaultState(Exception):
    type_name_mapping = {"bat": "houseBattery", "counter": "evu", "inverter": "pv"}

    def __init__(self, fault_str: str, fault_state: FaultStateLevel) -> None:
        self.fault_str = fault_str
        self.fault_state = fault_state

    def store_error(self, component_info: ComponentInfo) -> None:
        try:
            if self.fault_state is not FaultStateLevel.NO_ERROR:
                log.MainLogger().error(component_info.name + ": FaultState " +
                                       str(self.fault_state) + ", FaultStr " +
                                       self.fault_str + ", Traceback: \n" +
                                       traceback.format_exc())
            ramdisk = compatibility.is_ramdisk_in_use()
            if ramdisk:
                type = self.type_name_mapping.get(component_info.type, component_info.type)
                prefix = "openWB/set/" + type + "/"
                if component_info.id is not None:
                    prefix += str(component_info.id) + "/"
                pub.pub_single(prefix + "faultStr", self.fault_str)
                pub.pub_single(prefix + "faultState", self.fault_state.value)
            else:
                pub.pub(
                    "openWB/set/" + component_info.type + "/" + str(component_info.id) +
                    "/get/fault_str", self.fault_str)
                pub.pub(
                    "openWB/set/" + component_info.type + "/" + str(component_info.id) +
                    "/get/fault_state", self.fault_state.value)
        except Exception:
            log.MainLogger().exception("Fehler im Modul fault_state")

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
    def from_exception(exception: Optional[Exception], level: FaultStateLevel = FaultStateLevel.ERROR) -> "FaultState":
        if exception is None:
            return FaultState.no_error()
        if isinstance(exception, FaultState):
            return exception
        return FaultState(str(type(exception)) + " " + str(exception), level)
