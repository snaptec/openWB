#!/usr/bin/python3

import base64
import hashlib
import os
import sys
import re
import random
import time
import argparse
import json
from urllib.parse import parse_qs
import requests
from datetime import datetime, timezone

try:
    from ...helpermodules import log
except:
    # for 1.9 compability
    from pathlib import Path
    import sys
    parentdir2 = str(Path(os.path.abspath(__file__)).parents[2])
    sys.path.insert(0, parentdir2)
    from helpermodules import log

MAX_ATTEMPTS = 7
CLIENT_ID = "81527cff06843c8634fdc09e8ac0abefb46ac849f38fe1e431c2ef2106796384"
# UA = "Mozilla/5.0 (Linux; Android 10; Pixel 3 Build/QQ2A.200305.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.4183.81 Mobile Safari/537.36"
# X_TESLA_USER_AGENT = "TeslaApp/3.10.9-433/adff2e065/android/10"

# The documentation here:
#   https://tesla-api.timdorr.com/api-basics/authentication Says:
# "Avoid setting a User-Agent header that looks like a browser (such
#  as Chrome or Safari). The SSO service has protections in place
#  that will require executing JavaScript if a browser-like user
#  agent is detected."
# So to get a token I set the strings to:
UA = ""
X_TESLA_USER_AGENT = ""

tokensFilename = ""
tokens = {
    "access_token": "",
    "created_at": 0,
    "expires_in": 0,
    "refresh_token": ""
}
expiration = 0
verbose = False
num = 0
ramdisk = None

def eprint(msg):
    global num
    global ramdisk
    log.log_comp("error", "EV "+str(num)+": "+str(msg), ramdisk, file="soc")

def gen_params():
    verifier_bytes = os.urandom(86)
    code_verifier = base64.urlsafe_b64encode(verifier_bytes).rstrip(b"=")
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier).digest()).rstrip(b"=")
    state = base64.urlsafe_b64encode(os.urandom(16)).rstrip(b"=").decode("utf-8")
    return code_verifier, code_challenge, state

def loadTokens(tokensfile):
    global tokens, expiration
    try:
        with open(tokensfile, "r") as R:
            tokens = json.load(R)
            expiration = tokens["created_at"] + tokens["expires_in"] - 86400
            return True
    except IOError as e:
        if( verbose ):
            eprint("Could not read from file %s: %s (pressing on in hopes of alternate authenticaiton)"%(tokensfile, str(e)))
        return False

def saveTokens(tokensfile):
    try:
        with open(tokensfile, "w") as W:
            W.write(json.dumps(tokens))
            return True
    except IOError as e:
        eprint("Could not write to file %s: %s"%(tokensfile, str(e)))
        return False

