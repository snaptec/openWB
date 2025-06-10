from modules.common.component_state import ChargepointState
from modules.common.store import ValueStore
from modules.common.store._api import LoggingValueStore
from modules.common.store._broker import pub_to_broker
from modules.common.store.ramdisk import files
from helpermodules import compatibility


class ChargepointValueStoreRamdisk(ValueStore[ChargepointState]):
    def __init__(self, cp_id: int):
        self.num = cp_id

    def set(self, cp_state: ChargepointState):
        charge_point = files.charge_points[self.num]
        charge_point.is_charging.write(cp_state.charge_state)
        charge_point.voltages.write(cp_state.voltages)
        charge_point.currents.write(cp_state.currents)
        charge_point.energy.write(cp_state.imported/1000)
        charge_point.is_plugged.write(cp_state.plug_state)
        charge_point.power.write(int(cp_state.power))


class ChargepointValueStoreBroker(ValueStore[ChargepointState]):
    def __init__(self, cp_id: int):
        self.num = cp_id

    def set(self, state: ChargepointState) -> None:
        pub_to_broker("openWB/set/chargepoint/" + str(self.num) + "/get/voltages", state.voltages, 2)
        pub_to_broker("openWB/set/chargepoint/" + str(self.num) + "/get/currents", state.currents, 2)
        pub_to_broker("openWB/set/chargepoint/" + str(self.num) + "/get/power_factors", state.power_factors, 2)
        pub_to_broker("openWB/set/chargepoint/" + str(self.num) + "/get/imported", state.imported, 2)
        pub_to_broker("openWB/set/chargepoint/" + str(self.num) + "/get/exported", state.exported, 2)
        pub_to_broker("openWB/set/chargepoint/" + str(self.num) + "/get/power", state.power, 2)
        pub_to_broker("openWB/set/chargepoint/" + str(self.num) + "/get/powers", state.powers, 2)
        pub_to_broker("openWB/set/chargepoint/" + str(self.num) + "/get/frequency", state.frequency, 2)
        pub_to_broker("openWB/set/chargepoint/" + str(self.num) + "/get/phases_in_use", state.phases_in_use, 2)
        pub_to_broker("openWB/set/chargepoint/" + str(self.num) + "/get/charge_state", state.charge_state, 2)
        pub_to_broker("openWB/set/chargepoint/" + str(self.num) + "/get/plug_state", state.plug_state, 2)
        pub_to_broker("openWB/set/chargepoint/" + str(self.num) + "/get/read_tag", state.read_tag)


def get_chargepoint_value_store(id: int) -> ValueStore[ChargepointState]:
    return LoggingValueStore(
        ChargepointValueStoreRamdisk(id) if compatibility.is_ramdisk_in_use() else ChargepointValueStoreBroker(id)
    )
