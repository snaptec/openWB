#!/usr/bin/env python3
"""Modul für einfache Modbusoperationen.

Das Modul baut eine Modbus-TCP-Verbindung auf. Es gibt verschiedene Funktionen, um die gelesenen Register zu
formatieren.
"""
from enum import Enum
from typing import Callable, Iterable, Union

import pymodbus
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

try:
    from ...helpermodules import log
    from ..common.module_error import ModuleError, ModuleErrorLevel
except (ImportError, ValueError):
    from helpermodules import log
    from modules.common.module_error import ModuleError, ModuleErrorLevel


class ModbusDataType(Enum):
    UINT_8 = 8, "decode_8bit_uint"
    UINT_16 = 16, "decode_16bit_uint"
    UINT_32 = 32, "decode_32bit_uint"
    UINT_64 = 64, "decode_64bit_uint"
    INT_8 = 8, "decode_8bit_int"
    INT_16 = 16, "decode_16bit_int"
    INT_32 = 32, "decode_32bit_int"
    INT_64 = 64, "decode_64bit_int"
    FLOAT_32 = 32, "decode_32bit_float"
    FLOAT_64 = 64, "decode_64bit_float"

    def __init__(self, bits: int, decoding_method: str):
        self.bits = bits
        self.decoding_method = decoding_method


_MODBUS_HOLDING_REGISTER_SIZE = 16


class ModbusClient:
    def __init__(self, address: str, port: int = 502):
        self.delegate = ModbusTcpClient(address, port)

    def __enter__(self):
        self.delegate.__enter__()
        return self

    def __exit__(self, klass, value, traceback):
        self.delegate.__exit__(klass, value, traceback)

    def close_connection(self) -> None:
        try:
            log.MainLogger().debug("Close Modbus TCP connection")
            self.delegate.close()
        except Exception as e:
            raise ModuleError(__name__+" "+str(type(e))+" " +
                              str(e), ModuleErrorLevel.ERROR) from e

    def __read_registers(self, read_register_method: Callable,
                         address: int,
                         types: Union[Iterable[ModbusDataType], ModbusDataType],
                         big_endian: bool = True,
                         **kwargs):
        try:
            multi_request = isinstance(types, Iterable)
            if not multi_request:
                types = [types]

            def divide_rounding_up(numerator: int, denominator: int):
                return -(-numerator // denominator)

            number_of_addresses = sum(divide_rounding_up(
                t.bits, _MODBUS_HOLDING_REGISTER_SIZE) for t in types)
            response = read_register_method(
                address, number_of_addresses, **kwargs)
            if response.isError():
                raise response
            decoder = BinaryPayloadDecoder.fromRegisters(
                response.registers, Endian.Big if big_endian else Endian.Little)
            result = [getattr(decoder, t.decoding_method)() for t in types]
            return result if multi_request else result[0]
        except pymodbus.exceptions.ConnectionException as e:
            raise ModuleError(
                "TCP-Client konnte keine Verbindung aufbauen. Bitte Einstellungen (IP-Adresse, ..) und " +
                "Hardware-Anschluss pruefen.",
                ModuleErrorLevel.ERROR
            ) from e
        except pymodbus.exceptions.ModbusIOException as e:
            raise ModuleError(
                "TCP-Client konnte keinen Wert abfragen. Falls vorhanden, parallele Verbindungen, zB. node red," +
                "beenden und bei anhaltender Fehlermeldung Zaehler neustarten.",
                ModuleErrorLevel.WARNING
            ) from e
        except Exception as e:
            raise ModuleError(__name__+" "+str(type(e))+" " +
                              str(e), ModuleErrorLevel.ERROR) from e

    def read_holding_registers(self, address: int,
                               types: Union[Iterable[ModbusDataType], ModbusDataType],
                               **kwargs):
        return self.__read_registers(self.delegate.read_holding_registers, address, types, **kwargs)

    def read_input_registers(self, address: int,
                             types: Union[Iterable[ModbusDataType], ModbusDataType],
                             **kwargs):
        return self.__read_registers(self.delegate.read_input_registers, address, types, **kwargs)
