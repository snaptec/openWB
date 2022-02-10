#!/usr/bin/python3

import time
import json
from typing import Dict, Tuple

from helpermodules.log import MainLogger
from modules.common import req
from modules.common.fault_state import FaultState


CLIENT_ID = "81527cff06843c8634fdc09e8ac0abefb46ac849f38fe1e431c2ef2106796384"
# UA = "Mozilla/5.0 (Linux; Android 10; Pixel 3 Build/QQ2A.200305.002; wv) AppleWebKit/537.36 (KHTML, like Gecko)
# Version/4.0 Chrome/85.0.4183.81 Mobile Safari/537.36"
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


def post_wake_up_command(vehicle: int, token_file: str) -> str:
    token = __fetch_token(token_file)
    vehicle_id = __get_vehicle_id(vehicle, token)
    command = "vehicles/"+str(vehicle_id)+"/wake_up"
    MainLogger().debug("Sending command: \"%s\"" % (command))
    headers = {
        "user-agent": UA,
        "x-tesla-user-agent": X_TESLA_USER_AGENT,
        "authorization": "bearer " + token["access_token"]
    }
    session = req.get_http_session()
    response = session.post("https://owner-api.teslamotors.com/api/1/" + command, headers=headers, timeout=120).json()
    return response["response"]["state"]


def request_soc(vehicle: int, token_file: str) -> float:
    token = __fetch_token(token_file)
    vehicle_id = __get_vehicle_id(vehicle, token)
    data_part = "vehicles/"+str(vehicle_id)+"/vehicle_data"
    response = __request_data(data_part, token)
    response = json.loads(response)
    soc = response["response"]["charge_state"]["battery_level"]
    return float(soc)


def __fetch_token(token_file):
    token = {
        "access_token": "",
        "created_at": 0,
        "expires_in": 0,
        "refresh_token": ""
    }

    token, expiration = __load_token(token_file)
    MainLogger().debug("No need to authenticate. Valid token already present in " + token_file)
    if time.time() > expiration:
        MainLogger().debug("Access token expired. Refreshing token.")
        token = __refresh_token(token_file, token)
    return token


def __load_token(token_file: str) -> Tuple[Dict, int]:
    with open(token_file, "r") as f:
        token = json.load(f)
        # do not trust teslas expiration date!
        expiration = token["created_at"] + 2500000
        return token, expiration


def __refresh_token(token_file: str, token: Dict) -> Dict:
    headers = {"user-agent": UA, "x-tesla-user-agent": X_TESLA_USER_AGENT}
    payload = {
        "grant_type": "refresh_token",
        "client_id": "ownerapi",
        "refresh_token": token["refresh_token"],
        "scope": "openid email offline_access",
    }
    session = req.get_http_session()

    resp = session.post("https://auth.tesla.com/oauth2/v3/token", headers=headers, json=payload, timeout=120)
    resp_json = resp.json()
    refresh_token = resp_json["refresh_token"]
    access_token = resp_json["access_token"]
    MainLogger().debug("received refresh token")

    # Step 4: Exchange bearer token for access token
    headers["authorization"] = "bearer " + access_token
    payload = {
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "client_id": CLIENT_ID,
    }
    resp = session.post("https://owner-api.teslamotors.com/oauth/token", headers=headers, json=payload)

    # save our token
    resp_json = resp.json()
    token["refresh_token"] = refresh_token
    token["access_token"] = resp_json["access_token"]
    token["created_at"] = resp_json["created_at"]
    token["expires_in"] = resp_json["expires_in"]
    MainLogger().debug("Token Refresh succeeded")
    with open(token_file, "w") as f:
        f.write(json.dumps(token))
    return token


def __get_vehicle_id(index: int, token: Dict) -> str:
    vehicles = __request_data('vehicles', token)
    vehicle_id = str(json.loads(vehicles)["response"][index]["id"])
    MainLogger().debug("vehicle_id for entry %d: %s" % (index, vehicle_id))
    if not vehicle_id:
        raise FaultState.error("Zu EV"+str(index)+" konnte keine ID ermittelt werden.")
    return vehicle_id


def __request_data(data_part: str, token: Dict) -> str:
    MainLogger().debug("Requesting data: \"%s\"" % (data_part))
    headers = {
        "user-agent": UA,
        "x-tesla-user-agent": X_TESLA_USER_AGENT,
        "authorization": "bearer " + token["access_token"]
    }
    session = req.get_http_session()
    response = session.get("https://owner-api.teslamotors.com/api/1/" + data_part, headers=headers, timeout=120)
    return response.text
