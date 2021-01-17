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
        self.device_infos = {}
        try:
            with open('ramdisk/smarthomehandlerloglevel', 'r') as value:
                self.loglevel = int(value.read())
        except:
            self.loglevel=2

    # cacheFileString returns the filename in which the device dictionary is cached
    def cacheFileString(self):
        return '/var/www/html/openWB/ramdisk/smarthome_device_' + str(self.devicenumber) + '_avmdeviceinfos'

    # sessionIDFile returns the filename in which the session ID is stored
    def sessionIDFile(self):
        return '/var/www/html/openWB/ramdisk/smarthome_device_' + str(self.devicenumber) + '_sessionid'

    # connect checks the currently known session ID for validity and
    # performs an authentication to obtain a new session ID if neccessary.
    # The session ID is assumed to be valid if it has been written to the
    # ramdisk less than 5 minutes ago.
    def connect(self):
        file_stringsessionid = self.sessionIDFile()
        # try to read previous session id from ramdisk file. If this operation fails,
        # no harm is done as we can proceed with normal authentication. Reusing
        # a session ID (which is valid up to 60 minutes) saves some time, though.
        try:
            if os.path.isfile(file_stringsessionid):
                f = open(file_stringsessionid, 'r')
                self.sessionID = f.read().strip()
                f.close()
                mtime = os.path.getmtime(file_stringsessionid)
                age_of_id_in_seconds = time.time() - mtime
                should_authenticate = age_of_id_in_seconds / 60 >= 5
            else:
                should_authenticate = True
        except IOError:
            should_authenticate = True

        if should_authenticate:
            self.logMessage(0, "(re-)authenticate at fritzbox")
            # perform authentication
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
                print ('%s' % (self.sessionID),file = f)
                f.close()
            except IOError:
                pass

    # logMessage writes a message to the logfile for the smarthome device.
    def logMessage(self, level, message):
        if level < self.loglevel:
            return
        named_tuple = time.localtime() # getstruct_time
        time_string = time.strftime("%Y-%m-%d, %H:%M:%S", named_tuple)
        logfile_string = '/var/www/html/openWB/ramdisk/smarthome.log'
        try:
            if os.path.isfile(logfile_string):
                f = open( logfile_string , 'a')
            else:
                f = open( logfile_string , 'w') 
            print ('%s Device %s: AVMHomeAutomation (actor name:%s) %s' % (time_string, self.devicenumber, self.switchname, message), file = f)
            f.close()
        except IOError:
            pass

    # readOfBuildDeviceInfoCache fills self.device_infos, either from a cached
    # file of maximum age 5 minutes, or by fetching the info from the fritzbox.
    # The main purpose of this cache is to skip looking up the AIN via network
    # every time.
    def readOrBuildDeviceInfoCache(self):
        file_stringdeviceinfos = self.cacheFileString()
        try:
            if os.path.isfile(file_stringdeviceinfos):
                f = open(file_stringdeviceinfos, 'r')
                self.device_infos = json.loads(f.read().strip())
                f.close()
                mtime = os.path.getmtime(file_stringdeviceinfos)
                age_of_id_in_seconds = time.time() - mtime
                should_fetch = age_of_id_in_seconds / 60 >= 5
            else:
                should_fetch = True
        except IOError:
            should_fetch = True
        except:
            self.logMessage(2, "unexpected error: %s" % (sys.exc_info()[0]))

        if should_fetch:
            self.fetchAndCacheDeviceInfos()

    def fetchAndCacheDeviceInfos(self):
        self.device_infos = getDevicesDict(self.baseURL, self.sessionID)
        try:
            f = open(self.cacheFileString(), 'w')
            print ('%s' % (json.dumps(self.device_infos)), file = f)
            f.close()
        except IOError as e:
            pass
            self.logMessage(2, "error writing power result %s" % (e))
        except:
            self.logMessage(2, "unexpected error: %s" % (sys.exc_info()[0]))


    # switchDevice sets the relais of the AVM Home Automation actor
    # state parameter: true -> on, false -> off
    def switchDevice(self, state):
        if state:
            cmd = "setswitchon"
        else:
            cmd = "setswitchoff"
        self.logMessage(1, cmd)


        if not self.switchname in self.device_infos:
            # try updating the info, first
            self.readOrBuildDeviceInfoCache()

        if not self.switchname in self.device_infos:
            # still not found -> bail out
            self.logMessage(2, "no such device found at fritzbox: %s" % (self.switchname))
            return

        switch = self.device_infos[self.switchname]
        ain = urllib.parse.quote(switch["ain"])

        commandURL = self.baseURL + \
            "/webservices/homeautoswitch.lua?" + \
            "sid=" + self.sessionID + \
            "&switchcmd=" + cmd + \
            "&ain=" + ain
        urllib.request.urlopen(commandURL, timeout = 5)

    # getActualPowerForce returns current observed power and the state of the switch relais.
    # The JSON answer is either written to the according smarthome device return file
    # or dumped to stdout if no such file exists (for local development)
    def getActualPower(self):
        self.logMessage(0, "fetch power")

        self.fetchAndCacheDeviceInfos()
        if not self.switchname in self.device_infos:
            self.logMessage(2, "no such device found at fritzbox: %s" % (self.switchname))
            return

        try:
            switch = self.device_infos[self.switchname]
            aktpower = switch['power']
            powerc = switch['energy']

            if switch['state']:
                relais = 1
            else:
                relais = 0
            answer = '{"power":' + str(aktpower) + ',"powerc":' + str(powerc) + ',"on":' + str(relais) + '}'
        except:
            self.logMessage(2, "Unexpected error: %s" % (sys.exc_info()[0]))

        try:
            f1 = open('/var/www/html/openWB/ramdisk/smarthome_device_ret' + str(self.devicenumber), 'w')
            json.dump(answer, f1)
            f1.close()
        except IOError as e:
            self.logMessage(2, "error writing power result %s" % (e))
            print(answer) # dump answer to stdout if file cannot be written
        except:
            self.logMessage(2, "unexpected error: %s" % (sys.exc_info()[0]))

