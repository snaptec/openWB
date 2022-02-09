#!/usr/bin/python3

import base64
import hashlib
import os
import re
import time
import json
from urllib.parse import parse_qs
import requests

from helpermodules.log import MainLogger

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


def loadTokens():
    global tokens, expiration
    try:
        with open(tokensFilename, "r") as R:
            tokens = json.load(R)
            # do not trust teslas expiration date!
            # expiration = tokens["created_at"] + tokens["expires_in"] - 86400
            expiration = tokens["created_at"] + 2500000
            return True
    except IOError as e:
        MainLogger().exception(
            "Could not read from file %s: %s (pressing on in hopes of alternate authenticaiton)" %
            (tokensFilename, str(e)))
        return False


def saveTokens():
    try:
        with open(tokensFilename, "w") as W:
            W.write(json.dumps(tokens))
            return True
    except IOError as e:
        MainLogger().exception("Could not write to file %s: %s" % (tokensFilename, str(e)))
        return False


def refreshToken():
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
    MainLogger().debug("received refresh token")
    # MainLogger().debug("{\"refresh_token\": \"" + refresh_token + "\"}")

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
    return saveTokens()


def getVehicleIdByIndex(index):
    myVehicles = requestData('vehicles')
    myVehicleId = json.loads(myVehicles)["response"][index]["id"]
    MainLogger().debug("vehicle_id for entry %d: %s" % (index, str(myVehicleId)))
    return myVehicleId


def requestData(dataPart):
    MainLogger().debug("Requesting data: \"%s\"" % (dataPart))
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
    MainLogger().debug(resp.text, "\n")
    return resp.text


def postCommand(command):
    MainLogger().debug("Sending command: \"%s\"" % (command))
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
    MainLogger().debug(resp.text, "\n")
    return resp.text


def lib(
        tokensfile: str = "tesla.token",
        data: str = None,
        command: str = None,
        vehicle: int = 0) -> str:

    response = ""
    global tokensFilename
    tokensFilename = tokensfile
    if(not loadTokens()):
        raise Exception("Login with E-Mail and Password not supported (Captcha)!")
    else:
        MainLogger().debug("No need to authenticate. Valid tokens already present in " + tokensfile)
        if(time.time() > expiration):
            MainLogger().debug("Access token expired. Refreshing token.")
            try:
                if(refreshToken()):
                    MainLogger().debug("Token Refresh succeeded")
            except ValueError as err:
                raise Exception("Token Refresh failed")

    vehicleID = getVehicleIdByIndex(vehicle)
    if(vehicleID != None):
        if(data != None):
            response = requestData(data.replace("#", str(vehicleID)))
            print(json.dumps(json.loads(response)["response"]))
        if(command != None):
            response = postCommand(command.replace("#", str(vehicleID)))
            print(json.dumps(json.loads(response)["response"]))
    return response
