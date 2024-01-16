#!/usr/bin/env python3
import logging

from dataclass_utils import dataclass_from_dict
from modules.common.component_state import BatState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_bat_value_store
from modules.devices.rct.config import RctBatSetup
from modules.devices.rct.rct_lib import RCT

log = logging.getLogger(__name__)


class RctBat:
    def __init__(self, component_config: RctBatSetup) -> None:
        self.component_config = dataclass_from_dict(RctBatSetup, component_config)
        self.store = get_bat_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, rct_client: RCT) -> None:
        my_tab = []
        socx = rct_client.add_by_name(my_tab, 'battery.soc')
        watt1 = rct_client.add_by_name(my_tab, 'g_sync.p_acc_lp')
        watt2 = rct_client.add_by_name(my_tab, 'battery.stored_energy')
        watt3 = rct_client.add_by_name(my_tab, 'battery.used_energy')
        stat1 = rct_client.add_by_name(my_tab, 'battery.bat_status')
        stat2 = rct_client.add_by_name(my_tab, 'battery.status')
        stat3 = rct_client.add_by_name(my_tab, 'battery.status2')

        # read all parameters
        rct_client.read(my_tab)

        bat_state = BatState(
            power=watt1.value * -1,
            soc=socx.value * 100,
            imported=watt2.value,
            exported=watt3.value
        )
        self.store.set(bat_state)
        if (stat1.value + stat2.value + stat3.value) > 0:
            # Werte werden trotz Fehlercode übermittelt.
            log.warning(
                "Alarm Status Speicher ist ungleich 0. Status 1: " + str(stat1.value) + ", Status 2: " +
                str(stat2.value) + ", Status 3: " + str(stat3.value))


component_descriptor = ComponentDescriptor(configuration_factory=RctBatSetup)
