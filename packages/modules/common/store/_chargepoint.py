from modules.common.component_state import ChargepointState
from modules.common.store import ValueStore
from modules.common.store._broker import pub_to_broker


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
        pub_to_broker("openWB/set/chargepoint/" + str(self.num) + "/get/phases_in_use", state.phases_in_use, 2)
        pub_to_broker("openWB/set/chargepoint/" + str(self.num) + "/get/charge_state", state.charge_state, 2)
        pub_to_broker("openWB/set/chargepoint/" + str(self.num) + "/get/plug_state", state.plug_state, 2)
        pub_to_broker("openWB/set/chargepoint/" + str(self.num) + "/get/read_tag", state.read_tag)


def get_chargepoint_value_store(id: int) -> ValueStore[ChargepointState]:
    return ChargepointValueStoreBroker(id)
