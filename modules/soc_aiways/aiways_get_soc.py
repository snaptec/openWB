'''
Created on 03.01.2022

@author: eddi
'''

#!/usr/bin/env python

# Script to emulate Aiways login and get SoC.
# Author  : Eddi
# Version : 1.0
# Date    : 09.01.2022


import requests
import argparse
import json
import hashlib
import logging


CS_URL = "https://coiapp-api-eu.ai-ways.com:10443/"
language = "de"
version = "1.1.0"
platform = "android"
deviceid = ""
apptimezone = "GMT+02:00"
apptimezoneid = "Europe/Berlin"
#debug = False
debuglevel = 0

if __name__ == "__main__":

    # parse arguments
    parser = argparse.ArgumentParser(description='Control your Connected Aiways.')
    parser.add_argument('-a', '--account', required=True, help='Your Aiways App Account')
    parser.add_argument('-p', '--password',help='Your Aiways App password.')
    parser.add_argument('-v', '--vin', help='Your car VIN')
    parser.add_argument('-d', '--debuglevel', help='openWB Debuglevel', type = int)
    #parser.add_argument('-d', '--debug', action="store_true", help='Show debug commands.')
    args = parser.parse_args()
    account = args.account
    password = args.password
    vin = args.vin
    debuglevel = args.debuglevel
    #if args.debug:
    #    debug = True
    if debuglevel > 0: logging.basicConfig(filename='/var/log/openWB.log', format='%(asctime)s %(levelname)-8s %(name)-12s %(message)s', level=logging.DEBUG)
    else: logging.basicConfig(filename='/var/log/openWB.log', format='%(asctime)s %(levelname)-8s %(name)-12s %(message)s', level=logging.ERROR)
    #else: logging.basicConfig(filename='/var/log/openWB.log', format='%(asctime)s %(message)s', level=logging.ERROR)
    
    logger = logging.getLogger("aiways_get_soc.py")
    
    ############################################################# 
    # Request1: aiways-passport-service/passport/login/password #
    # Login with accountname and password                       #
    # Also here we get the value for "token"                    #
    # This value is changing for each session                   #
    #############################################################
    

    PATH = "aiways-passport-service/passport/login/password"
    
    headers = {
        "apptimezone": apptimezone,
        "apptimezoneid": apptimezoneid,
        "content-type": "application/json; charset=utf-8",
        "content-length": "65",
        "accept-encoding": "gzip",
        "user-agent": "okhttp/4.3.1"
    }
    
    encoded=password.encode()
    passwordmd5 = hashlib.md5(encoded)
    
    LOGIN_PAYLOAD = {"account":account,"password":passwordmd5.hexdigest()}
    
    resp = requests.post(CS_URL + PATH, headers=headers, data = json.dumps(LOGIN_PAYLOAD))
    
    
    logger.debug(resp.status_code)
    logger.debug(resp.content)
    
    data = resp.json()["data"]
    token = data["token"]
    userId = data["userId"]
    

    
    #########################################################################
    # Request2 "app/vc/getCondition"                                        #
    # Get the current Condition of the car                                  #
    # The data are located in data/vc                                       #
    # "soc" contains the value for the current State of Charge)             #
    #########################################################################
     
    PATH = "app/vc/getCondition"
    
    headers = {
        "token": token,
        "apptimezone": apptimezone,
        "apptimezoneid": apptimezoneid,
        "content-type": "application/json; charset=utf-8",
        "content-length": "54",
        "accept-encoding": "gzip",
        "user-agent": "okhttp/4.3.1"
    }
    
    PAYLOAD = {'userId': userId,'vin': vin}
    
    resp = requests.post(CS_URL + PATH, headers=headers, data = json.dumps(PAYLOAD))
    
    logger.debug(resp.status_code)
    logger.debug(resp.content)
    
    data = resp.json()["data"]
    vc = data["vc"]
    soc = vc["soc"]
    chargeSts = vc["chargeSts"]
    print (soc)
    logger.info("SoC erfolgreich ermittelt: " + soc + "%")
    
    #########################################################################
    # Request3 "aiways-passport-service/passport/logout"                    #
    # Makes a logout                                                        #
    #########################################################################

    PATH = "aiways-passport-service/passport/logout"
    
    headers = {
     
        "token": token,
        "apptimezone": apptimezone,
        "apptimezoneid": apptimezoneid,
        "accept-encoding": "gzip",
        "user-agent": "okhttp/4.3.1"
    }

    resp = requests.get(CS_URL + PATH, headers=headers)

    logger.debug(resp.status_code)
    logger.debug(resp.content)
    
