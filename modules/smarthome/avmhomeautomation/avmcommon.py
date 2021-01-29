#!/usr/bin/python3
import sys
import os
import time
import json
import urllib.request
import hashlib
import credentials
import xml.etree.ElementTree as ET

INVALID_SESSIONID =  "0000000000000000"
CACHEFILE = "/var/www/html/openWB/ramdisk/smarthome_avmautomation_cache"

class AVMHomeAutomation:
    # Parse configuration from command line arguments as proviced by /runs/smarthomehandler.py
    def __init__(self):
        self.devicenumber = str(sys.argv[1])
        self.host = str(sys.argv[2]) # IP or hostname (e.g. "fritz.box")
        self.switchname = str(sys.argv[5])
        self.username = str(sys.argv[6])
        self.password = str(sys.argv[7])
        self.baseURL = "http://" + self.host
        self.sessionID = ""
        self.device_infos = {}
        m = hashlib.sha256()
        m.update(self.password.encode('utf-8'))
        m.hexdigest()
        self.cacheKey = "%s:%s@%s" % (self.username, m.hexdigest(), self.host)
        try:
            with open('ramdisk/smarthomehandlerloglevel', 'r') as value:
                self.loglevel = int(value.read())
        except:
            self.loglevel=2

        self.cache = {}
        if os.path.isfile(CACHEFILE):
            self.logMessage(0, "found an AVM cache file, trying to load")
            try:
                f = open(CACHEFILE, 'r')
                self.cache = json.loads(f.read().strip())
                f.close()
            except Exception as e:
                self.logMessage(0, "unable to load cache file: %s" % (e))

    def cachedOwnInfo(self):
        key = self.cacheKey
        if key in self.cache:
            return self.cache[key]
        return {}

    def writeCacheToRamdisk(self):
        cacheToWrite = {}
        for login in self.cache:
            if "session_mtime" in self.cache[login]:
                mtime = self.cache[login]["session_mtime"]
                age = time.time() - mtime
                if age > 450:
                    self.logMessage(0, "removing stale cache for %s (%.1fs old)" % (login, age))
                else:
                    cacheToWrite[login] = self.cache[login]
        try:
            f = open(CACHEFILE, 'w')
            json.dump(cacheToWrite, f)
            f.close()
        except Exception as e:
            self.logMessage(0, "unable to write cache file: %s" % (e))

    # getAVMSessionID retrieves a session ID for issuing commands to a
    # FRITZ!Box webinterface. See
    # https://avm.de/fileadmin/user_upload/Global/Service/Schnittstellen/Session-ID_deutsch_13Nov18.pdf
    # for a description of the challenge-response-method.
    def getAVMSessionID(self):
        # fallback for storing password and credentials locally
        if self.username == '':
            self.username = credentials.username
        if self.password == '':
            self.password = credentials.password

        self.logMessage(0, "checking existing sessionID: %s" % (self.sessionID))
        loginurl = self.baseURL + '/login_sid.lua'
        challengeURL = loginurl + "?sid="+self.sessionID
        challengeResponse = ET.fromstring(urllib.request.urlopen(loginurl, timeout = 5).read())
        sessionid = challengeResponse.find('SID').text
        if sessionid != INVALID_SESSIONID:
            # We already had valid session id, so return directly
            self.logMessage(0, "last sessionID was accepted as valid")
            self.sessionID = sessionid
            return
        blockTimeXML = challengeResponse.find('BlockTime')
        if blockTimeXML != None and int(blockTimeXML.text) > 0:
            self.logMessage(2, "Durch Anmeldefehler in der Vergangenheit ist der Zugang zur FRITZ!Box noch fuer %s Sekunden gesperrt." % (blockTimeXML.text))
            self.errorListCredentials()
            self.sessionID = INVALID_SESSIONID
            return
        self.logMessage(0, "last sessionID was invalid, performing new challenge-response authentication")
        challenge = challengeResponse.find('Challenge').text
        self.logMessage(0, "challenge: %s" % (challenge))
        m = hashlib.md5()
        m.update((challenge + "-" + self.password).encode('utf-16le'))
        hashedPassword = m.hexdigest()
        dataDict = {
                'username': self.username,
                'response': challenge + "-" + hashedPassword
                }
        data = urllib.parse.urlencode(dataDict).encode()
        self.logMessage(0, "response: %s" % (dataDict))
        # with data parameter, the request will be of HTTP method POST
        try:
            loginRequest = urllib.request.Request(loginurl, data = data)
            loginResponseBody = urllib.request.urlopen(loginRequest, timeout = 5).read()
            sessioninfo = ET.fromstring(loginResponseBody)
            sessionid = sessioninfo.find('SID').text
            self.sessionID = sessionid
        except BaseException as e:
            self.logMessage(2, "error completing auth: %s" % (e))
        if self.sessionID == INVALID_SESSIONID:
            blockTime = sessioninfo.find('BlockTime').text
            self.logMessage(2, "Anmeldung fehlgeschlagen, bitte Nutzernamen und Passwort ueberpruefen. Anmeldung fuer die naechsten %s Sekunden durch FRITZ!Box-Webinterface gesperrt." % (blockTime))
            self.errorListCredentials()

    def errorListCredentials(self):
        errorMessage = "Folgende Anmeldungen sind im System bekannt: "
        for login in self.cache:
            errorMessage += "%s " % (login)
        self.logMessage(2, errorMessage)


    # connect checks the currently known session ID for validity and performs
    # an authentication to obtain a new session ID if neccessary. A session ID
    # is assumed to be recent enough if it has been obtained ramdisk less than
    # 5 minutes ago in which case it is reused.
    def connect(self): 
        should_authenticate = True
        ownInfo = self.cachedOwnInfo()
        if "session_mtime" in ownInfo and "session_id" in ownInfo:
            self.sessionID = ownInfo["session_id"]
            mtime = ownInfo["session_mtime"]
            age_of_id_in_seconds = time.time() - mtime
            should_authenticate = self.sessionID == INVALID_SESSIONID or age_of_id_in_seconds >= 5 * 60

        if should_authenticate:
            self.logMessage(0, "(re-)authenticate at FRITZ!Box, old sessionID: %s" % (self.sessionID))
            try:
                self.getAVMSessionID()
            except Exception as e:
                self.logMessage(2, "unexpected error while negotiating session id: %s" % (e))
                self.sessionID = INVALID_SESSIONID
            self.logMessage(0, "retrieved sessionID from FRITZ!Box: %s" % (self.sessionID))

            # Try to store potentially new session id to ramdisk for next run
            # If this operations fails, no harm is done as we can always authenticate
            # with username/password.
            if not self.cacheKey in self.cache: 
                self.cache[self.cacheKey] = {}
            self.cache[self.cacheKey]["session_mtime"] = time.time()
            self.cache[self.cacheKey]["session_id"] = self.sessionID
            self.writeCacheToRamdisk()

    # logMessage writes a message to the logfile for the smarthome device.
    def logMessage(self, level, message):
        if level < self.loglevel:
            return
        now = time.localtime() # getstruct_time
        time_string = time.strftime("%Y-%m-%d %H:%M:%S", now)
        logfile_string = '/var/www/html/openWB/ramdisk/smarthome.log'
        try:
            if os.path.isfile(logfile_string):
                f = open( logfile_string , 'a')
            else:
                f = open( logfile_string , 'w') 
            prefix = ""
            if level == 0:
                prefix = "[DEBUG] "
            if level == 1:
                prefix = "[INFO] "
            if level == 2:
                prefix = "[ERROR] "
            print ('%s: (%s) AVM (actor: %s) %s%s' % (time_string, self.devicenumber, self.switchname, prefix, message), file = f)
            f.close()
        except IOError:
            pass


    # getDevicesDict returns a dictionary that maps defined actor names to its
    # unique hardware ID (called "AIN": "Actuator Identification Number") and
    # current values for the power, voltage, integraded energy, temperature (not
    # for group actors).
    def getDevicesDict(self):
        getDeviceListInfosURL = self.baseURL + "/webservices/homeautoswitch.lua?sid="+self.sessionID+"&switchcmd=getdevicelistinfos"
        try:
            getDeviceListInfosResponseBodyRaw = urllib.request.urlopen(getDeviceListInfosURL, timeout = 5).read()
            getDeviceListInfosResponseBody = str(getDeviceListInfosResponseBodyRaw, "utf-8").strip()
            deviceListElementTree = ET.fromstring(getDeviceListInfosResponseBody)
        except BaseException as e:
            self.logMessage(2, "error while requesting device infos from FRITZ!Box:" % (e))
            self.device_infos = {}
            return
        next_device_infos = {}
        try:
            for device in deviceListElementTree:
                name = device.find("name").text
                ain = device.attrib["identifier"]
                next_device_infos[name] = {'ain': ain}

                hkrBlock = device.find("hkr")
                if hkrBlock != None:
                    next_device_infos[name]['is_thermostat'] = True
                else:
                    next_device_infos[name]['is_thermostat'] = False

                powermeterBlock = device.find("powermeter")
                if powermeterBlock != None:
                    # AVM returns mW, convert to W here
                    next_device_infos[name]['power'] = float(powermeterBlock.find("power").text)/1000.0
                    # AVM returns mV, convert to V here
                    next_device_infos[name]['voltage'] = float(powermeterBlock.find("voltage").text)/1000.0
                    # AVM returns Wh
                    next_device_infos[name]['energy'] = powermeterBlock.find("energy").text 

                temperatureBlock = device.find("temperature")
                if temperatureBlock != None:
                    # AVM returns tenths of degrees Celsius
                    next_device_infos[name]['temperature'] = float(temperatureBlock.find("celsius").text)/10.0 

                switchBlock = device.find("switch")
                if switchBlock != None:
                    if int(switchBlock.find("state").text) == 1:
                        next_device_infos[name]['state'] = True
                    else:
                        next_device_infos[name]['state'] = False
        except BaseException as e:
            self.logMessage(2, "unable to parse device infos: %s" % (e))
        self.device_infos = next_device_infos


    # readOrBuildDeviceInfoCache fills self.device_infos, either from cached
    # values (if more recent than 5 seconds), or by fetching the info from the FRITZ!Box.
    # The main purpose of this cache is to skip looking up the AIN via network
    # every time.
    def readOrBuildDeviceInfoCache(self):
        self.logMessage(0, "start of readOrBuildDeviceInfoCache")
        should_fetch = True
        ownInfo = self.cachedOwnInfo()
        if "device_infos_mtime" in ownInfo and "device_infos" in ownInfo:
            self.device_infos = ownInfo["device_infos"]
            mtime = ownInfo["device_infos_mtime"]
            age_of_infos_in_seconds = time.time() - mtime
            self.logMessage(0, "age of cached device infos: %.1f seconds" % (age_of_infos_in_seconds))
            should_fetch = self.device_infos == INVALID_SESSIONID or age_of_infos_in_seconds >= 5

        self.logMessage(0, "should fetch new info from FRITZ!Box: %s" % (should_fetch))
        if should_fetch:
            self.logMessage(0, "fetching device info for all devices from FRITZ!Box")
            try:
                self.getDevicesDict()
            except:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                self.logMessage(2, "unexpected error during getDevicesDict: %s %s %s" % (exc_type, fname, exc_tb.tb_lineno))
            self.logMessage(0, "device info fetched: %s" % (self.device_infos))
            if self.sessionID != INVALID_SESSIONID:
                if not self.cacheKey in self.cache: 
                    self.cache[self.cacheKey] = {}
                self.cache[self.cacheKey]["device_infos_mtime"] = time.time()
                self.cache[self.cacheKey]["device_infos"] = self.device_infos
                self.writeCacheToRamdisk()
                self.logMessage(0, "written device infos to ramdisk cache")
        else:
            self.logMessage(0, "using cached device infos from ramdisk")

        self.logMessage(0, "end of readOrBuildDeviceInfoCache")


    # switchDevice sets the relais of the AVM Home Automation actor
    # state parameter: true -> on, false -> off
    def switchDevice(self, state):
        if self.sessionID == INVALID_SESSIONID:
            self.logMessage(2, "Kann ohne valide Anmeldung nicht schalten.")
            return
        self.logMessage(0, "start of switchDevice")
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
            self.logMessage(2, "no such device found at FRITZ!Box: %s" % (self.switchname))
            return

        switch = self.device_infos[self.switchname]
        ain = urllib.parse.quote(switch["ain"])

        commandURL = self.baseURL + \
            "/webservices/homeautoswitch.lua?" + \
            "sid=" + self.sessionID + \
            "&switchcmd=" + cmd + \
            "&ain=" + ain
        urllib.request.urlopen(commandURL, timeout = 5)
        self.logMessage(0, "end of switchDevice")


    # getActualPowerForce returns current observed power and the state of the switch relais.
    # The JSON answer is either written to the according smarthome device return file
    # or dumped to stdout if no such file exists (for local development)
    def getActualPower(self):
        if self.sessionID == INVALID_SESSIONID:
            self.logMessage(2, "Kann ohne valide Anmeldung keine neuen Daten holen.")
            return
        self.logMessage(0, "start of getActualPower")
        self.readOrBuildDeviceInfoCache()
        if not self.switchname in self.device_infos:
            self.logMessage(2, "no such device found at FRITZ!Box: %s" % (self.switchname))
            return

        try:
            switch = self.device_infos[self.switchname]
            if 'power' in switch:
                aktpower = switch['power']
            else:
                aktpower = 0
                self.logMessage(2, "device does not provide power measurement, falling back to 0")
            if 'energy' in switch:
                powerc = switch['energy']
            else:
                powerc = 0
                self.logMessage(2, "device does not provide energy measurement, falling back to 0")
            if 'state' in switch:
                if switch['state']:
                    relais = 1
                else:
                    relais = 0
            else:
                self.logMessage(2, "device does not provider switch state, falling back to OFF")
                relais = 0
            answer = '{"power":' + str(aktpower) + ',"powerc":' + str(powerc) + ',"on":' + str(relais) + '}'
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.logMessage(2, "unexpected error getActualPower build JSON string: %s %s %s" % (exc_type, fname, exc_tb.tb_lineno))

        self.logMessage(0, "constructed JSON answer: %s" % (answer))
        outFileString ='/var/www/html/openWB/ramdisk/smarthome_device_ret' + str(self.devicenumber);
        self.logMessage(0, "handing answer back to smarthomehandler via %s" % (outFileString))
        try:
            f1 = open(outFileString, 'w')
            json.dump(answer, f1)
            f1.close()
        except IOError as e:
            self.logMessage(2, "error writing power result %s" % (e))
            print(answer) # dump answer to stdout if file cannot be written
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.logMessage(2, "unexpected error getActualPower write JSON %s %s %s" % (exc_type, fname, exc_tb.tb_lineno))
        self.logMessage(0, "end of getActualPower")

