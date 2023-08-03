import base64
import json
import random
import requests
import string
import sys
import time
import urllib

# ---------------Constants-------------------------------------------
auth_server = 'customer.bmwgroup.com'
api_server = 'cocoapi.bmwgroup.com'

client_id = '31c357a0-7a1d-4590-aa99-33b97244d048'
client_password = 'c0e3393d-70a2-4f6f-9d3c-8530af64d552'


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


# ---------------HTTP Function-------------------------------------------
def getHTTP(url: str = '', headers: str = '', cookies: str = '', timeout: int = 30) -> str:
    try:
        response = requests.get(url, headers=headers, cookies=cookies, timeout=timeout)
    except requests.Timeout:
        print("Connection Timeout")
        raise
    except:
        print("HTTP Error")
        raise

    if response.status_code == 200 or response.status_code == 204:
        return response.text
    else:
        print('Request failed, StatusCode: ' + str(response.status_code))
        raise RuntimeError


def postHTTP(url: str = '', data: str = '', headers: str = '', cookies: str = '', timeout: int = 30, allow_redirects: bool = True) -> str:
    try:
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


# ---------------Authentication Function-------------------------------------------
def authStage1(username: str, password: str, code_challenge: str, state: str) -> str:
    try:
        url = 'https://' + auth_server + '/gcdm/oauth/authenticate'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Mobile/15E148 Safari/604.1'}
        data = {
            'client_id': client_id,
            'response_type': 'code',
            'scope': 'openid profile email offline_access smacc vehicle_data perseus dlm svds cesim vsapi remote_services fupo authenticate_user',
            'redirect_uri': 'com.bmw.connected://oauth',
            'state': state,
            'nonce': 'login_nonce',
            'code_challenge': code_challenge,
            'code_challenge_method': 'plain',
            'username': username,
            'password': password,
            'grant_type': 'authorization_code'}
      
        response = json.loads(postHTTP(url, data, headers))
        authcode = dict(urllib.parse.parse_qsl(response["redirect_to"]))["authorization"]
    except:
        print("Authentication stage 1 failed")
        raise
        
    return authcode


def authStage2(authcode1: str, code_challenge: str, state: str) -> str:
    try:
        url = 'https://' + auth_server + '/gcdm/oauth/authenticate'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Mobile/15E148 Safari/604.1'}
        data = {
            'client_id': client_id,
            'response_type': 'code',
            'scope': 'openid profile email offline_access smacc vehicle_data perseus dlm svds cesim vsapi remote_services fupo authenticate_user',
            'redirect_uri': 'com.bmw.connected://oauth',
            'state': state,
            'nonce': 'login_nonce',
            'code_challenge': code_challenge,
            'code_challenge_method': 'plain',
            'authorization': authcode1}
        cookies = {
            'GCDMSSO': authcode1}
      
        response = postHTTP(url, data, headers, cookies, allow_redirects=False)
        authcode = dict(urllib.parse.parse_qsl(response.split("?",1)[1]))["code"]
    except:
        print("Authentication stage 2 failed")
        raise
        
    return authcode


def authStage3(authcode2: str, code_challenge: str) -> dict:
    try:
        url = 'https://' + auth_server + '/gcdm/oauth/token'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Authorization': create_auth_string(client_id, client_password)}
        data = {
            'code': authcode2,
            'code_verifier': code_challenge,
            'redirect_uri': 'com.bmw.connected://oauth',
            'grant_type': 'authorization_code'}
      
        response = postHTTP(url, data, headers, allow_redirects=False)
        token = json.loads(response)
    except:
        print("Authentication stage 3 failed")
        raise
        
    return token


def requestToken(username: str, password: str) -> dict:
    try:
        code_challenge = get_random_string(86)
        state = get_random_string(22)
    
        authcode1 = authStage1(username, password, code_challenge, state)
        authcode2 = authStage2(authcode1, code_challenge, state)
        token = authStage3(authcode2, code_challenge)
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
            'User-Agent': 'Dart/2.14 (dart:io)',
            'x-user-agent': 'android(SP1A.210812.016.C1);' + brand + ';2.5.2(14945);row',
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
