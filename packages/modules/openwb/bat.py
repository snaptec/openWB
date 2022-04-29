#!/usr/bin/env python3

from typing import Tuple
from modules.common import modbus
from modules.common.fault_state import FaultState
from modules.openwb_flex.bat import BatKitFlex


def get_default_config() -> dict:
    return {
        "name": "Speicher-Kit",
        "type": "bat",
        "id": 0,
        "configuration": {
            "version": 2
        }
    }


def create_preconfigured_component(device_id: int,
                                   component_config: dict,
                                   tcp_client: modbus.ModbusClient) -> Tuple[modbus.ModbusClient, BatKitFlex]:
    version = component_config["configuration"]["version"]
    if version == 0:
        id = 1
        ip_address = '192.168.193.19'
    elif version == 1:
        id = 9
        ip_address = '192.168.193.19'
    elif version == 2:
        id = 117
        ip_address = '192.168.193.15'
    else:
        raise FaultState.error("Version " + str(version) + " unbekannt.")
    component_config["configuration"]["id"] = id

    if tcp_client:
        if tcp_client.address != ip_address or tcp_client.port != 8899:
            raise FaultState.error(
                "Das Device kann nur auf eine IP-Adresse zugreifen. Für ein weiteres Kit bitte ein neues Device anlegen.")
    else:
        tcp_client = modbus.ModbusClient(ip_address, 8899)

    return tcp_client, BatKitFlex(device_id, component_config, tcp_client)
