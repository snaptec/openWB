from helpermodules import compatibility
from modules.common.component_state import BatState
from modules.common.store import ValueStore
from modules.common.store._api import LoggingValueStore
from modules.common.store._broker import pub_to_broker
from modules.common.store._util import process_error
from modules.common.store.ramdisk import files


class BatteryValueStoreRamdisk(ValueStore[BatState]):
    def __init__(self, component_num: int) -> None:
        self.num = component_num

    def set(self, bat_state: BatState):
        try:
            files.battery.power.write(bat_state.power)
            files.battery.soc.write(bat_state.soc)
            files.battery.energy_imported.write(bat_state.imported)
            files.battery.energy_exported.write(bat_state.exported)
        except Exception as e:
            process_error(e)


class BatteryValueStoreBroker(ValueStore[BatState]):
    def __init__(self, component_num: int) -> None:
        self.num = component_num

    def set(self, bat_state: BatState):
        try:
            pub_to_broker("openWB/set/bat/"+str(self.num)+"/get/power", bat_state.power, 2)
            pub_to_broker("openWB/set/bat/"+str(self.num)+"/get/soc", bat_state.soc, 0)
            pub_to_broker("openWB/set/bat/"+str(self.num)+"/get/imported", bat_state.imported, 2)
            pub_to_broker("openWB/set/bat/"+str(self.num)+"/get/exported", bat_state.exported, 2)
        except Exception as e:
            process_error(e)


def get_bat_value_store(component_num: int) -> ValueStore[BatState]:
    return LoggingValueStore(
        (BatteryValueStoreRamdisk if compatibility.is_ramdisk_in_use() else BatteryValueStoreBroker)(component_num)
    )
