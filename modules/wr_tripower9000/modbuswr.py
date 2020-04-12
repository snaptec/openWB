#!/usr/bin/python
import sys
import os
import time
import getopt
import socket
import ConfigParser
import struct
import binascii
from pymodbus.client.sync import ModbusTcpClient

class ModbusWR:
    def __init__(self, ip):
        self.host = ip
    
    def read(self):
        client = ModbusTcpClient(self.host, port=502)

        #pv watt
        resp= client.read_holding_registers(30775,2,unit=3)
        value1 = resp.registers[0]
        value2 = resp.registers[1]
        all = format(value1, '04x') + format(value2, '04x')
        power = int(struct.unpack('>i', all.decode('hex'))[0])
        if power < 0:
            power = 0
        power = -power

        #pv Wh
        resp= client.read_holding_registers(30529,2,unit=3)
        value1 = resp.registers[0]
        value2 = resp.registers[1]
        all = format(value1, '04x') + format(value2, '04x')
        generation = int(struct.unpack('>i', all.decode('hex'))[0])
        return power, generation

if __name__ == '__main__':
   power, generation = ModbusWR(sys.argv[1]).read()
   print("Current power: %s; Total generation: %s" % (power,generation))
   
