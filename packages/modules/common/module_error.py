from enum import Enum
import paho.mqtt.publish as publish
import traceback

try:
    from ...helpermodules import compability
    from ...helpermodules import log
    from ...helpermodules import pub
except:
    # for 1.9 compability
    import os
    import sys
    from pathlib import Path
    parentdir2 = str(Path(os.path.abspath(__file__)).parents[2])
    sys.path.insert(0, parentdir2)
    from helpermodules import compability
    from helpermodules import log
    from helpermodules import pub

class ModuleError(Exception):
    def __init__(self, fault_str: str, fault_state:int) -> None:
        self.fault_str = fault_str
        self.fault_state = fault_state

    def store_error(self, component_num: int, component_type: str, component_name: str) -> None:
        try:
            log.MainLogger().debug(component_name+": FaultState "+str(self.fault_state)+", FaultStr "+self.fault_str+", Traceback: \n"+traceback.format_exc())
            ramdisk = compability.check_ramdisk_usage()
            if ramdisk:
                if component_type == "counter":
                    component_type = "evu"
                elif component_type == "bat":
                    component_type = "houseBattery"
                if component_num is not None:
                    pub.pub_single("openWB/set/"+component_type+"/"+str(component_num)+"/faultStr", self.fault_str)
                    pub.pub_single("openWB/set/"+component_type+"/"+str(component_num)+"/faultState", self.fault_state.value)
                else:
                    pub.pub_single("openWB/set/"+component_type+"/faultStr", self.fault_str)
                    pub.pub_single("openWB/set/"+component_type+"/faultState", self.fault_state.value)
            else:
                pub.pub("openWB/set/"+component_type+"/"+str(component_num)+"/get/fault_str", self.fault_str)
                pub.pub("openWB/set/"+component_type+"/"+str(component_num)+"/get/fault_state", self.fault_state.value)
        except Exception as e:
            log.MainLogger().exception("Fehler im Modul module_error")

class ModuleErrorLevels(Enum):
    NO_ERROR = 0
    WARNING = 1
    ERROR = 2