#!/usr/bin/env python3

from modules.common.component_state import InverterState
from modules.common.store import get_inverter_value_store
from modules.sma_shm.utils import SpeedwireComponent


def get_default_config() -> dict:
    return {
        "name": "SMA Home Manager Wechselrichter",
        "id": 0,
        "type": "inverter",
        "configuration": {
            "serials": None
        }
    }


def parse_datagram(sma_data: dict):
    return InverterState(
        power=-int(sma_data['psupply']),
        exported=sma_data['psupplycounter'] * 1000
    )


def create_component(component_config: dict):
    return SpeedwireComponent(get_inverter_value_store, parse_datagram, component_config)
