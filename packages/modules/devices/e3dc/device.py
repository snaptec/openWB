#!/usr/bin/env python3
import logging
from typing import List, Union, Iterable

from helpermodules.cli import run_using_positional_cli_args
from modules.common.abstract_device import DeviceDescriptor
from modules.common.configurable_device import ConfigurableDevice, ComponentFactoryByType, SingleComponentUpdateContext
from modules.common import modbus
from modules.devices.e3dc.bat import E3dcBat, read_bat
from modules.devices.e3dc.inverter import E3dcInverter, read_inverter
from modules.devices.e3dc.external_inverter import E3dcExternalInverter, read_external_inverter
from modules.devices.e3dc.counter import E3dcCounter
from modules.devices.e3dc.config import E3dc, E3dcConfiguration
from modules.devices.e3dc.config import E3dcBatSetup
from modules.devices.e3dc.config import E3dcCounterSetup, E3dcCounterConfiguration
from modules.devices.e3dc.config import E3dcInverterSetup, E3dcExternalInverterSetup
from modules.common.store.ramdisk import files
from modules.common.simcount import sim_count
from modules.common.store import get_inverter_value_store, get_bat_value_store
from modules.common.component_state import InverterState, BatState


log = logging.getLogger(__name__)


def create_device(device_config: E3dc) -> ConfigurableDevice:
    def create_bat_component(component_config: E3dcBatSetup) -> E3dcBat:
        return E3dcBat(device_config.id,
                       component_config)

    def create_counter_component(component_config: E3dcCounterSetup) -> E3dcCounter:
        return E3dcCounter(device_config.id,
                           component_config)

    def create_inverter_component(component_config: E3dcInverterSetup) -> E3dcInverter:
        return E3dcInverter(device_config.id,
                            component_config)

    def create_external_inverter_component(component_config: E3dcExternalInverterSetup) -> E3dcExternalInverter:
        return E3dcExternalInverter(device_config.id,
                                    component_config)

    def update_components(components: Iterable[Union[E3dcBat, E3dcCounter, E3dcInverter,
                                                     E3dcExternalInverter]]) -> None:
        with modbus.ModbusTcpClient_(device_config.configuration.address, 502) as client:
            log.debug('reading: %s', device_config.configuration.address)
            for component in components:
                with SingleComponentUpdateContext(component.component_info):
                    component.update(client)

    return ConfigurableDevice(
        device_config=device_config,
        component_factory=ComponentFactoryByType(
            bat=create_bat_component,
            counter=create_counter_component,
            inverter=create_inverter_component,
            external_inverter=create_external_inverter_component
        ),
        component_updater=update_components
    )


def run_device_legacy(device_config: E3dc,
                      component_config: Union[E3dcBatSetup, E3dcCounterSetup, E3dcInverterSetup]) -> None:
    device = create_device(device_config)
    device.add_component(component_config)
    # do not log complete config objects as these will contain german umlauts and logging will fail in Version 1.9
    log.debug("E3dc Configuration: %s, Component Configuration: %s",
              device_config.configuration, component_config.configuration)
    device.update()


def create_legacy_device_config(address: str,
                                num: int) -> E3dc:
    device_config = E3dc(configuration=E3dcConfiguration(address=address),
                         id=num)
    log.debug("Config: %s", device_config)
    return device_config


def read_legacy_counter(address1: str, num: int) -> None:
    component_config = E3dcCounterSetup(configuration=E3dcCounterConfiguration())
    component_config.id = num
    run_device_legacy(create_legacy_device_config(address1,
                                                  num), component_config)


def read_legacy_bat(address1: str,
                    address2: str, read_ext_input: int,
                    pv_module: str,
                    num: int) -> None:
    # für Openwb Version 1.9 können mit der bisherigen Parametrisierung zwei IP-Adressen ausgelesen werden
    # ebenso wird bei Speicheraufruf Speicher und PV ausgelesen
    # in openwb v2.0 geht nur noch eine IP Adresse und die Pv muss separat ausgelesen werden
    addresses = [address for address in [address1, address2] if address != "none"]
    read_ext = (read_ext_input == 1)
    log.debug('e3dc IP-Adresse1: %s', address1)
    log.debug('e3dc IP-Adresse2: %s', address2)
    log.debug('e3dc read_ext: %s', read_ext)
    log.debug('e3dc pv_module: %s', pv_module)
    log.debug('e3dc id: %d', num)
    soc = 0   # type: Union[int, float]
    power = 0
    pv_external = 0
    pv = 0
    pv_other = pv_module != "none"
    for address in addresses:
        log.debug("Ip: %s, read_external %s pv_other %s", address, read_ext, pv_other)
        with modbus.ModbusTcpClient_(address, port=502) as client:
            soc_tmp, power_tmp = read_bat(client)
            soc += soc_tmp
            power += power_tmp
            pv_tmp = read_inverter(client)
            if read_ext:
                pv_external_tmp = read_external_inverter(client)
            else:
                pv_external_tmp = 0
            pv += pv_tmp
            pv_external += pv_external_tmp
    soc /= len(addresses)
    log.debug("Soc %d power %d pv %d pv_external %d",
              soc, power, pv, pv_external)
    counter_import, counter_export = sim_count(power, prefix="speicher")
    get_bat_value_store(1).set(BatState(power=power, soc=soc, imported=counter_import, exported=counter_export))
    # pv_other sagt aus, ob WR definiert ist, und dessen PV Leistung auch gilt
    # wenn 0 gilt nur PV und pv_external aus e3dc
    pv_total = pv + pv_external
    # Wenn wr1 nicht definiert ist, gilt nur die PV Leistung die hier im Modul ermittelt wurde
    # als gesamte PV Leistung für wr1
    # Wenn wr1 definiert ist, gilt die bestehende PV Leistung aus Wr1 und das was hier im Modul ermittelt wurde
    # als gesamte PV Leistung für wr1
    if pv_other:
        pv_total = pv_total + files.pv[0].power.read()
    log.debug("wr update pv_other %s pv_total %d", pv_other, pv_total)
    _, exported_pv = sim_count(pv_total, prefix="pv")
    get_inverter_value_store(num).set(InverterState(exported=exported_pv, power=pv_total))


def main(argv: List[str]) -> None:
    run_using_positional_cli_args(
        {"bat": read_legacy_bat, "counter": read_legacy_counter}, argv
    )


device_descriptor = DeviceDescriptor(configuration_factory=E3dc)
