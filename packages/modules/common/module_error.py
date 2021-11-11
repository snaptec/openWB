from enum import Enum
import traceback

try:
    from ...helpermodules import compatibility
    from ...helpermodules import log
    from ...helpermodules import pub
except (ImportError, ValueError):
    # for 1.9 compatibility
    from helpermodules import compatibility
    from helpermodules import log
    from helpermodules import pub


class ModuleErrorLevel(Enum):
    NO_ERROR = 0
    WARNING = 1
    ERROR = 2


class ModuleError(Exception):
    def __init__(self, fault_str: str, fault_state: ModuleErrorLevel) -> None:
        self.fault_str = fault_str
        self.fault_state = fault_state

    def store_error(self, component_num: int, component_type: str, component_name: str) -> None:
        try:
            log.MainLogger().debug(
                component_name+": FaultState "+str(self.fault_state)+", FaultStr "+self.fault_str+", Traceback: \n" +
                traceback.format_exc()
            )
            ramdisk = compatibility.is_ramdisk_in_use()
            if ramdisk:
                if component_type == "counter":
                    component_type = "evu"
                elif component_type == "bat":
                    component_type = "houseBattery"
                elif component_type == "inverter":
                    component_type = "pv"
                prefix = "openWB/set/"+component_type+"/"
                if component_num is not None:
                    prefix += str(component_num)+"/"
                pub.pub_single(prefix+"faultStr", self.fault_str)
                pub.pub_single(prefix+"faultState", self.fault_state.value)
            else:
                pub.pub("openWB/set/"+component_type+"/"+str(component_num)+"/get/fault_str", self.fault_str)
                pub.pub("openWB/set/"+component_type+"/"+str(component_num)+"/get/fault_state", self.fault_state.value)
        except Exception:
            log.MainLogger().exception("Fehler im Modul module_error")