def login(email, password, mfaPasscode, tokensfile):
    headers = {
        # "User-Agent": UA,
        # "x-tesla-user-agent": X_TESLA_USER_AGENT,
        # "X-Requested-With": "com.teslamotors.tesla",
    }

    # Step 1: Obtain the login page
    for attempt in range(MAX_ATTEMPTS):
        code_verifier, code_challenge, state = gen_params()

        params = (
            ("client_id", "ownerapi"),
            ("code_challenge", code_challenge),
            ("code_challenge_method", "S256"),
            ("redirect_uri", "https://auth.tesla.com/void/callback"),
            ("response_type", "code"),
            ("scope", "openid email offline_access"),
            ("state", state),
        )

        session = requests.Session()
        resp = session.get("https://auth.tesla.com/oauth2/v3/authorize", headers=headers, params=params)

        if resp.ok and "<title>" in resp.text:
            if( verbose ):
                eprint("Get auth form success - %d attempt(s)."%(attempt + 1))
            break
        time.sleep(3)
    else:
        raise ValueError("Didn't get auth form in %d attempts."%(MAX_ATTEMPTS))

    # Step 2: Obtain an authorization code
    csrf = re.search(r'name="_csrf".+value="([^"]+)"', resp.text).group(1)
    transaction_id = re.search(r'name="transaction_id".+value="([^"]+)"', resp.text).group(1)

    data = {
        "_csrf": csrf,
        "_phase": "authenticate",
        "_process": "1",
        "transaction_id": transaction_id,
        "cancel": "",
        "identity": email,
        "credential": password,
    }

    for attempt in range(MAX_ATTEMPTS):
        resp = session.post(
            "https://auth.tesla.com/oauth2/v3/authorize", headers=headers, params=params, data=data, allow_redirects=False
        )
        if resp.ok and (resp.status_code == 302 or "<title>" in resp.text):
            if( verbose ):
                eprint("Post auth form success - %d attempt(s)."%(attempt + 1))
            break
        time.sleep(3)
    else:
        raise ValueError("Didn't post auth form in %d attempts."%(MAX_ATTEMPTS))

    # Determine if user has MFA enabled
    # In that case there is no redirect to `https://auth.tesla.com/void/callback` and app shows new form with Passcode / Backup Passcode field
    is_mfa = True if resp.status_code == 200 and "/mfa/verify" in resp.text else False

    if is_mfa:
        resp = session.get(
            "https://auth.tesla.com/oauth2/v3/authorize/mfa/factors?transaction_id="+transaction_id, headers=headers,
        )
        # {
        #     "data": [
        #         {
        #             "dispatchRequired": false,
        #             "id": "41d6c32c-b14a-4cef-9834-36f819d1fb4b",
        #             "name": "Device #1",
        #             "factorType": "token:software",
        #             "factorProvider": "TESLA",
        #             "securityLevel": 1,
        #             "activatedAt": "2020-12-07T14:07:50.000Z",
        #             "updatedAt": "2020-12-07T06:07:49.000Z",
        #         }
        #     ]
        # }
        if( verbose ):
            eprint(resp.text)
        factor_id = resp.json()["data"][0]["id"]

        # Can use Passcode
        data = {"transaction_id": transaction_id, "factor_id": factor_id, "passcode": mfaPasscode}
        resp = session.post("https://auth.tesla.com/oauth2/v3/authorize/mfa/verify", headers=headers, json=data)
        # ^^ Content-Type - application/json
        if( verbose ):
            eprint(resp.text)
        # {
        #     "data": {
        #         "id": "63375dc0-3a11-11eb-8b23-75a3281a8aa8",
        #         "challengeId": "c7febba0-3a10-11eb-a6d9-2179cb5bc651",
        #         "factorId": "41d6c32c-b14a-4cef-9834-36f819d1fb4b",
        #         "passCode": "985203",
        #         "approved": true,
        #         "flagged": false,
        #         "valid": true,
        #         "createdAt": "2020-12-09T03:26:31.000Z",
        #         "updatedAt": "2020-12-09T03:26:31.000Z",
        #     }
        # }
        if "error" in resp.text or not resp.json()["data"]["approved"] or not resp.json()["data"]["valid"]:
            raise ValueError("Invalid passcode.")

        # Can use Backup Passcode
        # data = {"transaction_id": transaction_id, "backup_code": "3HZRJVC6D"}
        # resp = session.post(
        #     "https://auth.tesla.com/oauth2/v3/authorize/mfa/backupcodes/attempt", headers=headers, json=data
        # )
        # # ^^ Content-Type - application/json
        # if( verbose ):
        #     eprint(resp.text)
        # # {
        # #     "data": {
        # #         "valid": true,
        # #         "reason": null,
        # #         "message": null,
        # #         "enrolled": true,
        # #         "generatedAt": "2020-12-09T06:14:23.170Z",
        # #         "codesRemaining": 9,
        # #         "attemptsRemaining": 10,
        # #         "locked": false,
        # #     }
        # # }
        # if "error" in resp.text or not resp.json()["data"]["valid"]:
        #     raise ValueError("Invalid backup passcode.")

        data = {"transaction_id": transaction_id}

        for attempt in range(MAX_ATTEMPTS):
            resp = session.post(
                "https://auth.tesla.com/oauth2/v3/authorize",
                headers=headers,
                params=params,
                data=data,
                allow_redirects=False,
            )
            if resp.headers.get("location"):
                if( verbose ):
                    eprint("Got location in %d attempt(s)."%(attempt + 1))
                break
        else:
            raise ValueError("Didn't get location in %d attempts."%(MAX_ATTEMPTS))

    # Step 3: Exchange authorization code for bearer token
    code = parse_qs(resp.headers["location"])["https://auth.tesla.com/void/callback?code"]
    if( verbose ):
        eprint("received callback code")
        # eprint("Code -", code)
    
    # headers = {"user-agent": UA, "x-tesla-user-agent": X_TESLA_USER_AGENT}
    headers = {}
    payload = {
        "grant_type": "authorization_code",
        "client_id": "ownerapi",
        "code_verifier": code_verifier.decode("utf-8"),
        "code": code,
        "redirect_uri": "https://auth.tesla.com/void/callback",
    }

    resp = session.post("https://auth.tesla.com/oauth2/v3/token", headers=headers, json=payload)
    resp_json = resp.json()
    refresh_token = resp_json["refresh_token"]
    access_token = resp_json["access_token"]
    if( verbose ):
        eprint("received refresh token")
        # eprint("{\"refresh_token\": \"" + refresh_token + "\"}")

    # Step 4: Exchange bearer token for access token
    headers["authorization"] = "bearer " + access_token
    payload = {
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "client_id": CLIENT_ID,
    }
    resp = session.post("https://owner-api.teslamotors.com/oauth/token", headers=headers, json=payload)

    # save our tokens
    resp_json = resp.json()
    tokens["refresh_token"] = refresh_token
    tokens["access_token"] = resp_json["access_token"]
    tokens["created_at"] = resp_json["created_at"]
    tokens["expires_in"] = resp_json["expires_in"]
    return saveTokens(tokensfile)

