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
    parser.add_argument("-c", "--chargepoint", 
                        help="chargepoint", metavar="chargepoint", required=True)

    args = vars(parser.parse_args())
    vin=args['vin']
    id=args['user']
    pw=args['password']
    chargepoint=args['chargepoint']
    replyFile= '/var/www/html/openWB/ramdisk/soc_vwid_replylp'+chargepoint

    async with aiohttp.ClientSession() as session:
        w = libvwid.vwid(session)
        w.set_vin(vin)
        w.set_credentials(id, pw)

        data = await w.get_status()
        if (data):
            print (data['data']['batteryStatus']['currentSOC_pct'])
            f = open(replyFile, 'w', encoding='utf-8')
            json.dump(data, f, ensure_ascii=False, indent=4)
            f.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

