#!/usr/bin/python3

import requests
import json
import sys
import time
import html
from pathlib import Path

# call parameters
charge_point = sys.argv[1][-1]  # get last Character to identify the Chargepoint
code = sys.argv[2]

# debug = int(os.environ.get('debug'))
debug = 0
base_dir = str(Path(__file__).resolve().parents[2]) + "/"
module_dir = str(Path(__file__).resolve().parents[0]) + "/"
client_id = ""
client_secret = ""
callback = ""


def printDebug(message, level):
    if level <= debug:
        print("<p>" + html.escape(message) + "</p>")


def printHtml(message):
    print("<p>" + html.escape(message) + "</p>")


print("<html>\n<head>\n<meta charset=\"utf-8\" />\n</head>\n<body>\n")

# get SoC module config from openwb.conf
with open(base_dir + 'openwb.conf', 'r') as fd:
    for line in fd:
        try:
            printDebug("owb Conf: " + line, 2)
            (key, val) = line.rstrip().split("=")
            if key == "debug":
                debug = int(val)
            if key == "soc_eq_client_id_lp" + str(charge_point):
                printDebug("Found Client ID: " + val, 1)
                client_id = val
            if key == "soc_eq_client_secret_lp" + str(charge_point):
                printDebug("Found Client Secret: " + val, 1)
                client_secret = val
            if key == "soc_eq_cb_lp" + str(charge_point):
                printDebug("Found callback URL: " + val, 1)
                callback = val.replace("'", "")
        except Exception:
            val = ""

# tok_url  = "https://id.mercedes-benz.com/as/token.oauth2"
tok_url = "https://ssoalpha.dvb.corpinter.net/v1/token"

data = {'grant_type': 'authorization_code', 'code': str(code), 'redirect_uri': callback}
# call API to get Access/Refresh tokens
act = requests.post(tok_url, data=data, verify=True, allow_redirects=False, auth=(client_id, client_secret))

printDebug(act.url, 1)

if act.status_code == 200:
    # valid Response
    tokens = json.loads(act.text)
    access_token = tokens['access_token']
    refresh_token = tokens['refresh_token']
    expires_in = tokens['expires_in'] - 60 + int(time.time())

    # write tokens to files
    with open(module_dir + 'soc_eq_acc_lp' + str(charge_point), 'w') as fd:
        json.dump({'expires_in': expires_in, 'refresh_token': refresh_token, 'access_token': access_token}, fd)

if act.status_code == 200:
    printHtml("Anmeldung erfolgreich!")
    print("<a href=""javascript:window.close()"">Sie können das Fenster schließen.</a>")
else:
    printHtml("Anmeldung Fehlgeschlagen Code: " + str(act.status_code) + " " + act.text)
print("</body>\n</html>")
