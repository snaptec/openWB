#!/usr/bin/env python3

from typing import Tuple
from modules.common import modbus
from modules.common.fault_state import FaultState
from modules.openwb_flex.counter import EvuKitFlex


def get_default_config() -> dict:
    return {
        "name": "EVU-Kit",
        "type": "counter",
        "id": 0,
        "configuration": {
            "version": 2
        }
    }


def create_preconfigured_component(device_id: int,
                                   component_config: dict,
                                   tcp_client: modbus.ModbusClient) -> Tuple[modbus.ModbusClient, EvuKitFlex]:
    if tcp_client:
        if tcp_client.address != "192.168.193.15" or tcp_client.port != 8899:
            raise FaultState.error(
                "Das Device kann nur auf eine IP-Adresse zugreifen. Für ein weiteres Kit bitte ein neues Device anlegen.")
    else:
        tcp_client = modbus.ModbusClient("192.168.193.15", 8899)

    version = component_config["configuration"]["version"]
    if version == 0:
        id = 5
    elif version == 1:
        id = 2
    elif version == 2:
        id = 115
    else:
        raise FaultState.error("Version " + str(version) + " unbekannt.")
    component_config["configuration"]["id"] = id

    return tcp_client, EvuKitFlex(device_id, component_config, tcp_client)
