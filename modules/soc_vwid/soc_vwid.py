#!/usr/bin/python3

import argparse
from argparse import ArgumentParser
import libvwid
import aiohttp
import asyncio
import logging
import time
import json
import os
import pickle

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
    tokensFile= '/var/www/html/openWB/ramdisk/soc_vwid_tokens'+chargepoint

    async with aiohttp.ClientSession() as session:
        w = libvwid.vwid(session)
        w.set_vin(vin)
        w.set_credentials(id, pw)

        try:
            tf = open(tokensFile, "rb")     # try to open tokens file
            w.tokens = pickle.load(tf)      # initialize tokens in vwid
            tokens_old = pickle.dumps(w.tokens) # remember current tokens
            w.headers[Authorization] = Bearer %s % w.tokens["accessToken"]
            tf.close()
        except Exception as e:
            tokens_old = bytearray(1)   # if no old token found set tokens_old to dummy value

        data = await w.get_status()
        if (data):
            print (data['data']['batteryStatus']['currentSOC_pct'])
            try:
                f = open(replyFile, 'w', encoding='utf-8')
            except:
                os.system("sudo rm "+replyFile)
                f = open(replyFile, 'w', encoding='utf-8')
            json.dump(data, f, ensure_ascii=False, indent=4)
            f.close()
            tokens_new = pickle.dumps(w.tokens)
            if ( tokens_new != tokens_old ):    # check for modified tokens
                try:
                    tf = open(tokensFile, "wb") 
                except:
                    os.system("sudo rm "+tokensFile)
                    tf = open(tokensFile, "wb") 
                pickle.dump(w.tokens, tf) # write tokens file
                tf.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

