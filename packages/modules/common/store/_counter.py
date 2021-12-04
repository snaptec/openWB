from helpermodules import log, compatibility
from modules.common.component_state import CounterState
from modules.common.store import ValueStore
from modules.common.store._broker import pub_to_broker
from modules.common.store._ramdisk import ramdisk_write_to_files, ramdisk_write
from modules.common.store._util import process_error


class CounterValueStoreRamdisk(ValueStore[CounterState]):
    def __init__(self, component_num: int) -> None:
        self.num = component_num

    def set(self, counter_state: CounterState):
        try:
            ramdisk_write_to_files("evuv", counter_state.voltages, 1)
            ramdisk_write_to_files("bezuga", counter_state.currents, 1)
            ramdisk_write_to_files("bezugw", counter_state.powers, 0)
            ramdisk_write_to_files("evupf", counter_state.power_factors, 2)
            ramdisk_write("bezugkwh", counter_state.imported)
            ramdisk_write("einspeisungkwh", counter_state.exported)
            ramdisk_write("wattbezug", counter_state.power_all, 0)
            ramdisk_write("evuhz", counter_state.frequency, 2)
            log.MainLogger().info('EVU Watt: ' + str(counter_state.power_all))
            log.MainLogger().info('EVU Bezug: ' + str(counter_state.imported))
            log.MainLogger().info('EVU Einspeisung: ' + str(counter_state.exported))
        except Exception as e:
            process_error(e)


class CounterValueStoreBroker(ValueStore[CounterState]):
    def __init__(self, component_num: int) -> None:
        self.num = component_num

    def set(self, counter_state: CounterState):
        try:
            pub_to_broker("openWB/set/counter/" + str(self.num) + "/get/voltage", counter_state.voltages, 2)
            pub_to_broker("openWB/set/counter/" + str(self.num) + "/get/current", counter_state.currents, 2)
            pub_to_broker("openWB/set/counter/" + str(self.num) + "/get/power_phase", counter_state.powers, 2)
            pub_to_broker("openWB/set/counter/" + str(self.num) + "/get/power_factors", counter_state.power_factors, 2)
            pub_to_broker("openWB/set/counter/" + str(self.num) + "/get/imported", counter_state.imported)
            pub_to_broker("openWB/set/counter/" + str(self.num) + "/get/exported", counter_state.exported)
            pub_to_broker("openWB/set/counter/" + str(self.num) + "/get/power_all", counter_state.power_all)
            pub_to_broker("openWB/set/counter/" + str(self.num) + "/get/frequency", counter_state.frequency)
        except Exception as e:
            process_error(e)


def get_counter_value_store(component_num: int) -> ValueStore[CounterState]:
    if compatibility.is_ramdisk_in_use():
        return CounterValueStoreRamdisk(component_num)
    return CounterValueStoreBroker(component_num)
