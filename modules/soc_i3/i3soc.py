import base64
import json
import random
import requests
import string
import sys
import os
import time
import urllib
import uuid
import hashlib


# ---------------Constants-------------------------------------------
auth_server = 'customer.bmwgroup.com'
api_server = 'cocoapi.bmwgroup.com'
APIKey = b'NGYxYzg1YTMtNzU4Zi1hMzdkLWJiYjYtZjg3MDQ0OTRhY2Zh'
USER_AGENT = 'Dart/3.3 (dart:io)'
REGION = '0'        # 0 = rest_of_world
BRAND = 'bmw'       # for auth bmw or mini don't matter
X_USER_AGENT1 = 'android(AP2A.240605.024);'
X_USER_AGENT2 = ';4.7.2(35379);'
X_USER_AGENT = X_USER_AGENT1 + BRAND + X_USER_AGENT2 + REGION
CONTENT_TYPE = 'application/x-www-form-urlencoded'
CHARSET = 'charset=UTF-8'

storeFile = 'i3soc.json'


# --------------- Global Variables --------------------------------------
store = {}
config = {}
DEBUGLEVEL = 0
method = ''


# ---------------Helper Function-------------------------------------------

def _error(txt: str):
    print(txt)


def _info(txt: str):
    global DEBUGLEVEL
    if DEBUGLEVEL >= 1:
        print(txt)


def _debug(txt: str):
    global DEBUGLEVEL
    if DEBUGLEVEL > 1:
        print(txt)


def get_random_string(length: int) -> str:
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def create_auth_string(client_id: str, client_password: str) -> str:
    authstring = client_id + ':' + client_password
    authbytes = authstring.encode("ascii")
    b64bytes = base64.b64encode(authbytes)
    authstring = 'Basic ' + b64bytes.decode("ascii")
    return authstring


