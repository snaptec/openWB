#!/usr/bin/python3

from argparse import ArgumentParser
import requests
import logging
import os
import time
from datetime import datetime
from typing import Union
from json import loads, dumps

TS_FMT = "%Y-%m-%dT%H:%M:%S"

# OVMS_SERVER = "https://ovms.dexters-web.de:6869"
TOKEN_CMD = "/api/token"
STATUS_CMD = "/api/status"
OVMS_APPL_LABEL = "application"
OVMS_APPL_VALUE = "owb-ovms-1.9"
OVMS_PURPOSE_LABEL = "purpose"
OVMS_PURPOSE_VALUE = "get soc"


def utc2local(utc):
    global log, session, token, vehicleId
    epoch = time.mktime(utc.timetuple())
    offset = datetime.fromtimestamp(epoch) - datetime.utcfromtimestamp(epoch)
    return utc + offset


# sync function
def fetch_soc(id: str, pw: str, chargepoint: int) -> int:
    global log, session, token, vehicleId

    # get soc, from server
    soc = _fetch_soc(id, pw, chargepoint)

    return soc


def read_token_file() -> Union[int, dict]:
    global tokenFile
    rc = 0
    try:
        with open(tokenFile, "r") as f:
            jsonstr = f.read()
            confDict = loads(jsonstr)
    except Exception as e:
        log.exception("Token file read exception" + str(e))
        token = ""
        confDict = {}
        confDict['configuration'] = {}
        confDict['configuration']['token'] = token
        rc = 1
    return rc, confDict


def write_token_file(confDict: dict):
    global tokenFile
    try:
        with open(tokenFile, "w") as f:
            jsonstr = dumps(confDict, indent=4)
            f.write(jsonstr)
    except Exception as e:
        log.exception("Token file write exception" + str(e))

    try:
        os.chmod(tokenFile, 0o777)
    except Exception as e:
        log.exception("chmod tokenFile exception, e="+str(e))
        os.system("sudo chmod 0777 "+tokenFile)


def main():
    global log, session, token, vehicleId, tokenFile, OVMS_SERVER

    log = logging.getLogger("soc_ovms")
    token = ""

    parser = ArgumentParser()
    parser.add_argument("-s", "--server",
                        help="server", metavar="server", required=True)
    parser.add_argument("-u", "--user",
                        help="user", metavar="user", required=True)
    parser.add_argument("-p", "--password",
                        help="password", metavar="password", required=True)
    parser.add_argument("-v", "--vehicleId",
                        help="vehicleId", metavar="vehicleId", required=True)
    parser.add_argument("-c", "--chargepoint",
                        help="chargepoint", metavar="chargepoint", required=True)

    args = vars(parser.parse_args())
    OVMS_SERVER = args['server']
    id = args['user']
    pw = args['password']
    vehicleId = args['vehicleId']
    chargepoint = args['chargepoint']

    # logging setup
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

    log.debug("server=" + OVMS_SERVER +
              ", user=" + id +
              ", pw=" + pw +
              ", vehicleId=" + vehicleId +
              ", cp=" + chargepoint)
    RAMDISKDIR = os.environ.get("RAMDISKDIR", "undefined")
    tokenFile = RAMDISKDIR+'/soc_ovms_tokenlp'+chargepoint

    with requests.Session() as session:
        soc = fetch_soc(id, pw, chargepoint)
        print(str(soc))


# create a new token and store it in the soc_module configuration
def create_token(user_id: str, password: str, chargepoint: int) -> str:
    global log, session, token, vehicleId, OVMS_SERVER
    token_url = OVMS_SERVER + TOKEN_CMD
    appl = OVMS_APPL_VALUE + str(chargepoint)
    data = {
        "username": user_id,
        "password": password
    }
    form_data = {
        OVMS_APPL_LABEL: appl,
        OVMS_PURPOSE_LABEL: OVMS_PURPOSE_VALUE
    }
    try:
        resp = session.post(token_url, params=data, files=form_data)
    except Exception as e:
        resp = e.response

    log.debug("create_token status_code=" + str(resp.status_code))
    tokenDict = loads(resp.text)
    log.debug("create_token response=" + dumps(tokenDict, indent=4))
    token = tokenDict['token']
    confDict = {}
    confDict['configuration'] = {}
    confDict["configuration"]["token"] = resp.text.rstrip()
    log.debug("create_token confDict=" + dumps(confDict, indent=4))
    write_token_file(confDict)

    return token


