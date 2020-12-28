#!/usr/bin/python3
import sys
import os
import time
import json
import urllib.request
import hashlib
import xml.etree.ElementTree as ET

def getAVMSessionID(
        baseurl, 
        password,
        username, 
        previoussessionid="0000000000000000",
        ):
    loginurl = baseurl + '/login_sid.lua'
    challengeURL = loginurl + "?sid="+previoussessionid
    challengeResponse = ET.fromstring(urllib.request.urlopen(loginurl, timeout=5).read())
    sessionid = challengeResponse.find('SID').text
    if sessionid != "0000000000000000":
        # We already had valid session id, so return directly
        return sessionid
    challenge = challengeResponse.find('Challenge').text
    m = hashlib.md5()
    m.update((challenge + "-" + password).encode('utf-16le'))
    hashedPassword = m.hexdigest()
    dataDict = {
            'username': username,
            'response': challenge + "-" + hashedPassword
            }
    data = urllib.parse.urlencode(dataDict).encode()
    # with data parameter, the request will be of HTTP method POST
    loginRequest = urllib.request.Request(loginurl, data=data)
    loginResponseBody = urllib.request.urlopen(loginRequest, timeout=5).read()
    sessioninfo = ET.fromstring(loginResponseBody)
    sessionid = sessioninfo.find('SID').text
    return sessionid
