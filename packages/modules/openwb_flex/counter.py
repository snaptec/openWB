#!/usr/bin/env python3
try:
    from ...helpermodules import log
    from ..common import modbus
    from ..common.abstract_component import AbstractComponent, ComponentUpdater
    from ..common.component_state import CounterState
    from ..common.module_error import ComponentInfo
    from ..common.store import get_counter_value_store
    from ..common import simcount
    from ..openwb_flex.versions import kit_version_factory
except (ImportError, ValueError, SystemError):
    from helpermodules import log
    from modules.common import modbus
    from modules.common.abstract_component import AbstractComponent, ComponentUpdater
    from modules.common.component_state import CounterState
    from modules.common.module_error import ComponentInfo
    from modules.common.store import get_counter_value_store
    from modules.common import simcount
    from modules.openwb_flex.versions import kit_version_factory


def get_default_config() -> dict:
    return {
        "name": "EVU-Kit flex",
        "type": "counter",
        "id": None,
        "configuration":
            {
                "version": 2,
                "id": 115
            }
    }


def create_component(device_config: dict, component_config: dict,
                     modbus_client):
    return ComponentUpdater(
        EvuKitFlex(
            device_config["id"],
            component_config,
            modbus_client,
        ), get_counter_value_store(component_config["id"]))


class EvuKitFlex(AbstractComponent[CounterState]):
    def __init__(self, device_id: int, component_config: dict,
                 tcp_client: modbus.ModbusClient) -> None:
        self.__device_id = device_id
        self.component_config = component_config
        factory = kit_version_factory(
            component_config["configuration"]["version"])
        self.__client = factory(component_config["configuration"]["id"],
                                tcp_client)
        self.__tcp_client = tcp_client
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.__simulation = {}

    def get_component_info(self) -> ComponentInfo:
        return ComponentInfo(self.component_config["id"],
                             self.component_config["type"],
                             self.component_config["name"])

    def get_values(self) -> CounterState:
        """ liest die Werte des Moduls aus.
        """
        log.MainLogger().debug("Start kit reading")
        try:
            voltages = self.__client.get_voltage()
            power_per_phase, power_all = self.__client.get_power()
            frequency = self.__client.get_frequency()
            power_factors = self.__client.get_power_factor()

            version = self.component_config["configuration"]["version"]
            if version == 0:
                imported = self.__client.get_imported()
                exported = self.__client.get_exported()
            else:
                currents = list(map(abs, self.__client.get_current()))
        finally:
            self.__tcp_client.close_connection()

        if version == 0:
            currents = [(power_per_phase[i] / voltages[i]) for i in range(3)]
        else:
            if version == 1:
                power_all = sum(power_per_phase)
            topic_str = "openWB/set/system/device/" + \
                str(self.__device_id)+"/component/" + \
                str(self.component_config["id"])+"/"
            imported, exported = self.__sim_count.sim_count(
                power_all,
                topic=topic_str,
                data=self.__simulation,
                prefix="bezug")
        log.MainLogger().debug("EVU-Kit Leistung[W]: " + str(power_all))
        self.__tcp_client.close_connection()
        counter_state = CounterState(
            voltages=voltages,
            currents=currents,
            powers=power_per_phase,
            power_factors=power_factors,
            imported=imported,
            exported=exported,
            power_all=power_all,
            frequency=frequency
        )
        log.MainLogger().debug("Stop kit reading "+str(power_all))
        return counter_state
