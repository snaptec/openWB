#!/usr/bin/env python3

from helpermodules import log
from modules.common import modbus
from modules.common import simcount
from modules.common.component_state import CounterState
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_counter_value_store
from modules.openwb_flex.versions import kit_counter_inverter_version_factory


def get_default_config() -> dict:
    return {
        "name": "EVU-Kit flex",
        "type": "counter",
        "id": None,
        "configuration": {
            "version": 2,
            "id": 115
        }
    }


class EvuKitFlex:
    def __init__(self, device_id: int, component_config: dict,
                 tcp_client: modbus.ModbusClient) -> None:
        self.__device_id = device_id
        self.component_config = component_config
        factory = kit_counter_inverter_version_factory(
            component_config["configuration"]["version"])
        self.__client = factory(component_config["configuration"]["id"],
                                tcp_client)
        self.__tcp_client = tcp_client
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.simulation = {}
        self.__store = get_counter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self):
        log.MainLogger().debug("Start kit reading")
        # TCP-Verbindung schließen möglichst bevor etwas anderes gemacht wird, um im Fehlerfall zu verhindern,
        # dass offene Verbindungen den Modbus-Adapter blockieren.
        try:
            voltages = self.__client.get_voltages()
            powers, power = self.__client.get_power()
            frequency = self.__client.get_frequency()
            power_factors = self.__client.get_power_factors()

            version = self.component_config["configuration"]["version"]
            if version == 0:
                imported = self.__client.get_imported()
                exported = self.__client.get_exported()
            else:
                currents = list(map(abs, self.__client.get_currents()))
        finally:
            self.__tcp_client.close_connection()
        version = self.component_config["configuration"]["version"]
        if version == 0:
            currents = [powers[i] / voltages[i] for i in range(3)]
        else:
            if version == 1:
                power = sum(powers)
            topic_str = "openWB/set/system/device/{}/component/{}/".format(
                self.__device_id, self.component_config["id"]
            )
            imported, exported = self.__sim_count.sim_count(
                power,
                topic=topic_str,
                data=self.simulation,
                prefix="bezug"
            )
        counter_state = CounterState(
            voltages=voltages,
            currents=currents,
            powers=powers,
            power_factors=power_factors,
            imported=imported,
            exported=exported,
            power=power,
            frequency=frequency
        )
        log.MainLogger().debug("EVU-Kit Leistung[W]: " + str(counter_state.power))
        self.__store.set(counter_state)
