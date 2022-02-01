#!/usr/bin/env python3
import socket
import struct
from typing import Dict, Union, Optional, List

from helpermodules import log
from helpermodules.cli import run_using_positional_cli_args
from modules.common.fault_state import FaultState
from modules.sma import counter
from modules.sma import inverter
from modules.common.abstract_device import AbstractDevice
from modules.common.component_context import MultiComponentUpdateContext, SingleComponentUpdateContext
from modules.sma.speedwiredecoder import decode_speedwire


def get_default_config() -> dict:
    return {
        "name": "SMA Smarthome Manager",
        "type": "sma",
        "id": 0
    }


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        "counter": counter.SmaCounter,
        "inverter": inverter.SmaInverter
    }

    def __init__(self, device_config: dict) -> None:
        self._components = {}  # type: Dict[str, Union[counter.SmaCounter, inverter.SmaInverter]]
        try:
            self.device_config = device_config
        except Exception:
            log.MainLogger().exception("Fehler im Modul "+device_config["name"])

    def add_component(self, component_config: dict) -> None:
        component_type = component_config["type"]
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self._components["component"+str(component_config["id"])] = (self.COMPONENT_TYPE_TO_CLASS[component_type](
                component_config))
        else:
            raise Exception(
                "illegal component type " + component_type + ". Allowed values: " +
                ','.join(self.COMPONENT_TYPE_TO_CLASS.keys())
            )

    def update(self) -> None:
        with MultiComponentUpdateContext(self._components):
            log.MainLogger().debug("Beginning update")
            ipbind = '0.0.0.0'
            MCAST_GRP = '239.12.255.254'
            MCAST_PORT = 9522
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.bind(('', MCAST_PORT))
                try:
                    mreq = struct.pack("4s4s", socket.inet_aton(MCAST_GRP), socket.inet_aton(ipbind))
                    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
                except BaseException:
                    raise FaultState.error('could not connect to multicast group or bind to given interface')
                # processing received messages
                while not self.__process_datagram(sock.recv(608)):
                    pass
            log.MainLogger().debug("Update completed successfully")

    def __process_datagram(self, datagram: bytes) -> bool:
        # Paket ignorieren, wenn es nicht dem SMA-"energy meter protocol" mit protocol id = 0x6069 entspricht
        if datagram[16:18] != b'\x60\x69':
            return False
        sma_data = decode_speedwire(datagram)
        log.MainLogger().debug("SMA-Datagramm: "+str(sma_data))
        if self._components:
            for component in self._components:
                # Auch wenn bei einer Komponente ein Fehler auftritt, sollen alle anderen noch ausgelesen werden.
                with SingleComponentUpdateContext(self._components[component].component_info):
                    sma_serials = self._components[component].component_config["configuration"]["serials"]
                    if sma_serials is None or sma_serials == 'none' or str(sma_data['serial']) == sma_serials:
                        self._components[component].update(sma_data)
        else:
            log.MainLogger().warning(
                self.device_config["name"] +
                ": Es konnten keine Werte gelesen werden, da noch keine Komponenten konfiguriert wurden."
            )
        return True


def read_legacy(component_type: str, serials: Optional[str] = None, num: Optional[int] = None) -> None:
    COMPONENT_TYPE_TO_MODULE = {
        "counter": counter,
        "inverter": inverter
    }
    device_config = get_default_config()
    dev = Device(device_config)
    if component_type in COMPONENT_TYPE_TO_MODULE:
        component_config = COMPONENT_TYPE_TO_MODULE[component_type].get_default_config()
    else:
        raise Exception(
            "illegal component type " + component_type + ". Allowed values: " +
            ','.join(COMPONENT_TYPE_TO_MODULE.keys())
        )
    component_config["id"] = num
    component_config["configuration"]["serials"] = serials
    dev.add_component(component_config)

    log.MainLogger().debug('SMA serials: ' + str(serials))

    dev.update()


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)
