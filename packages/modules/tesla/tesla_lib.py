#!/usr/bin/python3

import time
import json
from typing import Dict, Tuple

from helpermodules.log import MainLogger
from modules.common import req


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


def load_token(token_file: str) -> Tuple[Dict, int]:
    with open(token_file, "r") as f:
        token = json.load(f)
        # do not trust teslas expiration date!
        expiration = token["created_at"] + 2500000
        return token, expiration


def refresh_token(token_file: str, token: Dict) -> Dict:
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


def get_vehicle_id(index: int, token: Dict) -> str:
    vehicles = request_data('vehicles', token)
    vehicle_id = str(json.loads(vehicles)["response"][index]["id"])
    MainLogger().debug("vehicle_id for entry %d: %s" % (index, vehicle_id))
    return vehicle_id


def request_data(data_part: str, token: Dict) -> str:
    MainLogger().debug("Requesting data: \"%s\"" % (data_part))
    headers = {
        "user-agent": UA,
        "x-tesla-user-agent": X_TESLA_USER_AGENT,
        "authorization": "bearer " + token["access_token"]
    }
    session = req.get_http_session()
    response = session.get("https://owner-api.teslamotors.com/api/1/" + data_part, headers=headers, timeout=120)
    return response.text


def post_command(command: str, token: Dict) -> str:
    MainLogger().debug("Sending command: \"%s\"" % (command))
    headers = {
        "user-agent": UA,
        "x-tesla-user-agent": X_TESLA_USER_AGENT,
        "authorization": "bearer " + token["access_token"]
    }
    session = req.get_http_session()
    response = session.post("https://owner-api.teslamotors.com/api/1/" + command, headers=headers, timeout=120)
    return response.text


def lib(
        token_file: str = "tesla.token",
        data: str = None,
        command: str = None,
        vehicle: int = 0) -> str:

    response = ""
    token = {
        "access_token": "",
        "created_at": 0,
        "expires_in": 0,
        "refresh_token": ""
    }

    token, expiration = load_token(token_file)
    MainLogger().debug("No need to authenticate. Valid token already present in " + token_file)
    if time.time() > expiration:
        MainLogger().debug("Access token expired. Refreshing token.")
    token = refresh_token(token_file, token)

    vehicle_id = get_vehicle_id(vehicle, token)
    if vehicle_id:
        if data is not None:
            response = request_data(data.replace("#", vehicle_id), token)
        if command is not None:
            response = post_command(command.replace("#", vehicle_id), token)
    return response
