#!/usr/bin/env python3
from dataclass_utils import dataclass_from_dict
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_inverter_value_store
from modules.devices.rct.config import RctInverterSetup
from modules.devices.rct.rct_lib import RCT


class RctInverter:
    def __init__(self, component_config: RctInverterSetup) -> None:
        self.component_config = dataclass_from_dict(RctInverterSetup, component_config)
        self.store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, rct_client: RCT) -> None:
        MyTab = []
        power1 = rct_client.add_by_name(MyTab, 'dc_conv.dc_conv_struct[0].p_dc')
        power2 = rct_client.add_by_name(MyTab, 'dc_conv.dc_conv_struct[1].p_dc')
        power3 = rct_client.add_by_name(MyTab, 'io_board.s0_external_power')
        # pLimit = rct_client.add_by_name(MyTab, 'p_rec_lim[2]')   # max. AC power according to RCT Power
        pv1total = rct_client.add_by_name(MyTab, 'energy.e_dc_total[0]')
        pv2total = rct_client.add_by_name(MyTab, 'energy.e_dc_total[1]')
        pv3total = rct_client.add_by_name(MyTab, 'energy.e_ext_total')

        # read all parameters
        rct_client.read(MyTab)

        inverter_state = InverterState(
            power=(power1.value + power2.value + power3.value) * -1,
            exported=(pv1total.value + pv2total.value + pv3total.value),
        )
        self.store.set(inverter_state)


component_descriptor = ComponentDescriptor(configuration_factory=RctInverterSetup)
