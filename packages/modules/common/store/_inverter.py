from helpermodules import compatibility
from modules.common.component_state import InverterState
from modules.common.fault_state import FaultState
from modules.common.store import ValueStore
from modules.common.store._api import LoggingValueStore
from modules.common.store._broker import pub_to_broker
from modules.common.store.ramdisk import files


class InverterValueStoreRamdisk(ValueStore[InverterState]):
    def __init__(self, component_num: int) -> None:
        self.__pv = files.pv[component_num - 1]

    def set(self, inverter_state: InverterState):
        try:
            self.__pv.power.write(inverter_state.power)
            self.__pv.energy.write(inverter_state.counter)
            self.__pv.energy_k.write(inverter_state.counter / 1000)
            self.__pv.currents.write(inverter_state.currents)
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
    return LoggingValueStore(
        (InverterValueStoreRamdisk if compatibility.is_ramdisk_in_use() else InverterValueStoreBroker)(component_num)
    )
