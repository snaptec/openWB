#!/usr/bin/env python3
try:
    from ...helpermodules import log
    from ..common import modbus
    from ..common.component_state import CounterState
    from ..common.module_error import ComponentInfo
    from ..common.store import get_counter_value_store
    from ..common import simcount
    from ..openwb_flex.versions import kit_version_factory
except (ImportError, ValueError, SystemError):
    from helpermodules import log
    from modules.common import modbus
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


class EvuKitFlex:
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
        self.__store = get_counter_value_store(component_config["id"])

    def get_component_info(self) -> ComponentInfo:
        return ComponentInfo(self.component_config["id"],
                             self.component_config["type"],
                             self.component_config["name"])

    def update(self):
        log.MainLogger().debug("Start kit reading")
        # TCP-Verbindung schließen möglichst bevor etwas anderes gemacht wird, um im Fehlerfall zu verhindern,
        # dass ungeschlossene Verbindungen den Modbus-Adapter blockieren.
        with self.__tcp_client:
            counter_state = self.try_get_modbus_state()
        counter_state = self.calculate_missing_values(counter_state)
        log.MainLogger().debug("EVU-Kit Leistung[W]: " + str(counter_state.power_all))
        self.__store.set(counter_state)

    def try_get_modbus_state(self) -> CounterState:
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

        return CounterState(
            voltages=voltages,
            currents=currents,
            powers=power_per_phase,
            power_factors=power_factors,
            imported=imported,
            exported=exported,
            power_all=power_all,
            frequency=frequency
        )

    def calculate_missing_values(self, counter_state: CounterState) -> CounterState:
        version = self.component_config["configuration"]["version"]
        if version == 0:
            counter_state.currents = [counter_state.power_per_phase[i] / counter_state.voltages[i] for i in range(3)]
        else:
            if version == 1:
                counter_state.power_all = sum(counter_state.power_per_phase)
            topic_str = "openWB/set/system/device/{}/component/{}/".format(
                self.__device_id, self.component_config["id"]
            )
            counter_state.exported, counter_state.imported = self.__sim_count.sim_count(
                counter_state.power_all,
                topic=topic_str,
                data=self.__simulation,
                prefix="bezug"
            )
        return counter_state