def create_s256_code_challenge(code_verifier: str) -> str:
    """Create S256 code_challenge with the given code_verifier."""
    data = hashlib.sha256(code_verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("UTF-8")


# initialize store structures when no store is available
def init_store():
    global store
    store = {}
    store['Token'] = {}
    store['expires_at'] = int(0)


# load store from file, initialize store structure if no file exists
def load_store():
    global store
    global storeFile
    try:
        tf = open(storeFile, 'r', encoding='utf-8')
        store = json.load(tf)
        if 'Token' not in store:
            init_store()
        tf.close()
    except FileNotFoundError:
        _error("load_store: store file not found, new authentication required")
        store = {}
        init_store()
    except Exception as e:
        _error("init: loading stored data failed, file: " +
               storeFile + ", error=" + str(e))
        store = {}
        init_store()


# write store file
def write_store():
    global store
    global storeFile
    try:
        tf = open(storeFile, 'w', encoding='utf-8')
    except Exception as e:
        _error("write_store_file: Exception " + str(e))
        os.system("sudo rm -f " + storeFile)
        tf = open(storeFile, 'w', encoding='utf-8')
    json.dump(store, tf, indent=4)
    tf.close()
    try:
        os.chmod(storeFile, 0o666)
    except Exception as e:
        os.system("sudo chmod 0666 " + storeFile)


# ---------------HTTP Function-------------------------------------------
def getHTTP(url: str = '', headers: str = '', cookies: str = '', timeout: int = 30) -> str:
    try:
        response = requests.get(url, headers=headers, cookies=cookies, timeout=timeout)
    except requests.Timeout:
        _error("Connection Timeout")
        raise
    except Exception as e:
        _error("HTTP Error:" + str(e))
        raise

    if response.status_code == 200 or response.status_code == 204:
        return response.text
    else:
        _error('Request failed, StatusCode: ' + str(response.status_code))
        raise RuntimeError


def postHTTP(url: str = '', data: str = '', headers: str = '', cookies: str = '',
             timeout: int = 30, allow_redirects: bool = True,
             authId: str = '', authSec: str = '') -> str:
    try:
        _debug("postHTTP: url=" + url +
               ",\nheaders=" + json.dumps(headers, indent=4) +
               ",\ndata=" + json.dumps(data, indent=4))
        if authId != '':
            response = requests.post(url, data=data, headers=headers, cookies=cookies,
                                     timeout=timeout, auth=(authId, authSec),
                                     allow_redirects=allow_redirects)
        else:
            response = requests.post(url, data=data, headers=headers, cookies=cookies,
                                     timeout=timeout, allow_redirects=allow_redirects)
    except requests.Timeout:
        _error("Connection Timeout")
        raise
    except:
        _error("HTTP Error")
        raise

    if response.status_code == 200 or response.status_code == 204:
        return response.text
    elif response.status_code == 302:
        return response.headers["location"]
    else:
        _error('Request failed, StatusCode: ' + str(response.status_code))
        raise RuntimeError


def authStage0() -> str:
    try:
        id0 = str(uuid.uuid4())
        id1 = str(uuid.uuid4())
        ocp = base64.b64decode(APIKey).decode()
        url = 'https://' + api_server + '/eadrax-ucs/v1/presentation/oauth/config'
        headers = {
            'ocp-apim-subscription-key': ocp,
            'bmw-session-id': id0,
            'x-identity-provider': 'gcdm',
            'x-correlation-id': id1,
            'bmw-correlation-Id': id1,
            'user-agent': USER_AGENT,
            'x-user-agent': X_USER_AGENT}
        body = getHTTP(url, headers)
        cfg = json.loads(body)
    except:
        _error("authStage0 failed")
        raise
    return cfg


# ---------------Authentication Function-------------------------------------------
def authStage1(url: str,
               username: str,
               password: str,
               code_challenge: str,
               state: str,
               nonce: str) -> str:
    global config
    try:
        headers = {
            'Content-Type': CONTENT_TYPE,
            'user-agent': USER_AGENT,
            'x-user-agent': X_USER_AGENT}
        data = {
            'client_id': config['clientId'],
            'response_type': 'code',
            'scope': ' '.join(config['scopes']),
            'redirect_uri': config['returnUrl'],
            'state': state,
            'nonce': nonce,
            'code_challenge': code_challenge,
            'code_challenge_method': 'S256',
            'username': username,
            'password': password,
            'grant_type': 'authorization_code'}

        resp = postHTTP(url, data, headers)
        response = json.loads(resp)
        authcode = dict(urllib.parse.parse_qsl(response["redirect_to"]))["authorization"]
        _debug("authStage1: authcode=" + authcode)
    except:
        _error("Authentication stage 1 failed")
        raise

    return authcode


def authStage2(url: str, authcode1: str, code_challenge: str, state: str, nonce: str) -> str:
    try:
        headers = {
            'Content-Type': CONTENT_TYPE,
            'user-agent': USER_AGENT,
            'x-user-agent': X_USER_AGENT}
        data = {
            'client_id': config['clientId'],
            'response_type': 'code',
            'scope': ' '.join(config['scopes']),
            'redirect_uri': config['returnUrl'],
            'state': state,
            'nonce': nonce,
            'code_challenge': code_challenge,
            'code_challenge_method': 'S256',
            'authorization': authcode1}
        cookies = {
            'GCDMSSO': authcode1}

        response = postHTTP(url, data, headers, cookies, allow_redirects=False)
        _debug("authStage2: response=" + response)
        authcode = dict(urllib.parse.parse_qsl(response.split("?", 1)[1]))["code"]
        _debug("authStage2: authcode=" + authcode)
    except:
        _error("Authentication stage 2 failed")
        raise

    return authcode


def authStage3(token_url: str, authcode2: str, code_verifier: str) -> dict:
    global config
    try:
        url = token_url
        headers = {
            'Content-Type': CONTENT_TYPE + '; ' + CHARSET}
        data = {
            'code': authcode2,
            'code_verifier': code_verifier,
            'redirect_uri': config['returnUrl'],
            'grant_type': 'authorization_code'}
        authId = config['clientId']
        authSec = config['clientSecret']
        response = postHTTP(url, data, headers, authId=authId, authSec=authSec, allow_redirects=False)
        _debug("authStage3: response=" + response)
        token = json.loads(response)
        _debug("authStage3: token=" + json.dumps(token, indent=4))
    except:
        _error("Authentication stage 3 failed")
        raise

    return token


def requestToken(username: str, password: str) -> dict:
    global config
    global method
    try:
        # new: get oauth config from server
        method += ' requestToken'
        config = authStage0()
        _debug('config=\n' + json.dumps(config, indent=4))
        token_url = config['tokenEndpoint']
        authenticate_url = token_url.replace('/token', '/authenticate')
        code_verifier = get_random_string(86)
        code_challenge = create_s256_code_challenge(code_verifier)
        state = get_random_string(22)
        nonce = get_random_string(22)

        authcode1 = authStage1(authenticate_url, username, password, code_challenge, state, nonce)
        authcode2 = authStage2(authenticate_url, authcode1, code_challenge, state, nonce)
        token = authStage3(token_url, authcode2, code_verifier)
    except:
        _error("Login failed")
        raise

    return token


def refreshToken(refreshToken: str) -> dict:
    global config
    global method
    try:
        method += ' refreshToken'
        config = authStage0()
        url = config['tokenEndpoint']
        headers = {
            'Content-Type': CONTENT_TYPE,
            'user-agent': USER_AGENT,
            'x-user-agent': X_USER_AGENT}
        data = {
            'scope': ' '.join(config['scopes']),
            'redirect_uri': config['returnUrl'],
            'grant_type': 'refresh_token',
            'refresh_token': refreshToken}
        authId = config['clientId']
        authSec = config['clientSecret']
        resp = postHTTP(url, data, headers, authId=authId, authSec=authSec, allow_redirects=False)
        token = json.loads(resp)
    except:
        _error("Login failed")
        raise

    return token


# ---------------Interface Function-------------------------------------------
def requestData(token: str, vin: str) -> dict:
    global method
    try:
        method += ' requestData'
        if vin[:2] == 'WB':
            brand = 'bmw'
        elif vin[:2] == 'WM':
            brand = 'mini'
        else:
            _error("Unknown VIN")
            raise RuntimeError

        url = 'https://' + api_server + '/eadrax-vcs/v4/vehicles/state'
        headers = {
            'user-agent': USER_AGENT,
            'x-user-agent': X_USER_AGENT1 + brand + X_USER_AGENT2 + REGION,
            'bmw-vin': vin,
            'Authorization': (token["token_type"] + " " + token["access_token"])}
        body = getHTTP(url, headers)
        response = json.loads(body)
    except:
        _error("Data-Request failed")
        _error("requestData: url=" + url +
               ",\nheaders=" + json.dumps(headers, indent=4))
        raise

    return response


# ---------------Main Function-------------------------------------------
def main():
    global store
    global storeFile
    global DEBUGLEVEL
    global method
    try:
        method = ''
        CHARGEPOINT = os.environ.get("CHARGEPOINT", "1")
        DEBUGLEVEL = int(os.environ.get("debug", "0"))
        RAMDISKDIR = os.environ.get("RAMDISKDIR", "undefined")
        storeFile = RAMDISKDIR + '/soc_i3_cp' + CHARGEPOINT + '.json'
        _debug('storeFile =' + storeFile)

        argsStr = base64.b64decode(str(sys.argv[1])).decode('utf-8')
        argsDict = json.loads(argsStr)

        username = str(argsDict["user"])
        password = str(argsDict["pass"])
        vin = str(argsDict["vin"]).upper()
        socfile = str(argsDict["socfile"])
        meterfile = str(argsDict["meterfile"])
        statefile = str(argsDict["statefile"])
    except:
        _error("Parameters could not be processed")
        raise

    try:
        # try to read store file from ramdisk
        expires_in = -1
        load_store()
        now = int(time.time())
        _debug('main0: store=\n' + json.dumps(store, indent=4))
        # if OK, check if refreshToken is required
        if 'expires_at' in store and \
           'Token' in store and \
           'expires_in' in store['Token'] and \
           'refresh_token' in store['Token']:
            expires_in = store['Token']['expires_in']
            expires_at = store['expires_at']
            token = store['Token']
            _debug('main0: expires_in=' + str(expires_in) + ', now=' + str(now) +
                   ', expires_at=' + str(expires_at) + ', diff=' + str(expires_at - now))
            if now > expires_at - 120:
                _debug('call refreshToken')
                token = refreshToken(token['refresh_token'])
                if 'expires_in' in token:
                    expires_in = int(token['expires_in'])
                    expires_at = now + expires_in
                    store['expires_at'] = expires_at
                    store['Token'] = token
                    write_store()
                else:
                    _error("refreshToken failed, re-authenticate")
                    expires_in = -1
            else:
                expires_in = store['Token']['expires_in']

        # if refreshToken fails, call requestToken
        if expires_in == -1:
            _debug('call requestToken')
            token = requestToken(username, password)

        # compute expires_at and store file in ramdisk
        if 'expires_in' in token:
            if expires_in != int(token['expires_in']):
                expires_in = int(token['expires_in'])
                expires_at = now + expires_in
                store['expires_at'] = expires_at
                store['Token'] = token
                write_store()
        else:
            _error("requestToken failed")
            store['expires_at'] = 0
            store['Token'] = token
            write_store()
        _debug('main: token=\n' + json.dumps(token, indent=4))
        data = requestData(token, vin)
        soc = int(data["state"]["electricChargingState"]["chargingLevelPercent"])
        _info("Successful - SoC: " + str(soc) + "%" + ', method=' + method)
    except:
        _error("Request failed")
        raise

    try:
        with open(socfile, 'w') as f:
            f.write(str(int(soc)))
        state = {}
        state["soc"] = int(soc)
        with open(meterfile, 'r') as f:
            state["meter"] = float(f.read())
        with open(statefile, 'w') as f:
            f.write(json.dumps(state))
    except:
        _error("Saving SoC failed")
        raise


if __name__ == '__main__':
    main()
