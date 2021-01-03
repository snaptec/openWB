#!/usr/bin/python3
import sys
import os
import time
import json
import urllib.request
import hashlib
import credentials
import xml.etree.ElementTree as ET

# getAVMSessionID retrieves a session ID for issuing commands to a FRITZ!Box webinterface.
# See https://avm.de/fileadmin/user_upload/Global/Service/Schnittstellen/Session-ID_deutsch_13Nov18.pdf for a description of the challenge-response-method.
def getAVMSessionID(
        baseurl, 
        password,
        username, 
        previoussessionid = "0000000000000000",
        ):

    # fallback for storing password and credentials locally
    if username == '':
        username = credentials.username
    if password == '':
        password = credentials.password
        
    loginurl = baseurl + '/login_sid.lua'
    challengeURL = loginurl + "?sid="+previoussessionid
    challengeResponse = ET.fromstring(urllib.request.urlopen(loginurl, timeout = 5).read())
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
    loginRequest = urllib.request.Request(loginurl, data = data)
    loginResponseBody = urllib.request.urlopen(loginRequest, timeout = 5).read()
    sessioninfo = ET.fromstring(loginResponseBody)
    sessionid = sessioninfo.find('SID').text
    return sessionid

# getDevicesDict returns a dictionary that maps defined actor names to its
# unique hardware ID (called "AIN": "Actuator Identification Number") and
# current values for the power, voltage, integraded energy, temperature (not
# for group actors).
def getDevicesDict(baseurl, sessionid):
    getdevicelistinfosurl = baseurl + "/webservices/homeautoswitch.lua?sid="+sessionid+"&switchcmd=getdevicelistinfos"
    getdevicelistinfosResponseBody = str(urllib.request.urlopen(getdevicelistinfosurl).read(), "utf-8").strip()
    devicelistinfos = ET.fromstring(getdevicelistinfosResponseBody)
    deviceNames = {}
    for device in devicelistinfos:
        name = device.find("name").text
        ain = device.attrib["identifier"]
        powermeter = device.find("powermeter")
        power = float(powermeter.find("power").text)/1000.0 # AVM returns mW, convert to W here
        voltage = float(powermeter.find("voltage").text)/1000.0 # AVM returns mV, convert to V here
        energy = powermeter.find("energy").text # AVM returns Wh
        deviceNames[name] = {'ain': ain, 'power': power, 'voltage': voltage, 'energy': energy}
        temperatureBlock = device.find("temperature")
        if temperatureBlock != None:
            deviceNames[name]['temperature'] = float(temperatureBlock.find("celsius").text)/10.0 
        switchBlock = device.find("switch")
        if switchBlock != None:
            if int(switchBlock.find("state").text) == 1:
                deviceNames[name]['state'] = True
            else:
                deviceNames[name]['state'] = False
    return deviceNames

class AVMHomeAutomation:
    # Parse configuration from command line arguments as proviced by /runs/smarthomehandler.py
    def __init__(self):
        self.devicenumber = str(sys.argv[1])
        self.baseURL = "http://" + str(sys.argv[2]) # IP or hostname (e.g. "fritz.box")
        self.switchname = str(sys.argv[5])
        self.username = str(sys.argv[6])
        self.password = str(sys.argv[7])
        self.sessionID = ""

    # connect checks the currently known session ID for validity and
    # performs an authentication to obtain a new session ID if neccessary
    def connect(self):
        file_stringsessionid = '/var/www/html/openWB/ramdisk/smarthome_device_' + str(self.devicenumber) + '_sessionid'

        # try to read previous session id from ramdisk file. If this operation fails,
        # no harm is done as we can proceed with normal authentication. Reusing
        # a session ID (which is valid up to 60 minutes) saves some time, though.
        try:
            if os.path.isfile(file_stringsessionid):
                f = open(file_stringsessionid, 'r')
                self.sessionID = f.read()
                f.close()
        except IOError:
            pass

        # perform login
        self.sessionID = getAVMSessionID(
                self.baseURL,
                previoussessionid = self.sessionID,
                username = self.username,
                password = self.password)

        # Try to store potentially new session id to ramdisk for next run
        # If this operations fails, no harm is done as we can always authenticate
        # with username/password.
        try:
            f = open(file_stringsessionid, 'w')
            print ('%s' % (sessionid),file = f)
            f.close()
        except IOError:
            pass

    # logAction writes a message to the logfile for the smarthome device.
    def logAction(self, action):
        named_tuple = time.localtime() # getstruct_time
        time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
        logfile_string = '/var/www/html/openWB/ramdisk/smarthome_device_' + str(self.devicenumber) + '_avmhomeautomation.log'
        try:
            if os.path.isfile(logfile_string):
                f = open( logfile_string , 'a')
            else:
                f = open( logfile_string , 'w') 
                print ('%s devicenr %s avmhomeautomation %s' % (time_string, self.devicenumber, action),file = f)
                f.close()
        except IOError:
            pass


    # switchDevice sets the relais of the AVM Home Automation actor
    # state parameter: true -> on, false -> off
    def switchDevice(self, state):
        if state:
            cmd = "setswitchon"
        else:
            cmd = "setswitchoff"
        self.logAction(cmd)

        switch = getDevicesDict(self.baseURL, self.sessionID)[self.switchname]
        ain = urllib.parse.quote(switch["ain"])

        commandURL = self.baseURL + \
            "/webservices/homeautoswitch.lua?" + \
            "sid=" + self.sessionID + \
            "&switchcmd=" + cmd + \
            "&ain=" + ain
        urllib.request.urlopen(commandURL, timeout = 5)

    # getActualPower returns current observed power and the state of the switch relais.
    # The JSON answer is either written to the according smarthome device return file
    # or dumped to stdout if no such file exists (for local development)
    def getActualPower(self):
        self.logAction("fetch power")

        switch = getDevicesDict(self.baseURL, self.sessionID)[self.switchname]
        aktpower = switch['power']
        powerc = switch['energy']

        if switch['state']:
            relais = 1
        else:
            relais = 0
        answer = '{"power":' + str(aktpower) + ',"powerc":' + str(powerc) + ',"on":' + str(relais) + '} '
        try:
            f1 = open('/var/www/html/openWB/ramdisk/smarthome_device_ret' + str(self.devicenumber), 'w')
            json.dump(answer, f1)
            f1.close()
        except IOError:
            print(answer) # dump answer to stdout if file cannot be written