# check list of token on OVMS server for unused token created by the soc mudule
# if any obsolete token are found these are deleted.
def cleanup_token(user_id: str, password: str, chargepoint: int):
    global log, session, token, vehicleId, OVMS_SERVER
    tokenlist_url = OVMS_SERVER + TOKEN_CMD + '?username=' + user_id + '&' + 'password=' + token

    log.debug("tokenlist_url=" + tokenlist_url)
    try:
        resp = session.get(tokenlist_url)
    except Exception as e:
        log.error("cleanup_token: exception = " + str(e))
        resp = e.response

    status_code = resp.status_code
    if status_code > 299:
        log.error("cleanup_token status_code=" + str(status_code))
        full_tokenlist = {}
    else:
        response = resp.text
        full_tokenlist = loads(response)
        appl = OVMS_APPL_VALUE + str(chargepoint)
        log.debug("cleanup_token status_code=" +
                  str(status_code) + ", full_tokenlist=\n" +
                  dumps(full_tokenlist, indent=4))
        obsolete_tokenlist = list(filter(lambda token:
                                         token[OVMS_APPL_LABEL] == appl and token["token"] != token,
                                         full_tokenlist))
        log.debug("cleanup_token: obsolete_tokenlist=\n" +
                  dumps(obsolete_tokenlist, indent=4))
        if len(obsolete_tokenlist) > 0:
            log.debug("cleanup_token obsolete_tokenlist=\n" + dumps(obsolete_tokenlist, indent=4))
            for tok in obsolete_tokenlist:
                token_to_delete = tok["token"]
                if token_to_delete != token:
                    log.debug("cleanup_token: token_to_delete=" + dumps(tok, indent=4))
                    token_del_url = OVMS_SERVER + TOKEN_CMD + '/' + token_to_delete
                    token_del_url = token_del_url + '?username=' + user_id + '&password=' + token
                    log.debug("token_del_url=" + token_del_url)
                    try:
                        resp = session.delete(token_del_url)
                    except Exception as e:
                        log.error("delete_token: exception = " + str(e))
                        resp = e.response

                    status_code = resp.status_code
                else:
                    log.debug("cleanup_token: skip active token: " + token)
        else:
            log.debug("cleanup_token: no obsolete token found")

    return


# get status for vehicleId
def get_status(user_id: str) -> Union[int, dict]:
    global log, session, token, vehicleId, OVMS_SERVER
    status_url = OVMS_SERVER + STATUS_CMD + '/' + vehicleId + '?username=' + user_id + '&password=' + token

    log.debug("status-url=" + status_url)
    try:
        resp = session.get(status_url)
    except Exception as e:
        resp = e.response

    status_code = resp.status_code
    if status_code > 299:
        log.error("get_status status_code=" + str(status_code) + ", create new token")
        respDict = {}
    else:
        response = resp.text
        respDict = loads(response)
        log.debug("get_status status_code=" + str(status_code) + ", response=" + dumps(respDict, indent=4))
    return int(status_code), respDict


# function to fetch soc, range, soc_ts
def _fetch_soc(user_id: str, password: str, chargepoint: int) -> int:
    global log, session, token, vehicleId

    try:
        rc, confDict = read_token_file()
        if rc == 0:
            tokenstr = confDict['configuration']['token']
            tokdict = loads(tokenstr)
            token = tokdict['token']
            log.debug("read token: " + token)
            if token is None or token == "":
                token = create_token(user_id, password, chargepoint)
                log.debug("create_token: " + token)
    except Exception as e:
        log.info("_fetch_soc exception:" + str(e) + ", create new token")
        token = create_token(user_id, password, chargepoint)
        log.debug("create_token: " + token)

    log.debug("call get_status, token:" + token)
    status_code, statusDict = get_status(user_id)
    if status_code > 299:
        token = create_token(user_id, password, chargepoint)
        status_code, statusDict = get_status(user_id)
        if status_code > 299:
            raise "Authentication Problem, status_code " + str(status_code)

    soc = statusDict['soc']
    range = statusDict['estimatedrange']
    kms = statusDict['odometer']
    vehicle12v = statusDict['vehicle12v']

    soc_ts = statusDict['m_msgtime_s']
    log.info("soc=" + str(soc) +
             ", range=" + str(range) +
             ", soc_ts=" + str(soc_ts) +
             ", km-stand=" + str(float(kms)/10) +
             ", soc_12v=" + str(vehicle12v))

    cleanup_token(user_id, password, chargepoint)

    return int(float(soc))


if __name__ == '__main__':
    main()
