#!/usr/bin/python
import sys
import os
import time
from pymodbus.client.sync import ModbusTcpClient
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--address", required=True, type=str, help="ip address")
parser.add_argument("-i", "--id", required=True, type=int, help="modbus id")
parser.add_argument("-d", "--duration", required=False, type=int, default=2, help="duration in seconds, defaults to 2")
parser.add_argument("-v", "--verbose", action="store_true", help="verbose debug output")
args = parser.parse_args()

if(args.verbose):
    print("CP-Unterbrechung %s #%d: %ds"%(args.address, args.id, args.duration))

client = ModbusTcpClient(args.address, port=8899)
rq = client.write_register(0x0001, 256, unit=args.id)
time.sleep(args.duration)
rq = client.write_register(0x0001, 512, unit=args.id)
