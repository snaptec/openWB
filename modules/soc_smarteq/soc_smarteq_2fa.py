#!/usr/bin/python3

from argparse import ArgumentParser
import requests
import json
import os
import time
import datetime
import logging
import copy
import urllib
import uuid

# Constants
BASE_URL = "https://id.mercedes-benz.com"
TOKEN_URL = BASE_URL + "/as/token.oauth2"
STATUS_URL_SMART = "https://oneapp.microservice.smart.mercedes-benz.com"
STATUS_URL_MERCEDES = "https://bff.emea-prod.mobilesdk.mercedes-benz.com"
SCOPE = "openid+profile+email+phone+ciam-uid+offline_access"
CLIENT_ID = "70d89501-938c-4bec-82d0-6abb550b0825"
GUID = "280C6B55-F179-4428-88B6-E0CCF5C22A7C"
ACCEPT_LANGUAGE = "de-DE;q=1.0"
SSL_VERIFY_STATUS = True
LOGIN_APP_ID = "01398c1c-dc45-4b42-882b-9f5ba9f175f1"
COUNTRY_CODE = "DE"
X_APPLICATIONNAME_ECE = "mycar-store-ece"
RIS_APPLICATION_VERSION = "1.40.0 (2097)"
RIS_OS_NAME = "ios"
RIS_OS_VERSION = "17.3"
RIS_SDK_VERSION = "2.111.1"
X_LOCALE = "de-DE"
WEBSOCKET_USER_AGENT = "MyCar/1.40.0 (com.daimler.ris.mercedesme.ece.ios; build:2097; iOS 17.3.0) Alamofire/5.4.0"
STATUS_USER_AGENT = "Device: iPhone 6; OS-version: iOS_12.5.1; App-Name: smart EQ control; App-Version: 3.0;\
                    Build: 202108260942; Language: de_DE"
CONTENT_TYPE_OAUTH = "application/x-www-form-urlencoded"
CONTENT_TYPE = "application/json"
ACCEPT = "*/*"
ACCEPT_LANGUAGE = "de-DE;q=1.0"


# helper functions
def nested_key_exists(element: dict, *keys: str) -> bool:
    # Check if *keys (nested) exists in `element` (dict).
    if not isinstance(element, dict):
        raise AttributeError('nested_key_exists() expects dict as first argument - got type ' + str(type(element)))
    if len(keys) == 0:
        raise AttributeError('nested_key_exists() expects at least two arguments, one given.')

    _element = element
    for key in keys:
        try:
            _element = _element[key]
        except KeyError:
            return False
    return True


