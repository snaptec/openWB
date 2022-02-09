from typing import Dict, Union, Optional, List

from helpermodules import log
from helpermodules.cli import run_using_positional_cli_args
from modules.common import modbus
from modules.common.abstract_device import AbstractDevice
from modules.common.component_context import SingleComponentUpdateContext
from modules.openwb_flex import bat
from modules.openwb_flex import counter
from modules.openwb_flex import inverter


def get_default_config() -> dict:
    return {
        "name": "OpenWB-Kit flex",
        "type": "openwb_flex",
        "id": 0,
        "configuration": {
            "ip_address": "192.168.193.15",
            "port": 8899
        }
    }


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        "bat": bat.BatKitFlex,
        "counter": counter.EvuKitFlex,
        "inverter": inverter.PvKitFlex
    }

    def __init__(self, device_config: dict) -> None:
        self._components = {}  # type: Dict[str, Union[counter.EvuKitFlex, inverter.PvKitFlex]]
        try:
            self.device_config = device_config
            ip_address = device_config["configuration"]["ip_address"]
            port = device_config["configuration"]["port"]
            self.client = modbus.ModbusClient(ip_address, port)
        except Exception:
            log.MainLogger().exception("Fehler im Modul " + device_config["name"])

    def add_component(self, component_config: dict) -> None:
        component_type = component_config["type"]
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self._components["component"+str(component_config["id"])] = (self.COMPONENT_TYPE_TO_CLASS[component_type](
                self.device_config["id"], component_config, self.client))
        else:
            raise Exception("illegal component type " + component_type +
                            ". Allowed values: " +
                            ','.join(self.COMPONENT_TYPE_TO_CLASS.keys()))

    def update(self) -> None:
        log.MainLogger().debug("Start device reading " + str(self._components))
        if self._components:
            for component in self._components:
                # Auch wenn bei einer Komponente ein Fehler auftritt, sollen alle anderen noch ausgelesen werden.
                with SingleComponentUpdateContext(self._components[component].component_info):
                    self._components[component].update()
        else:
            log.MainLogger().warning(
                self.device_config["name"] +
                ": Es konnten keine Werte gelesen werden, da noch keine Komponenten konfiguriert wurden."
            )


def read_legacy(component_type: str, version: int, ip_address: str, port: int, id: int, num: Optional[int] = None):
    """ Ausführung des Moduls als Python-Skript
    """
    COMPONENT_TYPE_TO_MODULE = {
        "bat": bat,
        "counter": counter,
        "inverter": inverter
    }
    log.MainLogger().debug('Start reading flex')
    device_config = get_default_config()
    device_config["configuration"]["ip_address"] = ip_address
    device_config["configuration"]["port"] = port
    dev = Device(device_config)
    if component_type in COMPONENT_TYPE_TO_MODULE:
        component_config = COMPONENT_TYPE_TO_MODULE[
            component_type].get_default_config()
    else:
        raise Exception("illegal component type " + component_type +
                        ". Allowed values: " +
                        ','.join(COMPONENT_TYPE_TO_MODULE.keys()))

    component_config["id"] = num
    component_config["configuration"]["version"] = version
    component_config["configuration"]["id"] = id
    dev.add_component(component_config)

    log.MainLogger().debug('openWB flex Version: ' + str(version))
    log.MainLogger().debug('openWB flex-Kit IP-Adresse: ' + str(ip_address))
    log.MainLogger().debug('openWB flex-Kit Port: ' + str(port))
    log.MainLogger().debug('openWB flex-Kit ID: ' + str(id))

    dev.update()


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)
