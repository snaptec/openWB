import base64
import json
import random
import requests
import string
import sys
# import time
import urllib
import uuid
import hashlib


# ---------------Constants-------------------------------------------
auth_server = 'customer.bmwgroup.com'
api_server = 'cocoapi.bmwgroup.com'


# ---------------Helper Function-------------------------------------------
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


# ---------------HTTP Function-------------------------------------------
def getHTTP(url: str = '', headers: str = '', cookies: str = '', timeout: int = 30) -> str:
    try:
        response = requests.get(url, headers=headers, cookies=cookies, timeout=timeout)
    except requests.Timeout:
        print("Connection Timeout")
        raise
    except Exception as e:
        print("HTTP Error:" + str(e))
        raise

    if response.status_code == 200 or response.status_code == 204:
        return response.text
    else:
        print('Request failed, StatusCode: ' + str(response.status_code))
        raise RuntimeError


def postHTTP(url: str = '', data: str = '', headers: str = '', cookies: str = '',
             timeout: int = 30, allow_redirects: bool = True,
             authId: str = '', authSec: str = '') -> str:
    try:
        if authId != '':
            response = requests.post(url, data=data, headers=headers, cookies=cookies,
                                     timeout=timeout, auth=(authId, authSec),
                                     allow_redirects=allow_redirects)
        else:
            response = requests.post(url, data=data, headers=headers, cookies=cookies,
                                     timeout=timeout, allow_redirects=allow_redirects)
    except requests.Timeout:
        print("Connection Timeout")
        raise
    except:
        print("HTTP Error")
        raise

    if response.status_code == 200 or response.status_code == 204:
        return response.text
    elif response.status_code == 302:
        return response.headers["location"]
    else:
        print('Request failed, StatusCode: ' + str(response.status_code))
        raise RuntimeError


def authStage0(region: str, username: str, password: str) -> str:
    try:
        id0 = str(uuid.uuid4())
        id1 = str(uuid.uuid4())
        apiKey = b'NGYxYzg1YTMtNzU4Zi1hMzdkLWJiYjYtZjg3MDQ0OTRhY2Zh'
        ocp = base64.b64decode(apiKey).decode()
        url = 'https://' + api_server + '/eadrax-ucs/v1/presentation/oauth/config'
        headers = {
            'ocp-apim-subscription-key': ocp,
            'bmw-session-id': id0,
            'x-identity-provider': 'gcdm',
            'x-correlation-id': id1,
            'bmw-correlation-Id': id1,
            'user-agent': 'Dart/3.0 (dart:io)',
            'x-user-agent': 'android(TQ2A.230405.003.B2);bmw;3.11.1(29513);0'}
        body = getHTTP(url, headers)
        cfg = json.loads(body)
    except:
        print("authStage0 failed")
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
        # url = 'https://' + auth_server + '/gcdm/oauth/authenticate'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'user-agent': 'Dart/3.0 (dart:io)',
            'x-user-agent': 'android(TQ2A.230405.003.B2);bmw;3.11.1(29513);0'}
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
        # print("authStage1: authcode=" + authcode)
    except:
        print("Authentication stage 1 failed")
        raise

    return authcode


def authStage2(url: str, authcode1: str, code_challenge: str, state: str, nonce: str) -> str:
    try:
        # url = 'https://' + auth_server + '/gcdm/oauth/authenticate'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'user-agent': 'Dart/3.0 (dart:io)',
            'x-user-agent': 'android(TQ2A.230405.003.B2);bmw;3.11.1(29513);0'}
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
        # print("authStage2: response=" + response)
        authcode = dict(urllib.parse.parse_qsl(response.split("?", 1)[1]))["code"]
        # print("authStage2: authcode=" + authcode)
    except:
        print("Authentication stage 2 failed")
        raise

    return authcode


def authStage3(token_url: str, authcode2: str, code_verifier: str) -> dict:
    global config
    try:
        url = token_url
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Authorization': (config['clientId'], config['clientSecret'])}
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        data = {
            'code': authcode2,
            'code_verifier': code_verifier,
            'redirect_uri': config['returnUrl'],
            'grant_type': 'authorization_code'}
        authId = config['clientId']
        authSec = config['clientSecret']
        response = postHTTP(url, data, headers, authId=authId, authSec=authSec, allow_redirects=False)
        # print("authStage3: response=" + response)
        token = json.loads(response)
        # print("authStage3: token=" + json.dumps(token, indent=4))
    except:
        print("Authentication stage 3 failed")
        raise

    return token


def requestToken(username: str, password: str) -> dict:
    global config
    try:
        # new: get oauth config from server
        config = authStage0('0', username, password)
        # print('config=\n' + json.dumps(config, indent=4))
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
        print("Login failed")
        raise

    return token


# ---------------Interface Function-------------------------------------------
def requestData(token: str, vin: str) -> dict:
    try:
        if vin[:2] == 'WB':
            brand = 'bmw'
        elif vin[:2] == 'WM':
            brand = 'mini'
        else:
            print("Unknown VIN")
            raise RuntimeError

        url = 'https://' + api_server + '/eadrax-vcs/v4/vehicles/state'
        headers = {
            'user-agent': 'Dart/3.0 (dart:io)',
            'x-user-agent': 'android(TQ2A.230405.003.B2);' + brand + ';3.11.1(29513);0',
            'bmw-vin': vin,
            'Authorization': (token["token_type"] + " " + token["access_token"])}
        body = getHTTP(url, headers)
        response = json.loads(body)
    except:
        print("Data-Request failed")
        raise

    return response


# ---------------Main Function-------------------------------------------
def main():
    try:
        argsStr = base64.b64decode(str(sys.argv[1])).decode('utf-8')
        argsDict = json.loads(argsStr)

        username = str(argsDict["user"])
        password = str(argsDict["pass"])
        vin = str(argsDict["vin"]).upper()
        socfile = str(argsDict["socfile"])
        meterfile = str(argsDict["meterfile"])
        statefile = str(argsDict["statefile"])
    except:
        print("Parameters could not be processed")
        raise

    try:
        token = requestToken(username, password)
        data = requestData(token, vin)
        soc = int(data["state"]["electricChargingState"]["chargingLevelPercent"])
        print("Download sucessful - SoC: " + str(soc) + "%")
    except:
        print("Request failed")
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
        print("Saving SoC failed")
        raise


if __name__ == '__main__':
    main()