def refreshToken(email, tokensfile):
    global tokens

    headers = {"user-agent": UA, "x-tesla-user-agent": X_TESLA_USER_AGENT}
    payload = {
        "grant_type": "refresh_token",
        "client_id": "ownerapi",
        "refresh_token": tokens["refresh_token"],
        "scope": "openid email offline_access",
    }
    session = requests.Session()

    resp = session.post("https://auth.tesla.com/oauth2/v3/token", headers=headers, json=payload, timeout=120)
    resp_json = resp.json()
    refresh_token = resp_json["refresh_token"]
    access_token = resp_json["access_token"]
    if( verbose ):
        eprint("received refresh token")
        # eprint("{\"refresh_token\": \"" + refresh_token + "\"}")

    # Step 4: Exchange bearer token for access token
    headers["authorization"] = "bearer " + access_token
    payload = {
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "client_id": CLIENT_ID,
    }
    resp = session.post("https://owner-api.teslamotors.com/oauth/token", headers=headers, json=payload)

    # save our tokens
    resp_json = resp.json()
    tokens["refresh_token"] = refresh_token
    tokens["access_token"] = resp_json["access_token"]
    tokens["created_at"] = resp_json["created_at"]
    tokens["expires_in"] = resp_json["expires_in"]
    return saveTokens(tokensfile)

def listCars():
     myList = []
     myVehicles = requestData('vehicles').text
     for index, car in enumerate(json.loads(myVehicles)["response"]):
         myList.append(json.loads("{\"id\":\"%s\", \"vin\":\"%s\", \"name\":\"%s\"}"%(index, car["vin"], car["display_name"])))
     print(json.dumps(myList))

def getVehicleIdByVin(vin):
    myVehicles = requestData('vehicles').text
    for car in json.loads(myVehicles)["response"]:
        if( verbose ):
            eprint("VIN: %s"%(car["vin"]))
        if( car["vin"] == vin):
            myVehicleId = car["id"]
            if( verbose ):
                eprint("vehicle_id for vin %s: %s"%(vin, str(myVehicleId)))
            return myVehicleId
    eprint("vin not found: %s"%(vin))
    for index, car in enumerate(json.loads(myVehicles)["response"]):
        eprint("Index: %d VIN: %s"%(index, car["vin"]))

def getVehicleIdByIndex(index):
    myVehicles = requestData('vehicles').text
    myVehicleId = json.loads(myVehicles)["response"][int(index)]["id"]
    if( verbose ):
        eprint("vehicle_id for entry %d: %s"%(index, str(myVehicleId)))
    return myVehicleId

def requestData(dataPart):
    if( verbose ):
        eprint("Requesting data: \"%s\""%(dataPart))
    session = requests.Session()
    headers = {
        "user-agent": UA,
        "x-tesla-user-agent": X_TESLA_USER_AGENT,
        "authorization": "bearer " + tokens["access_token"]
        }

    owner_headers = headers
    # owner_headers["authorization"] = "bearer " + tokens["access_token"]
    owner_headers = {**headers, "authorization": "bearer " + tokens["access_token"]}

    resp = session.get("https://owner-api.teslamotors.com/api/1/" + dataPart, headers=owner_headers, timeout=120)
    if( verbose ):
        eprint(resp.text, "\n")
    return resp

def postCommand(command):
    if( verbose ):
        eprint("Sending command: \"%s\""%(command))
    session = requests.Session()
    headers = {
        "user-agent": UA,
        "x-tesla-user-agent": X_TESLA_USER_AGENT,
        "authorization": "bearer " + tokens["access_token"]
        }
 
    owner_headers = headers
    # owner_headers["authorization"] = "bearer " + tokens["access_token"]
    owner_headers = {**headers, "authorization": "bearer " + tokens["access_token"]}

    resp = session.post("https://owner-api.teslamotors.com/api/1/" + command, headers=owner_headers, timeout=120)
    if( verbose ):
        eprint(resp.text, "\n")
    return resp

def lib(email, ev_num, p_ramdisk, tokensfile="tesla.token", data=None, command=None, vehicle=0, vin=None, listcars=False, p_verbose=False):
    global num
    num = ev_num
    global ramdisk
    ramdisk = p_ramdisk
    global verbose
    verbose = p_verbose

    if( not loadTokens(tokensfile) ):
        eprint("Tokens file not found: " + tokensfile)
        eprint("Login with E-Mail and Password not supported (Captcha)!")
        return 0
    else:
        if( verbose ):
            eprint("No need to authenticate. Valid tokens already present in " + tokensFilename)
        if( time.time() > expiration ):
            if( verbose ):
                eprint("Access token expired. Refreshing token.")
            try:
                if( refreshToken(email, tokensfile) ):
                    if( verbose ):
                        eprint("Token Refresh succeeded")
            except ValueError as err:
                eprint(err)
                eprint("Token Refresh failed")
                return 0

    if listcars == True:
        listCars()
        return 0
    if vin != None:
        vehicleID = getVehicleIdByVin(vin)
    else:
        vehicleID = getVehicleIdByIndex(vehicle)
    if vehicleID != None:
        if data != None :
            response = requestData(data.replace("#", str(vehicleID)))
            #print(json.dumps(json.loads(response)["response"]))
        if command != None:
            response = postCommand(command.replace("#", str(vehicleID)))
            #print(json.dumps(json.loads(response)["response"]))
    return response