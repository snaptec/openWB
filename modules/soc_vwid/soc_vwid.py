#!/usr/bin/python3

import argparse
from argparse import ArgumentParser
import libvwid
import aiohttp
import asyncio
import logging
import time
import json

async def main():
#    logging.basicConfig(level=logging.DEBUG)

    parser = ArgumentParser()
    parser.add_argument("-v", "--vin", 
                        help="VIN of vehicle", metavar="VIN", required=True)
    parser.add_argument("-u", "--user", 
                        help="user", metavar="user", required=True)
    parser.add_argument("-p", "--password", 
                        help="password", metavar="password", required=True)

    args = vars(parser.parse_args())
    vin=args['vin']
    id=args['user']
    pw=args['password']

    async with aiohttp.ClientSession() as session:
        w = libvwid.vwid(session)
        w.set_vin(vin)
        w.set_credentials(id, pw)

        data = await w.get_status()
        if (data):
            print (data['data']['batteryStatus']['currentSOC_pct'])

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

