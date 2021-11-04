#!/usr/bin/env python3
""" Das Modul baut eine Modbus-TCP-Verbindung auf. Es gibt verschiedene Funktionen, um die gelesenen Register zu formatieren.
"""
import codecs
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
import pymodbus
import struct

try:
    from ...helpermodules import log
    from ..common.module_error import ModuleError, ModuleErrorLevels
except:
    from pathlib import Path
    import os
    import sys
    parentdir2 = str(Path(os.path.abspath(__file__)).parents[2])
    sys.path.insert(0, parentdir2)
    from helpermodules import log
    from modules.common.module_error import ModuleError, ModuleErrorLevels


class ConnectTcp:
    def __init__(self, name: str, id: int, ip_address: str, port: int) -> None:
        try:
            self.tcp_client = ModbusTcpClient(ip_address, port)
            log.MainLogger().debug("Baue Verbindung auf zu "+str(self.tcp_client))
            # Den Verbinungsaufbau übernimmt der tcp_client automatisch.
            self.name = name
            self.id = id
            self.decode_hex = codecs.getdecoder("hex_codec")
        except:
            log.MainLogger().exception(self.name)

    def close_connection(self) -> None:
        try:
            log.MainLogger().debug("Close Modbus TCP connection")
            self.tcp_client.close()
        except:
            log.MainLogger().exception(self.name)

    def __process_modbus_error(self, e):
        if isinstance(e, pymodbus.exceptions.ConnectionException):
            raise ModuleError("TCP-Client konnte keine Verbindung aufbauen. Bitte Einstellungen (IP-Adresse, ..) und Hardware-Anschluss pruefen.", ModuleErrorLevels.ERROR) from e
        elif isinstance(e, pymodbus.exceptions.ModbusIOException):
            self.close_connection()
            raise ModuleError("TCP-Client konnte keinen Wert abfragen. Falls vorhanden, parallele Verbindungen, zB. node red, beenden und bei anhaltender Fehlermeldung Zaehler neustarten.", ModuleErrorLevels.WARNING) from e
        else:
            raise ModuleError(__name__+" "+str(type(e))+" "+str(e), ModuleErrorLevels.ERROR) from e

    def read_integer_registers(self, reg: int, len: int, id: int) -> int:
        try:
            resp = self.tcp_client.read_input_registers(reg, len, unit=id)
            if type(resp) == pymodbus.exceptions.ModbusIOException:
                self.__process_modbus_error(resp)
            all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
            return int(struct.unpack('>i', self.decode_hex(all)[0])[0])
        except Exception as e:
            self.__process_modbus_error(e)
            

    def read_short_int_registers(self, reg: int, len: int, id: int) -> int:
        try:
            resp = self.tcp_client.read_holding_registers(reg, len, unit=id)
            if type(resp) == pymodbus.exceptions.ModbusIOException:
                self.__process_modbus_error(resp)
            all = format(resp.registers[0], '04x')
            return int(struct.unpack('>h', self.decode_hex(all)[0])[0])
        except Exception as e:
            self.__process_modbus_error(e)

    def read_float_registers(self, reg: int, len: int, id: int) -> float:
        try:
            resp = self.tcp_client.read_input_registers(reg, len, unit=id)
            if type(resp) == pymodbus.exceptions.ModbusIOException:
                self.__process_modbus_error(resp)
            return float(struct.unpack('>f', struct.pack('>HH', *resp.registers))[0])
        except Exception as e:
            self.__process_modbus_error(e)

    def read_registers(self, reg: int, len: int, id: int) -> float:
        try:
            resp = self.tcp_client.read_input_registers(reg, len, unit=id)
            if type(resp) == pymodbus.exceptions.ModbusIOException:
                self.__process_modbus_error(resp)
            return float(resp.registers[1])
        except Exception as e:
            self.__process_modbus_error(e)

    def read_binary_registers_to_int(self, reg: int, id: int, bit: int, signed=True) -> int:
        try:
            resp = self.tcp_client.read_holding_registers(reg, bit/8, unit=id)
            if type(resp) == pymodbus.exceptions.ModbusIOException:
                self.__process_modbus_error(resp)
            decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
            if bit == 32:
                if signed == True:
                    value = int(decoder.decode_32bit_int())
                else:
                    value = int(decoder.decode_32bit_uint())
            elif bit == 16:
                if signed == True:
                    value = int(decoder.decode_16bit_int())
                else:
                    value = int(decoder.decode_16bit_uint())
            else:
                raise Exception("Invalid value for bit: "+str(bit)+". Allowed values are 16, 32")
            return value
        except Exception as e:
            self.__process_modbus_error(e)

    def read_binary_registers_to_float(self, reg: int, id: int, bit: int) -> float:
        try:
            resp = self.tcp_client.read_holding_registers(reg, bit/8, unit=id)
            if type(resp) == pymodbus.exceptions.ModbusIOException:
                self.__process_modbus_error(resp)
            decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
            if bit == 32:
                value = float(decoder.decode_32bit_float())
            elif bit == 16:
                value = float(decoder.decode_16bit_float())
            else:
                raise Exception("Invalid value for bit: "+str(bit)+". Allowed values are 16, 32")
            return value
        except Exception as e:
            self.__process_modbus_error(e)
