#!/usr/bin/python3
import sys
import os
import time
import json
import urllib.request
import hashlib
import credentials
import xml.etree.ElementTree as ET

def getAVMSessionID(
        baseurl, 
        password,
        username, 
        previoussessionid="0000000000000000",
        ):

    # fallback for storing password and credentials locally
    if username == '':
        username = credentials.username
    if password == '':
        password = credentials.password
        
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

def getDevicesDict(baseurl, sessionid):
    getdevicelistinfosurl = baseurl + "/webservices/homeautoswitch.lua?sid="+sessionid+"&switchcmd=getdevicelistinfos"
    getdevicelistinfosResponseBody = str(urllib.request.urlopen(getdevicelistinfosurl).read(), "utf-8").strip()
    devicelistinfos = ET.fromstring(getdevicelistinfosResponseBody)
    deviceNames = {}
    for device in devicelistinfos:
        name = device.find("name").text
        ain = device.attrib["identifier"]
        powermeter = device.find("powermeter")
        power = float(powermeter.find("power").text)/1000.0
        voltage = float(powermeter.find("voltage").text)/1000.0
        energy = powermeter.find("energy").text
        deviceNames[name] = {'ain': ain, 'power': power, 'voltage': voltage, 'energy': energy}
        temperatureBlock = device.find("temperature")
        if temperatureBlock != None:
            deviceNames['temperature'] = float(temperatureBlock.find("celsius").text)/10.0 
    return deviceNames
