from helpermodules import compatibility
from modules.common.component_state import CounterState
from modules.common.store import ValueStore
from modules.common.store._api import LoggingValueStore
from modules.common.store._broker import pub_to_broker
from modules.common.store._util import process_error
from modules.common.store.ramdisk import files


class CounterValueStoreRamdisk(ValueStore[CounterState]):
    def set(self, counter_state: CounterState):
        try:
            files.evu.voltages.write(counter_state.voltages)
            if counter_state.currents:
                files.evu.currents.write(counter_state.currents)
            files.evu.powers_import.write(counter_state.powers)
            files.evu.power_factors.write(counter_state.power_factors)
            files.evu.energy_import.write(counter_state.imported)
            files.evu.energy_export.write(counter_state.exported)
            files.evu.power_import.write(int(counter_state.power))
            files.evu.frequency.write(counter_state.frequency)
        except Exception as e:
            process_error(e)


class CounterValueStoreBroker(ValueStore[CounterState]):
    def __init__(self, component_num: int) -> None:
        self.num = component_num

    def set(self, counter_state: CounterState):
        try:
            pub_to_broker("openWB/set/counter/" + str(self.num) + "/get/voltages", counter_state.voltages, 2)
            if counter_state.currents:
                pub_to_broker("openWB/set/counter/" + str(self.num) + "/get/currents", counter_state.currents, 2)
            pub_to_broker("openWB/set/counter/" + str(self.num) + "/get/powers", counter_state.powers, 2)
            pub_to_broker("openWB/set/counter/" + str(self.num) + "/get/power_factors", counter_state.power_factors, 2)
            pub_to_broker("openWB/set/counter/" + str(self.num) + "/get/imported", counter_state.imported)
            pub_to_broker("openWB/set/counter/" + str(self.num) + "/get/exported", counter_state.exported)
            pub_to_broker("openWB/set/counter/" + str(self.num) + "/get/power", counter_state.power)
            pub_to_broker("openWB/set/counter/" + str(self.num) + "/get/frequency", counter_state.frequency)
        except Exception as e:
            process_error(e)


def get_counter_value_store(component_num: int) -> ValueStore[CounterState]:
    return LoggingValueStore(
        CounterValueStoreRamdisk() if compatibility.is_ramdisk_in_use() else CounterValueStoreBroker(component_num)
    )
