#!/usr/bin/python3

from argparse import ArgumentParser
import requests
import json
import bs4
import os
import pkce
import logging
import pickle

# Constants
BASE_URL = "https://id.mercedes-benz.com"
OAUTH_URL = BASE_URL + "/as/authorization.oauth2"
LOGIN_URL = BASE_URL + "/ciam/auth/login"
TOKEN_URL = BASE_URL + "/as/token.oauth2"
STATUS_URL = "https://oneapp.microservice.smart.com"
REDIRECT_URI = STATUS_URL
SCOPE = "openid+profile+email+phone+ciam-uid+offline_access"
CLIENT_ID = "70d89501-938c-4bec-82d0-6abb550b0825"
GUID = "280C6B55-F179-4428-88B6-E0CCF5C22A7C"
ACCEPT_LANGUAGE = "de-de"


class smarteq:
    def __init__(self, tokensFile: str):
        self.tokensFile = tokensFile
        self.log = logging.getLogger("soc_smarteq")
        debug = os.environ.get('debug', '0')
        LOGLEVEL = 'WARN'
        if debug == '1':
            LOGLEVEL = 'INFO'
        if debug == '2':
            LOGLEVEL = 'DEBUG'
        RAMDISKDIR = os.environ.get("RAMDISKDIR", "undefined")
        logFile = RAMDISKDIR+'/soc.log'
        format = '%(asctime)s %(name)s:%(levelname)s: %(message)s'
        datefmt = '%Y-%m-%d %H:%M:%S'
        logging.basicConfig(filename=logFile,
                            filemode='a',
                            format=format,
                            datefmt=datefmt,
                            level=LOGLEVEL)
        # self.log.error("init logging: debug=" + debug + ", LOGLEVEL=" + LOGLEVEL)

        self.session = requests.session()
        self.Tokens = {}
        self.code_verifier, self.code_challenge = pkce.generate_pkce_pair()
        self.code_challenge_method = "S256"

        try:
            tf = open(self.tokensFile, "rb")
            self.Tokens = pickle.load(tf)
            tf.close()
        except Exception as e:
            self.log.warn("init: loading tokens failed, file: " + self.tokensFile)
            self.Tokens = {}

    def set_credentials(self, username: str, password: str):
        self.username = username
        self.password = password

    def set_vin(self, vin: str):
        self.vin = vin

    def set_chargepoint(self, chargepoint: str):
        self.chargepoint = chargepoint

    # ===== step1 get resume ======
    def get_resume(self) -> str:
        response_type = "code"
        url1 = OAUTH_URL + '?client_id=' + CLIENT_ID + '&response_type=' + response_type + '&scope=' + SCOPE
        url1 = url1 + '&redirect_uri=' + REDIRECT_URI
        url1 = url1 + '&code_challenge=' + self.code_challenge + '&code_challenge_method=' + self.code_challenge_method
        headers1 = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": ACCEPT_LANGUAGE,
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_5_1 like Mac OS X)\
            AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
        }

        try:
            response1 = self.session.get(url1, headers=headers1)
            self.log.debug("response1.status_code = " + str(response1.status_code))
            soup = bs4.BeautifulSoup(response1.text, 'html.parser')
        
            for cd in soup.findAll(text=True):
                self.log.debug("cd= " + str(cd))
                # if isinstance(cd, bs4.CData):
                if "CDATA" in cd:
                    self.log.debug("cd.CData= " + str(cd))
                    for w in cd.split(','):
                        if w.find("const initialState = ") != -1:
                            iS = w
            if iS:
                js = iS.split('{')[1].split('}')[0].replace('\\', '').replace('\\"', '"').replace('""', '"')
                self.resume = js[1:len(js)-1].split(':')[1][2:]
            self.log.debug("Step1 get_resume: resume = " + self.resume)
        except Exception as e:
            self.log.error('Step1 get_resume Exception: ' + str(e))
        return self.resume

    # step2: login to website, return token
    def login(self) -> str:

        url3 = LOGIN_URL + "/pass"
        headers3 = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_5_1 like Mac OS X)\
            AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
            "Referer": LOGIN_URL,
            "Accept-Language": ACCEPT_LANGUAGE
        }
        d = {}
        d['username'] = self.username
        d['password'] = self.password
        d['rememberMe'] = 'true'
        data3 = json.dumps(d)

        try:
            response3 = self.session.post(url3, headers=headers3, data=data3)
            self.log.debug("response3.status_code = " + str(response3.status_code))
            # self.log.debug("response3.text = " + str(response3.text))
            if response3.status_code > 400:
                self.log.error("login: failed, status_code = " + str(response3.status_code) + ", check username/password" )
                token = ""
            else:
                result_json = json.loads(str(bs4.BeautifulSoup(response3.text, 'html.parser')))
                self.log.debug("login: result_json:\n" + json.dumps(result_json))
                token = result_json['token']
                self.log.debug("login: token = " + token)
        except Exception as e:
            self.log.error('login:  Exception: ' + str(e))
            token = ""
        return token

    # get code
    def get_code(self, token: str) -> str:
        url4 = BASE_URL + '/' + self.resume
        headers4 = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_5_1 like Mac OS X)\
            AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
            "Referer": LOGIN_URL,
            "Accept-Language": ACCEPT_LANGUAGE,
        }
        d = {}
        d['token'] = token
        data4 = json.dumps(d)

        try:
            response4 = self.session.post(url4, headers=headers4, data=data4)
            code = response4.url.split('?')[1].split('=')[1]
            self.log.debug("get_ ode, code=" + code)
        except Exception as e:
            self.log.error("get_code Exception: " + str(e))
        return code

    # get Tokens
    def get_Tokens(self, code: str) -> dict:
        url5 = TOKEN_URL
        headers5 = {
            "Accept": "*/*",
            "User-Agent": "sOAF/202108260942 CFNetwork/978.0.7 Darwin/18.7.0",
            "Accept-Language": ACCEPT_LANGUAGE,
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data5 = "grant_type=authorization_code&code=" + code + "&code_verifier=" + self.code_verifier +\
                "&redirect_uri=" + REDIRECT_URI + "&client_id=" + CLIENT_ID

        try:
            response5 = self.session.post(url5, headers=headers5, data=data5)
            self.log.debug("get_Tokens: response5.status_code = " + str(response5.status_code))
            Tokens = json.loads(response5.text)
            if not Tokens['access_token']:
                self.log.warn("get_Tokens: no access_token found")
                Tokens = {}
            else:
                self.log.debug("Tokens=\n" + json.dumps(Tokens, indent=4))
        except Exception as e:
            self.log.exception("get_Tokens: Exception: " + str(e))
        return Tokens

    # reconnect to Server
    def reconnect(self) -> dict:
        token = self.login()
        if token == "":
            self.log.error("reconnect: Login failed")
            return {}

        code = self.get_code(token)
        Tokens = self.get_Tokens(code)

        tf = open(self.tokensFile, "wb")
        pickle.dump(Tokens, tf)
        tf.close()

        return Tokens

    # get Soc of Vehicle
    def get_status(self, vin: str) -> int:
        url7 = STATUS_URL + "/seqc/v0/vehicles/" + vin +\
               "/init-data?requestedData=BOTH&countryCode=DE&locale=de-DE"
        headers7 = {
            "accept": "*/*",
            "accept-language": "de-DE;q=1.0",
            "authorization": "Bearer " + self.Tokens['access_token'],
            "x-applicationname": CLIENT_ID,
            "user-agent": "Device: iPhone 6; OS-version: iOS_12.5.1; App-Name: smart EQ control; App-Version: 3.0;\
            Build: 202108260942; Language: de_DE",
            "guid": GUID
        }

        try:
            response7 = self.session.get(url7, headers=headers7)
            res7 = json.loads(response7.text)
            res7s = json.dumps(res7, indent=4)
            res7s = json.dumps(res7['precond']['data']['soc'], indent=4)
            try:
                soc = res7['precond']['data']['soc']['value']
                self.log.info("get_status: result json:\n" + res7s)
            except:
                soc = -1
                pass
        except Exception as e:
            self.log.error("get_status: Exception: " + str(e))
            self.log.error("get_status: result json:\n" + res7s)
            soc = -1
        if "Vehicle not found" in res7s:
            soc = -2
        return soc

    def fetch_soc(self) -> int:
        soc = -1
        try:
            try:
                if self.Tokens['access_token']:
                    soc = self.get_status(self.vin)
                    self.log.info("fetch_soc: 1st attempt successful - skip reconnect")
            except Exception as e:
                soc = -1
                pass

            if soc == -1:
                self.log.info("fetch_soc: (re)connecting ...")
                self.resume = self.get_resume()
                self.Tokens = self.reconnect()
                if self.Tokens:
                    soc = self.get_status(self.vin)
                else:
                    self.log.error("fetch_soc: (re-)connect failed")
                    soc = 0
            elif soc == -2:
                self.log.error("fetch_soc: failed, Vehicle not found, check VIN")
                soc = 0
                pass

        except Exception as e:
            self.log.error("fetch_soc: exception, (re-)connecting ..." + str(e))
            self.resume = self.get_resume()
            self.Tokens = self.reconnect()
            soc = self.get_status(self.vin)
        self.log.info("fetch_soc: result: soc=" + str(soc) + '%')
        return soc


# main program
def main():
    parser = ArgumentParser()
    parser.add_argument("-v", "--vin",
                        help="VIN of vehicle", metavar="VIN", required=True)
    parser.add_argument("-u", "--user",
                        help="user", metavar="user", required=True)
    parser.add_argument("-p", "--password",
                        help="password", metavar="password", required=True)
    parser.add_argument("-c", "--chargepoint",
                        help="chargepoint", metavar="chargepoint", required=True)
    args = vars(parser.parse_args())
    user_id = args['user']
    password = args['password']
    vin = args['vin']
    chargepoint = args['chargepoint']

    OPENWBBASEDIR = os.environ.get("OPENWBBASEDIR", "undefined")
    RAMDISKDIR = os.environ.get("RAMDISKDIR", "undefined")
    tokensFile = RAMDISKDIR+'/soc_smarteq_tokens_lp'+chargepoint

    Smart = smarteq(tokensFile)
    Smart.set_credentials(user_id, password)
    Smart.set_vin(vin)
    Smart.set_chargepoint(chargepoint)
    soc = Smart.fetch_soc()
    print(soc)


if __name__ == "__main__":
    main()
