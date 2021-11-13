#!/usr/bin/env python3


try:
    from ...helpermodules import log
    from ..common import modbus
    from ..common.abstract_component import AbstractInverter
    from ..common.component_state import InverterState
except (ImportError, ValueError):
    from helpermodules import log
    from modules.common import modbus
    from modules.common.abstract_component import AbstractInverter
    from modules.common.component_state import InverterState


def get_default_config() -> dict:
    return {
        "name": "PV-Kit flex",
        "type": "inverter",
        "id": None,
        "configuration":
            {
                "version": 2,
                "id": 116
            }
    }


class PvKitFlex(AbstractInverter):
    def __init__(self, device_id: int, component_config: dict, tcp_client: modbus.ModbusClient) -> None:
        try:
            client = self.kit_version_factory(
                component_config["configuration"]["version"], component_config["configuration"]["id"], tcp_client
            )
            super().__init__(device_id, component_config, client)
            self.tcp_client = tcp_client
        except Exception as e:
            self.process_error(e)

    def get_values(self) -> InverterState:
        """ liest die Werte des Moduls aus.
        """
        counter = self.client.get_counter()
        power_per_phase, power_all = self.client.get_power()

        version = self.data["config"]["configuration"]["version"]
        if version == 1:
            power_all = sum(power_per_phase)
        if power_all > 10:
            power_all = power_all*-1
        currents = self.client.get_current()

        log.MainLogger().debug("PV-Kit Leistung[W]: "+str(power_all))
        self.tcp_client.close_connection()
        inverter_state = InverterState(
            power=power_all,
            counter=counter,
            currents=currents
        )
        return inverter_state
