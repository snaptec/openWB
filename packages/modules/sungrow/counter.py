#!/usr/bin/env python3
from helpermodules import log
from modules.common import modbus
from modules.common import simcount
from modules.common.component_state import CounterState
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType, Endian
from modules.common.store import get_counter_value_store


def get_default_config() -> dict:
    return {
        "name": "Sungrow Zähler",
        "id": 0,
        "type": "counter",
        "configuration": {
            "version": 1
        }
    }


class SungrowCounter:
    def __init__(self, device_id: int, component_config: dict, tcp_client: modbus.ModbusClient) -> None:
        self.__device_id = device_id
        self.component_config = component_config
        self.__tcp_client = tcp_client
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.__simulation = {}
        self.__store = get_counter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self):
        log.MainLogger().debug("Komponente "+self.component_config["name"]+" auslesen.")
        unit = 1
        with self.__tcp_client:
            if self.component_config["configuration"]["version"] == 1:
                power = self.__tcp_client.read_input_registers(5082, ModbusDataType.INT_32,
                                                               wordorder=Endian.Little, unit=unit)
                frequency = self.__tcp_client.read_input_registers(5035, ModbusDataType.UINT_16, unit=unit) / 10
                voltages = self.__tcp_client.read_input_registers(5018, [ModbusDataType.UINT_16] * 3,
                                                                  wordorder=Endian.Little, unit=unit)
                voltages = [voltage / 10 for voltage in voltages]
                # no valid data for powers per phase
                # powers = self.__tcp_client.read_input_registers(5084, [ModbusDataType.UINT_16] * 3,
                #                                                 wordorder=Endian.Little, unit=unit)
                # powers = [power / 10 for power in powers]
                # log.MainLogger().info("power: " + str(power) + " powers?: " + str(powers))
            else:
                power = self.__tcp_client.read_input_registers(13009, ModbusDataType.INT_32,
                                                               wordorder=Endian.Little, unit=unit) * -1
                frequency = self.__tcp_client.read_input_registers(5035, ModbusDataType.UINT_16, unit=unit) / 10
                voltages = self.__tcp_client.read_input_registers(5018, [ModbusDataType.UINT_16] * 3,
                                                                  wordorder=Endian.Little, unit=unit)
                voltages = [voltage / 10 for voltage in voltages]
                # no valid data for powers per phase
                # powers = self.__tcp_client.read_input_registers(5084, [ModbusDataType.INT_16] * 3,
                #                                                 wordorder=Endian.Little, unit=unit)
                # powers = [power / 10 for power in powers]
                # log.MainLogger().info("power: " + str(power) + " powers?: " + str(powers))

        topic_str = "openWB/set/system/device/{}/component/{}/".format(self.__device_id, self.component_config["id"])
        imported, exported = self.__sim_count.sim_count(
            power,
            topic=topic_str,
            data=self.__simulation,
            prefix="bezug"
        )

        counter_state = CounterState(
            imported=imported,
            exported=exported,
            power=power,
            voltages=voltages,
            frequency=frequency
        )
        log.MainLogger().debug("Sungrow Leistung[W]: " + str(counter_state.power))
        self.__store.set(counter_state)
