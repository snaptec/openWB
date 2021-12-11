from helpermodules import log, compatibility
from modules.common.component_state import InverterState
from modules.common.fault_state import FaultState
from modules.common.store import ValueStore
from modules.common.store._broker import pub_to_broker
from modules.common.store._ramdisk import ramdisk_write, ramdisk_write_to_files


class InverterValueStoreRamdisk(ValueStore[InverterState]):
    def __init__(self, component_num: int) -> None:
        self.num = component_num

    def set(self, inverter_state: InverterState):
        try:
            if self.num == 1:
                filename_extension = ""
            elif self.num == 2:
                filename_extension = "2"
            else:
                raise FaultState.error("Unbekannte PV-Nummer " + str(self.num))
            ramdisk_write("pv" + filename_extension + "watt", inverter_state.power, 0)
            ramdisk_write("pv" + filename_extension + "kwh", inverter_state.counter, 3)
            ramdisk_write("pv" + filename_extension + "kwhk", inverter_state.counter / 1000, 3)
            ramdisk_write_to_files("pv" + filename_extension + "a", inverter_state.currents, 1)
            log.MainLogger().info('PV Watt: ' + str(inverter_state.power))
        except Exception as e:
            raise FaultState.from_exception(e)


class InverterValueStoreBroker(ValueStore[InverterState]):
    def __init__(self, component_num: int) -> None:
        self.num = component_num

    def set(self, inverter_state: InverterState):
        try:
            pub_to_broker("openWB/set/pv/" + str(self.num) + "/get/power", inverter_state.power, 2)
            pub_to_broker("openWB/set/pv/" + str(self.num) + "/get/counter", inverter_state.counter, 3)
            pub_to_broker("openWB/set/pv/" + str(self.num) + "/get/currents", inverter_state.currents, 1)
        except Exception as e:
            raise FaultState.from_exception(e)


def get_inverter_value_store(component_num: int) -> ValueStore[InverterState]:
    if compatibility.is_ramdisk_in_use():
        return InverterValueStoreRamdisk(component_num)
    return InverterValueStoreBroker(component_num)
