#!/usr/bin/env python3

try:
    from ...helpermodules import log
    from ..common import modbus
    from ..common.abstract_component import AbstractInverter
    from ..common.component_state import InverterState
    from ..common.module_error import ModuleError
except (ImportError, ValueError):
    from helpermodules import log
    from modules.common import modbus
    from modules.common.abstract_component import AbstractInverter
    from modules.common.component_state import InverterState
    from modules.common.module_error import ModuleError


def get_default_config() -> dict:
    return {
        "name": "Alpha ESS Wechselrichter",
        "id": 0,
        "type": "inverter",
        "configuration":
        {
            "version": 1
        }
    }


class AlphaEssInverter(AbstractInverter):
    def __init__(self, device_id: int, component_config: dict, tcp_client: modbus.ModbusClient) -> None:
        try:
            super().__init__(device_id, component_config, tcp_client)
        except Exception as e:
            self.process_error(e)

    def get_values(self) -> InverterState:
        log.MainLogger().debug(
            "Komponente "+self.data["config"]["name"]+" auslesen.")
        reg_p = self.__version_factory(
            self.data["config"]["configuration"]["version"])
        power = self.__get_power(85, reg_p)

        topic_str = "openWB/set/system/device/" + \
            str(self.device_id)+"/component/" + \
            str(self.data["config"]["id"])+"/"
        _, counter = self.sim_count.sim_count(
            power, topic=topic_str, data=self.data["simulation"], prefix="pv")
        inverter_state = InverterState(
            power=power,
            counter=counter,
            currents=[0, 0, 0]
        )
        return inverter_state

    def __version_factory(self, version: int) -> int:
        return 0x0012 if version == 0 else 0x00A1

    def __get_power(self, unit: int, reg_p: int) -> int:
        try:
            powers = [
                self.client.read_holding_registers(address, modbus.ModbusDataType.INT_32, unit=unit)
                for address in [reg_p, 0x041F, 0x0423, 0x0427]
            ]
            powers[0] = abs(powers[0])
            power = sum(powers) * -1
            log.MainLogger().debug("Alpha Ess Leistung: "+str(power)+", WR-Register: " + str(powers))
            return power
        except ModuleError:
            raise
        except Exception as e:
            self.process_error(e)
