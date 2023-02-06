#!/usr/bin/python3

from argparse import ArgumentParser
import libvwid
import aiohttp
import asyncio
import logging
import json
import os
import time
import pickle
import getpass
from datetime import datetime

TS_FMT = "%Y-%m-%dT%H:%M:%S"
# utc_offset = datetime.fromtimestamp(0) - datetime.utcfromtimestamp(0)


def utc2local(utc):
    epoch = time.mktime(utc.timetuple())
    offset = datetime.fromtimestamp(epoch) - datetime.utcfromtimestamp(epoch)
    return utc + offset


async def main():

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
    vin = args['vin']
    id = args['user']
    pw = args['password']
    chargepoint = args['chargepoint']

    # logging setup
    log = logging.getLogger("soc_vwid")
    debug = os.environ.get('debug', '0')
    LOGLEVEL = 'WARN'
    if debug == '1':
        LOGLEVEL = 'INFO'
    if debug == '2':
        LOGLEVEL = 'DEBUG'
    RAMDISKDIR = os.environ.get("RAMDISKDIR", "undefined")
    logFile = RAMDISKDIR+'/soc.log'
    format = '%(asctime)s %(levelname)s:%(name)s:Lp' + str(chargepoint) + ' %(message)s'
    datefmt = '%Y-%m-%d %H:%M:%S'
    logging.basicConfig(filename=logFile,
                        filemode='a',
                        format=format,
                        datefmt=datefmt,
                        level=LOGLEVEL)

    RAMDISKDIR = os.environ.get("RAMDISKDIR", "undefined")
    replyFile = RAMDISKDIR+'/soc_vwid_replylp'+chargepoint
    tokensFile = RAMDISKDIR+'/soc_vwid_tokenslp'+chargepoint

    async with aiohttp.ClientSession() as session:
        w = libvwid.vwid(session)
        w.set_vin(vin)
        w.set_credentials(id, pw)
        w.set_jobs(['charging'])

        try:
            tf = open(tokensFile, "rb")           # try to open tokens file
            w.tokens = pickle.load(tf)            # initialize tokens in vwid
            tokens_old = pickle.dumps(w.tokens)   # remember current tokens
            w.headers['Authorization'] = 'Bearer %s' % w.tokens["accessToken"]
            tf.close()
        except Exception as e:
            log.exception("tokens initialization exception: e="+str(e))
            log.exception("tokens initialization exception: set tokens_old to initial value")
            tokens_old = bytearray(1)   # if no old token found set tokens_old to dummy value

        data = await w.get_status()
        if (data):
            try:
                f = open(replyFile, 'w', encoding='utf-8')
            except Exception as e:
                log.exception("replyFile open exception: e="+str(e)+"user: "+getpass.getuser())
                log.exception("replyFile open Exception, remove existing file")
                os.system("sudo rm "+replyFile)
                f = open(replyFile, 'w', encoding='utf-8')
            json.dump(data, f, ensure_ascii=False, indent=4)
            f.close()
            try:
                os.chmod(replyFile, 0o777)
            except Exception as e:
                log.exception("chmod replyFile exception, e="+str(e))
                log.exception("use sudo, user: "+getpass.getuser())
                os.system("sudo chmod 0777 "+replyFile)

            try:
                soc = data['charging']['batteryStatus']['value']['currentSOC_pct']
                soc_tsZ = data['charging']['batteryStatus']['value']['carCapturedTimestamp']
                soc_tsdtZ = datetime.strptime(soc_tsZ, TS_FMT + "Z")
                soc_tsdtL = utc2local(soc_tsdtZ)
                soc_ts = datetime.strftime(soc_tsdtL, TS_FMT)
                log.info("SOC: " + str(soc) + '%' +
                         '@' + soc_ts)
                print(soc)
            except Exception as e:
                log.exception("reply Exception: e=" + str(e))
                log.exception("charging.batteryStatus.value.currentSOC_pct not found, return 0")
                print("0")

            tokens_new = pickle.dumps(w.tokens)
            if (tokens_new != tokens_old):    # check for modified tokens
                log.debug("tokens_new != tokens_old, rewrite tokens file")
                tf = open(tokensFile, "wb")
                pickle.dump(w.tokens, tf)     # write tokens file
                tf.close()
                try:
                    os.chmod(tokensFile, 0o777)
                except Exception as e:
                    log.exception("chmod tokensFile exception, use sudo, e="+str(e)+"user: "+getpass.getuser())
                    os.system("sudo chmod 0777 "+tokensFile)
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