class smarteq:
    def __init__(self, storeFile: str):
        self.storeFile = storeFile

        self.log = logging.getLogger("soc_smarteq_2fa")
        debug = os.environ.get('debug', '0')
        LOGLEVEL = 'WARN'
        if debug == '1':
            LOGLEVEL = 'INFO'
        if debug == '2':
            LOGLEVEL = 'DEBUG'
        RAMDISKDIR = os.environ.get("RAMDISKDIR", "undefined")
        logFile = RAMDISKDIR+'/soc.log'
        format = '%(asctime)s %(levelname)s:%(name)s:%(message)s'
        datefmt = '%Y-%m-%d %H:%M:%S'
        logging.basicConfig(filename=logFile,
                            filemode='a',
                            format=format,
                            datefmt=datefmt,
                            level=LOGLEVEL)

        # for testing send logs to console
        if os.environ.get('logConsole', '0') == '1':
            consoleHandler = logging.StreamHandler()
            consoleHandler.setFormatter(logging.Formatter(format, datefmt))
            self.log.addHandler(consoleHandler)

        # self.method keeps a high level trace of actions
        self.method = ''
        self.soc_ts = 'n/a'

        self._country_code = COUNTRY_CODE
        self.session = requests.session()

        self.load_store()
        self.oldTokens = copy.deepcopy(self.store['Tokens'])

    # set_authState
    # authState: 'init'
    #            'authenticated'
    #            'tokenRequested'
    #            'pinRequested'
    #            'accessTokenExpired'
    def set_authState(self, state: str):
        if 'authState' in self.store:
            old_state = self.store['authState']
        else:
            old_state = 'n/a'
        self.store['authState'] = state
        self.log.debug('set_authState from ' + old_state + ' to ' + state)

    # initialize store structures when no store is available
    def init_store(self):
        self.store['Tokens'] = {}
        self.store['Tokens']['access_token'] = ""
        self.store['Tokens']['refresh_token'] = ""
        # self.store['refresh_token_history'] = []
        self.store['refresh_timestamp'] = int(0)
        self.set_authState('init')
        self.store['last_pin_used'] = ''

    # load store from file, initialize store structure if no file exists
    def load_store(self):
        try:
            tf = open(self.storeFile, 'r', encoding='utf-8')
            self.store = json.load(tf)
            if 'Tokens' not in self.store:
                self.init_store()
            tf.close()
        except FileNotFoundError:
            self.log.warning("init: store file not found, new 2FA authentication required")
            self.store = {}
            self.init_store()
            self.set_authState('init')
        except Exception as e:
            self.log.debug("init: loading stored data failed, file: " +
                           self.storeFile + ", error=" + str(e))
            self.store = {}
            self.init_store()

    # write store file
    def write_store(self):
        try:
            tf = open(self.storeFile, 'w', encoding='utf-8')
        except Exception as e:
            self.log.debug("write_store_file: Exception " + str(e))
            os.system("sudo rm -f " + self.storeFile)
            tf = open(self.storeFile, 'w', encoding='utf-8')
        json.dump(self.store, tf, indent=4)
        tf.close()
        try:
            os.chmod(self.storeFile, 0o777)
        except Exception as e:
            os.system("sudo chmod 0777 " + self.storeFile)

    # set username and pin
    def set_credentials(self, username: str, pin: str):
        self.username = username
        self.pin = pin

    # set vin
    def set_vin(self, vin: str):
        self.vin = vin

    # set chargepoint number
    def set_chargepoint(self, chargepoint: str):
        self.chargepoint = chargepoint


