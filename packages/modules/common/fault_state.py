from enum import Enum
import traceback
from typing import Optional

from helpermodules import compatibility, exceptions, log, pub


class FaultStateLevel(Enum):
    NO_ERROR = 0
    WARNING = 1
    ERROR = 2


class ComponentInfo:
    def __init__(self, id: int, name: str, type: str) -> None:
        self.id = id
        self.name = name
        self.type = type

    @staticmethod
    def from_component_config(component_config: dict):
        return ComponentInfo(component_config["id"], component_config["name"], component_config["type"])


class FaultState(Exception):
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
                topic = self.__type_topic_mapping_comp(component_info.type)
                prefix = "openWB/set/" + topic + "/"
                if component_info.id is not None:
                    if topic == "lp":
                        prefix += str(component_info.id) + "/socF"
                    else:
                        prefix += str(component_info.id) + "/f"
                else:
                    prefix += "f"
                pub.pub_single(prefix + "aultStr", self.fault_str)
                pub.pub_single(prefix + "aultState", self.fault_state.value)
            else:
                topic = self.__type_topic_mapping(component_info.type)
                pub.Pub().pub(
                    "openWB/set/" + topic + "/" + str(component_info.id) + "/get/fault_str", self.fault_str)
                pub.Pub().pub(
                    "openWB/set/" + topic + "/" + str(component_info.id) + "/get/fault_state", self.fault_state.value)
        except Exception:
            log.MainLogger().exception("Fehler im Modul fault_state")

    def __type_topic_mapping(self, component_type: str) -> str:
        if "counter" in component_type:
            return "counter"
        elif "inverter" in component_type:
            return "pv"
        else:
            return component_type

    def __type_topic_mapping_comp(self, component_type: str) -> str:
        if "bat" in component_type:
            return "houseBattery"
        elif "counter" in component_type:
            return "evu"
        elif "inverter" in component_type:
            return "pv"
        elif "vehicle" in component_type:
            return "lp"
        else:
            raise Exception("Unbekannter Komponententyp: "+str(component_type))

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
