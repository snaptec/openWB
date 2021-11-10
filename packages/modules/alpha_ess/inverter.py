#!/usr/bin/env python3
import time

try:
    from ...helpermodules import log
    from ..common import modbus
    from ..common.abstract_component import AbstractInverter
    from ..common.component_state import InverterState
    from ..common.module_error import ModuleError
except:
    from pathlib import Path
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
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
        try:
            if version == 0:
                return 0x0012
            else:
                return 0x00A1
        except ModuleError as e:
            raise
        except Exception as e:
            self.process_error(e)

    def __get_power(self, unit: int, reg_p: int) -> int:
        try:
            p_reg = self.client.read_holding_registers(
                reg_p, modbus.ModbusDataType.INT_32, unit=unit)
            if (p_reg < 0):
                p_reg = p_reg * -1
            time.sleep(0.1)
            p2_reg = self.client.read_holding_registers(
                0x041F, modbus.ModbusDataType.INT_32, unit=unit)
            p3_reg = self.client.read_holding_registers(
                0x0423, modbus.ModbusDataType.INT_32, unit=unit)
            p4_reg = self.client.read_holding_registers(
                0x0427, modbus.ModbusDataType.INT_32, unit=unit)
            power = (p_reg + p2_reg + p3_reg + p4_reg) * -1
            log.MainLogger().debug("Alpha Ess Leistung: "+str(power)+", WR-Register: R1" +
                                   str(p_reg)+" R2 "+str(p2_reg)+" R3 "+str(p3_reg)+" R4 "+str(p4_reg))
            return power
        except ModuleError as e:
            raise
        except Exception as e:
            self.process_error(e)
