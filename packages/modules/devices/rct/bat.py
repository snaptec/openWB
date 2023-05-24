#!/usr/bin/env python3
from dataclass_utils import dataclass_from_dict
from modules.common.component_state import BatState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo, FaultState
from modules.common.store import get_bat_value_store
from modules.devices.rct.config import RctBatSetup
from modules.devices.rct.rct_lib import RCT


class RctBat:
    def __init__(self, component_config: RctBatSetup) -> None:
        self.component_config = dataclass_from_dict(RctBatSetup, component_config)
        self.store = get_bat_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, rct_client: RCT) -> None:
        MyTab = []
        socx = rct_client.add_by_name(MyTab, 'battery.soc')
        watt1 = rct_client.add_by_name(MyTab, 'g_sync.p_acc_lp')
        watt2 = rct_client.add_by_name(MyTab, 'battery.stored_energy')
        watt3 = rct_client.add_by_name(MyTab, 'battery.used_energy')
        stat1 = rct_client.add_by_name(MyTab, 'battery.bat_status')
        stat2 = rct_client.add_by_name(MyTab, 'battery.status')
        stat3 = rct_client.add_by_name(MyTab, 'battery.status2')
        socsoll = rct_client.add_by_name(MyTab, 'battery.soc_target')

        # read all parameters
        rct_client.read(MyTab)

        # postprocess values
        soc = socx.value
        power = int(watt1.value) * -1.0
        imported = int(watt2.value)
        exported = int(watt3.value)
        stat1 = int(stat1.value)
        stat2 = int(stat2.value)
        stat3 = int(stat3.value)
        socsoll = int(socsoll.value * 100.0)

        if (stat1 + stat2 + stat3) > 0:
            raise FaultState.error("Alarm Status Speicher ist ungleich 0.")

        bat_state = BatState(
            power=int(power) * -1,
            soc=soc * 100,
            imported=int(imported),
            exported=int(exported)
        )
        self.store.set(bat_state)


component_descriptor = ComponentDescriptor(configuration_factory=RctBatSetup)
