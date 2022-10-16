#!/usr/bin/env python3
import logging
from typing import Dict, List, Union, Optional

from dataclass_utils import dataclass_from_dict
from helpermodules.cli import run_using_positional_cli_args
from modules.common.abstract_device import AbstractDevice, DeviceDescriptor
from modules.common.component_context import SingleComponentUpdateContext
from modules.e3dc import bat
from modules.e3dc import counter
from modules.e3dc.config import E3dc, E3dcBatSetup, E3dcConfiguration
from modules.e3dc.config import E3dcCounterSetup

log = logging.getLogger(__name__)


e3dc_component_classes = Union[bat.E3dcBat, counter.E3dcCounter]


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        "bat": bat.E3dcBat,
        "counter": counter.E3dcCounter}

    def __init__(self, device_config: Union[Dict, E3dc]) -> None:
        self.components = {}  # type: Dict[str, e3dc_component_classes]
        try:
            self.device_config = dataclass_from_dict(E3dc, device_config)
        except Exception:
            log.exception("Fehler im Modul "+self.device_config.name)

    def add_component(self,
                      component_config: Union[Dict,
                                              E3dcBatSetup,
                                              E3dcCounterSetup]) -> None:
        if isinstance(component_config, Dict):
            component_type = component_config["type"]
        else:
            component_type = component_config.type
        component_config = dataclass_from_dict(COMPONENT_TYPE_TO_MODULE[
            component_type].component_descriptor.configuration_factory,
            component_config)
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self.components["component"+str(component_config.id)] = (self.COMPONENT_TYPE_TO_CLASS[component_type](
                self.device_config.id,
                self.device_config.configuration.ip_address1,
                self.device_config.configuration.ip_address2,
                self.device_config.configuration.read_ext,
                self.device_config.configuration.pvmodul,
                component_config))
        else:
            raise Exception(
                "illegal component type " + component_type +
                ". Allowed values: " +
                ','.join(self.COMPONENT_TYPE_TO_CLASS.keys())
            )

    def update(self) -> None:
        log.debug("Start device reading " + str(self.components))
        if self.components:
            for component in self.components:
                # Auch wenn bei einer Komponente ein Fehler auftritt,
                # sollen alle anderen noch ausgelesen werden.
                with SingleComponentUpdateContext(self.components[component].component_info):
                    self.components[component].update()
        else:
            log.warning(
                self.device_config.name +
                ": Es konnten keine Werte gelesen werden," +
                " da noch keine Komponenten konfiguriert wurden."
            )


COMPONENT_TYPE_TO_MODULE = {
    "bat": bat,
    "counter": counter
}


def read_legacy(component_type: str, address1: str,
                address2: str, read_ext: int,
                pvmodul: str,
                num: Optional[int]) -> None:
    device_config = E3dc(configuration=E3dcConfiguration(ip_address1=address1,
                                                         ip_address2=address2,
                                                         read_ext=read_ext,
                                                         pvmodul=pvmodul))
    dev = Device(device_config)
    if component_type in COMPONENT_TYPE_TO_MODULE:
        component_config = COMPONENT_TYPE_TO_MODULE[component_type].component_descriptor.configuration_factory()
    else:
        raise Exception(
            "illegal component type " + component_type + ". Allowed values: " +
            ','.join(COMPONENT_TYPE_TO_MODULE.keys())
        )
    dev.add_component(component_config)
    # none bei counter und bat
    # muss aber bei bat mitkommen da sonst ein optionaler pv update fehlschlägt
    component_config.id = num
    log.debug('e3dc IP-Adresse1: ' + address1)
    log.debug('e3dc IP-Adresse2: ' + address2)
    log.debug('e3dc read_ext: ' + str(read_ext))
    log.debug('e3dc pvmodul: ' + pvmodul)
    log.debug('e3dc id: ' + str(component_config.id))

    dev.update()
#    dev.client.close_connection()


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)


device_descriptor = DeviceDescriptor(configuration_factory=E3dc)