# 2fa authentication functions
    # send request for new pin to oauth server
    def request_pin(self, email: str, nonce: str):
        self.log.debug("Start request_pin: email=" + email + ", nonce=" + nonce)

        headers = {
            "Host": "bff.emea-prod.mobilesdk.mercedes-benz.com",
            "Ris-Os-Name": RIS_OS_NAME,
            "Ris-Os-Version": RIS_OS_VERSION,
            "Ris-Sdk-Version": RIS_SDK_VERSION,
            "X-Locale": X_LOCALE,
            "X-Trackingid": str(uuid.uuid4()),
            "X-Sessionid": str(uuid.uuid4()),
            "User-Agent": WEBSOCKET_USER_AGENT,
            "Content-Type": CONTENT_TYPE,
            "X-Applicationname": X_APPLICATIONNAME_ECE,
            "Accept": ACCEPT,
            "Accept-Encoding": "gzip, deflate, br",
            "Ris-Application-Version": RIS_APPLICATION_VERSION
        }

        url = STATUS_URL_MERCEDES + "/v1/config"
        self.log.info("request_pin-get: url=" + url +
                      ", headers=" + json.dumps(headers, indent=4))
        response1 = self.session.get(url, headers=headers)
        self.log.info("Result request_pin get: %s", response1)

        url = STATUS_URL_MERCEDES + "/v1/login"
        d = {
             "emailOrPhoneNumber": self.username,
             "countryCode": self._country_code,
             "nonce": nonce
        }
        data = json.dumps(d)

        self.log.info("request_pin-post: url=" + url +
                      ", data=" + json.dumps(data, indent=4) +
                      ", headers=" + json.dumps(headers, indent=4))
        response = self.session.post(url, data=data, headers=headers)
        self.log.debug("Result request_pin%s", response)
        self.set_authState('pinRequested')
        return response

    # request new token set using pin
    def request_new_token_set(self, user_input=None):
        errors = {}
        nonce = self.store['nonce']
        self.set_authState('tokenRequested')
        self.store['last_pin_used'] = self.pin
        try:
            self.log.debug("calling request_access_token")
            result = self.request_access_token(self.username, self.pin, nonce)
        except Exception as error:
            errors = error
            self.log.error("Request token error: %s", errors)
        if not errors:
            self.log.debug("Token received: " + str(result))

    # authenticate: request pin and get tokens
    def authenticate(self):
        errors = {}
        nonce = str(uuid.uuid4())
        user_input = {}
        user_input["nonce"] = nonce

        try:
            self.log.debug("calling request_pin")
            response = self.request_pin(self.username, nonce)
            self.log.debug("request_pin done, response=" + str(response))
            self.log.debug("response.status_code = " + str(response.status_code))
            if response.status_code > 200:
                errors["request_pin"] = "Authentication error " + str(response.status_code)
        except Exception as error:
            errors = error
            self.log.error("Request PIN error: %s", errors)

    # request_access_token - part of 2FA process
    def request_access_token(self, email: str, pin: str, nonce: str):
        self.log.debug("enter request_access_token: email=" + email + ", pin=" + pin + ", nonce=" + nonce)
        self.method += " 3-request_access_token"
        url = TOKEN_URL
        encoded_email = urllib.parse.quote_plus(email, safe="@")

        data = (
            "client_id=" + LOGIN_APP_ID +
            "&grant_type=password&username=" + encoded_email +
            "&password=" + nonce + ":" + pin +
            "&scope=" + SCOPE
        )

        headers = {
            "X-Applicationname": X_APPLICATIONNAME_ECE,
            "Ris-Application-Version": RIS_APPLICATION_VERSION,
            "Content-Type": CONTENT_TYPE_OAUTH,
            "Stage": "prod",
            "X-Device-Id": str(uuid.uuid4()),
            "X-Request-Id": str(uuid.uuid4())
        }
        self.log.debug("request_access_token-post: url=" + url +
                       ", data=" + json.dumps(data, indent=4) +
                       ", headers=" + json.dumps(headers, indent=4))
        try:
            token_info = self.session.post(url, data=data, headers=headers)
            self.log.debug("request_access_token.status_code = " + str(token_info.status_code))
            Tokens = json.loads(token_info.text)
            if not Tokens['access_token']:
                self.log.warning("request_access_token failed")
                return None
            self.log.debug("Tokens=\n" + json.dumps(Tokens, indent=4))
            self.store['Tokens'] = Tokens

            if token_info is not None:
                ts = int(time.time())
                self.store['refresh_timestamp'] = ts
                self.store['refresh_time'] = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                self.set_authState('authenticated')
                self.write_store()
                return token_info
        except Exception as e:
            self.log.error("request_access_token exception: " + str(e))
        return None

    # refresh_token using existing refresh_token
    def refresh_token(self, refresh_token: str) -> dict:
        self.method += " 2-refresh_token"

        url = TOKEN_URL

        headers = {
            "Accept": ACCEPT,
            "User-Agent": "sOAF/202108260942 CFNetwork/978.0.7 Darwin/18.7.0",
            "Accept-Language": ACCEPT_LANGUAGE,
            "Authorization": "Bearer " + self.store['Tokens']['refresh_token'],
            "Content-Type": CONTENT_TYPE_OAUTH,
        }

        data = {'grant_type': 'refresh_token',
                'refresh_token': refresh_token}

        try:
            response = self.session.post(url,
                                         headers=headers,
                                         data=data,
                                         verify=True,
                                         allow_redirects=False,
                                         timeout=(30, 30))
            self.log.debug("refresh_token.status_code = " + str(response.status_code))
            self.log.debug("refresh_token.text = " + str(response.text))
        except Exception as e:
            self.log.error("refresh_token exception: " + str(e))
            resperr = {}
            resperr.status_code = 500
            resperr.test = str(e)
            return resperr
        return response

    # refresh access_token
    def refresh_access_token(self) -> dict:
        response = self.refresh_token(self.store['Tokens']['refresh_token'])
        self.log.debug("refresh_access_token.status_code = " + str(response.status_code))

        if response.status_code > 200:
            self.log.warning("refresh_access_token failed, start 2FA process")
            self.set_authState('init')
            return None
        else:
            self.log.debug("refresh_access_token.text = " + str(response.text))
            Tokens = json.loads(response.text)
            self.log.debug("Tokens=\n" + json.dumps(self.store['Tokens'], indent=4))

        if Tokens['access_token']:
            self.store['Tokens'] = Tokens
            ts = int(time.time())
            self.store['refresh_timestamp'] = ts
            self.store['refresh_time'] = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            self.set_authState('authenticated')
            self.write_store()
        return self.store['Tokens']['access_token']

    # get Soc of Vehicle
    def get_status(self, vin: str) -> int:
        self.method += " 1-get_status"

        url = STATUS_URL_SMART + "/seqc/v0/vehicles/" + vin + "/refresh-data"

        headers = {
            "Accept": ACCEPT,
            "Accept-Language": ACCEPT_LANGUAGE,
            "Authorization": "Bearer " + self.store['Tokens']['access_token'],
            "X-Applicationname": CLIENT_ID,
            "User-Agent": STATUS_USER_AGENT,
            "Guid": GUID
        }
        # soc = -1
        try:
            response = self.session.get(url, headers=headers, verify=SSL_VERIFY_STATUS)
            res = json.loads(response.text)
            res_json = json.dumps(res, indent=4)
            self.log.debug("get_status: result json:\n" + res_json)
            if nested_key_exists(res, 'precond', 'data', 'soc', 'value'):
                res_json = json.dumps(res['precond']['data']['soc'], indent=4)
                try:
                    soc = res['precond']['data']['soc']['value']
                    _ts = res['precond']['data']['soc']['ts']
                    self.soc_ts = datetime.datetime.fromtimestamp(_ts).strftime('%Y-%m-%d %H:%M:%S')
                    self.log.debug("get_status: result json:\n" + res_json)
                except Exception as e:
                    self.log.exception("get_status: exception0 e=" + str(e))
                    soc = -1
            elif 'error' in res and res['error'] == 'unauthorized':
                self.log.debug("get_status: access_token expired or invalid - try refresh")
                self.log.debug("get_status: error - result json:\n" + res_json)
                soc = -1
            else:
                self.log.debug("get_status: unexpected error - response.status_code:" + str(response.status_code))
                self.log.debug("get_status: unexpected error - response.text:" + response.text)
                self.log.debug("get_status: unexpected error - result json:\n" + res_json)
                soc = -1

        except Exception as e:
            self.log.error("get_status: Exception1: " + str(e))
            self.log.error("get_status: result:\n" + res_json)
            soc = -1
        if "Vehicle not found" in res_json:
            soc = -2
        return soc

    # fetch_soc: execute next step dependent on authState
    # authState: 'init'
    #            'authenticated'
    #            'pinRequested'
    #            'tokenRequested'
    #            'accessTokenExpired'
    def fetch_soc(self: str, start_ts: float) -> int:
        self.log.debug('fetch_soc/' + self.store['authState'] +
                       ': username=' + self.username +
                       ', pin=' + self.pin +
                       ', vin=' + self.vin)
        self.Soc = -1
        while self.Soc == -1:
            if self.store['authState'] == 'authenticated':
                try:
                    if 'access_token' in self.store['Tokens']:
                        self.Soc = self.get_status(self.vin)
                        if self.Soc >= 0:
                            self.log.debug("fetch_soc/authenticated: 1st attempt successful")

                    if self.Soc == -1:
                        self.set_authState('accessTokenExpired')
                        self.log.debug("fetch_soc/authenticated: get_status failed, refresh access_token ...")
                        self.store['Tokens']['access_token'] = self.refresh_access_token()
                        if self.store['authState'] == 'authenticated' and 'access_token' in self.store['Tokens']:
                            self.Soc = self.get_status(self.vin)
                            if self.Soc >= 0:
                                self.log.debug("fetch_soc/authenticated: 2nd attempt successful")
                            else:
                                self.log.warning("fetch_soc/authenticated: 2nd attempt failed - soc=" + str(self.Soc))
                        else:
                            self.log.error("fetch_soc/authenticated: refresh_access_token failed")
                            self.Soc = -1
                    elif self.Soc == -2:
                        self.log.error("fetch_soc/authenticated: failed, Vehicle not found, check VIN")
                        self.Soc = -1
                    else:
                        self.log.debug("fetch_soc/authenticated: get_status 1st attempt success")
                except Exception as e:
                    self.log.error("fetch_soc/authenticated: get_status exception, refresh_access_token ..." + str(e))
                    self.store['Tokens']['access_token'] = self.refresh_access_token()
                    if self.store['authState'] == 'authenticated' and 'access_token' in self.store['Tokens']:
                        self.Soc = self.get_status(self.vin)
                    else:
                        self.log.error("fetch_soc/authenticated: refresh_access_token failed")
                elapsed = time.time() - start_ts
                self.log.info("Lp" + self.chargepoint +
                              " SOC: " + str(self.Soc) + '%' +
                              '@' + self.soc_ts +
                              ', Elapsed: ' + str(round(elapsed, 2)) + ' s' +
                              ', Method:' + self.method)
                if self.store['Tokens'] != self.oldTokens:
                    self.log.debug("fetch_soc/authenticated: tokens changed, store token file")
                    self.write_store()

            # authState == pinRequested and pin != last_pin_used: get new token set
            if self.store['authState'] == 'pinRequested':
                self.log.debug('fetch_soc/pinRequested: old_pin = ' + self.store['last_pin_used'] + ', pin=' + self.pin)
                if self.store['last_pin_used'] != self.pin:
                    self.log.debug('fetch_soc/pinRequested: call request_new_token_set')
                    self.request_new_token_set()
                    self.write_store()
                    self.Soc = -1
                else:
                    self.log.warning('fetch_soc/pinRequested: waiting for new pin in configuration')
                    self.Soc = 0

            # authState == init: request pin
            if self.store['authState'] == 'init' or self.pin == 'neu':
                self.log.debug('fetch_soc/init: request_pin')
                self.store['nonce'] = str(uuid.uuid4())
                self.request_pin(self.username, self.store['nonce'])
                self.write_store()
                self.Soc = 0

        return self.Soc


# main program
def main():
    start_ts = time.time()
    parser = ArgumentParser()
    parser.add_argument("-v", "--vin",
                        help="VIN of vehicle", metavar="VIN", required=True)
    parser.add_argument("-u", "--user",
                        help="user", metavar="user", required=True)
    parser.add_argument("-p", "--pin",
                        help="pin", metavar="pin", required=True)
    parser.add_argument("-c", "--chargepoint",
                        help="chargepoint", metavar="chargepoint", required=True)
    args = vars(parser.parse_args())
    user_id = args['user']
    pin = args['pin']
    vin = args['vin']
    chargepoint = args['chargepoint']

    OPENWBBASEDIR = os.environ.get("OPENWBBASEDIR", "undefined")
    storeFile = OPENWBBASEDIR+'/soc_smarteq_store_lp'+chargepoint+'.json'

    Smart = smarteq(storeFile)
    Smart.set_credentials(user_id, pin)
    Smart.set_vin(vin)
    Smart.set_chargepoint(chargepoint)
    soc = Smart.fetch_soc(start_ts)
    if soc == -1:
        soc = 0
    print(soc)


if __name__ == "__main__":
    main()
