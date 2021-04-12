#!/usr/bin/python
from pymodbus.client.sync import ModbusTcpClient
import sys
import os
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--address", required=True, type=str, help="ip address")
parser.add_argument("-i", "--id", required=True, type=int, help="modbus id")
parser.add_argument("-p", "--phases", required=True, type=int, choices=[1, 3], help="phases to activate")
parser.add_argument("-d", "--duration", required=False, type=int, default=1, help="duration in seconds, defaults to 1")
parser.add_argument("-v", "--verbose", required=False, action="store_true", help="verbose debug output")
args = parser.parse_args()

if(args.verbose):
    print("Wartezeit vor und nach %dp Umschaltung %s #%d: %ds"%(args.phases, args.address, args.id, args.duration))

client = ModbusTcpClient(args.address, port=8899)
if ( args.phases == 1 ):
    rq = client.write_register(0x0001, 256, unit=args.id)
    time.sleep(args.duration)
    rq = client.write_register(0x0001, 512, unit=args.id)

elif ( args.phases == 3 ):
    rq = client.write_register(0x0002, 256, unit=args.id)
    time.sleep(args.duration)
    rq = client.write_register(0x0002, 512, unit=args.id)

