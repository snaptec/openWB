#!/usr/bin/env python3
try:
    from ...helpermodules import log
    from ..common import modbus
    from ..common.abstract_component import AbstractCounter
    from ..common.component_state import CounterState
except (ImportError, ValueError, SystemError):
    from helpermodules import log
    from modules.common import modbus
    from modules.common.abstract_component import AbstractCounter
    from modules.common.component_state import CounterState


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


class EvuKitFlex(AbstractCounter):
    def __init__(self, device_id: int, component_config: dict, tcp_client: modbus.ModbusClient) -> None:
        try:
            client = self.kit_version_factory(
                component_config["configuration"]["version"], component_config["configuration"]["id"], tcp_client)
            super().__init__(device_id, component_config, client)
            self.tcp_client = tcp_client
        except Exception as e:
            self.process_error(e)

    def get_values(self) -> CounterState:
        """ liest die Werte des Moduls aus.
        """
        log.MainLogger().debug("Start kit reading")
        try:
            voltages = self.client.get_voltage()
            power_per_phase, power_all = self.client.get_power()
            frequency = self.client.get_frequency()
            power_factors = self.client.get_power_factor()

            version = self.data["config"]["configuration"]["version"]
            if version == 0:
                imported = self.client.get_imported()
                exported = self.client.get_exported()
            else:
                currents = map(abs, self.client.get_current())
        finally:
            self.tcp_client.close_connection()

        if version == 0:
            currents = [(power_per_phase[i]/voltages[i]) for i in range(3)]
        else:
            if version == 1:
                power_all = sum(power_per_phase)
            topic_str = "openWB/set/system/device/" + \
                str(self.device_id)+"/component/" + \
                str(self.data["config"]["id"])+"/"
            imported, exported = self.sim_count.sim_count(
                power_all, topic=topic_str, data=self.data["simulation"], prefix="bezug")

        log.MainLogger().debug("EVU-Kit Leistung[W]: "+str(power_all))
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
