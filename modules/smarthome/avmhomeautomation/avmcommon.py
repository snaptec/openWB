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
                self.logMessage(0, "found a session ID file, trying to load")
                f = open(file_stringsessionid, 'r')
                self.sessionID = f.read().strip()
                f.close()
                mtime = os.path.getmtime(file_stringsessionid)
                age_of_id_in_seconds = time.time() - mtime
                should_authenticate = self.sessionID == INVALID_SESSIONID or age_of_id_in_seconds / 60 >= 5
                self.logMessage(0, "loaded session ID from ramdisk: %s (age: %.1f seconds)" % (self.sessionID, age_of_id_in_seconds))
            else:
                self.logMessage(1, "no previously stored session ID found, will try to get a new one")
                should_authenticate = True
        except IOError as e:
            self.logMessage(2, "non-critical error reading previous session id: %s" % (e))
            should_authenticate = True
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.logMessage(2, "unexpected error during connect: %s %s %s" % (exc_type, fname, exc_tb.tb_lineno))

        if should_authenticate:
            self.logMessage(0, "(re-)authenticate at fritzbox, old sessionID: %s" % (self.sessionID))
            try:
                self.getAVMSessionID()
            except:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                self.logMessage(2, "unexpected error while negotiating session id: %s %s %s" % (exc_type, fname, exc_tb.tb_lineno))
            self.logMessage(0, "retrieved sessionID from fritzbox: %s" % (self.sessionID))
            try:
                # Try to store potentially new session id to ramdisk for next run
                # If this operations fails, no harm is done as we can always authenticate
                # with username/password.
                f = open(file_stringsessionid, 'w')
                print ('%s' % (self.sessionID),file = f)
                f.close()
            except IOError:
                self.logMessage(2, "non-critical storing session id: %s" % (e))
            except:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                self.logMessage(2, "unexpected error while storing session id: %s %s %s" % (exc_type, fname, exc_tb.tb_lineno))

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
            print ('%s: Device: %s AHA Module (actor: %s) %s%s' % (time_string, self.devicenumber, self.switchname, prefix, message), file = f)
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
            self.logMessage(2, "error while requesting device infos from fritz box:" % (e))
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


    # readOrBuildDeviceInfoCache fills self.device_infos, either from a cached
    # file of maximum age 5 minutes, or by fetching the info from the fritzbox.
    # The main purpose of this cache is to skip looking up the AIN via network
    # every time.
    def readOrBuildDeviceInfoCache(self):
        self.logMessage(0, "start of readOrBuildDeviceInfoCache")
        file_stringdeviceinfos = self.cacheFileString()
        try:
            if os.path.isfile(file_stringdeviceinfos):
                self.logMessage(0, "trying to load cached device infos")
                f = open(file_stringdeviceinfos, 'r')
                self.device_infos = json.loads(f.read().strip())
                f.close()
                mtime = os.path.getmtime(file_stringdeviceinfos)
                age_of_id_in_seconds = time.time() - mtime
                self.logMessage(0, "age of cachefile for device infos: %.1f seconds" % (age_of_id_in_seconds))
                should_fetch = age_of_id_in_seconds / 60 >= 5
            else:
                self.logMessage(0, "no cached device info yet")
                should_fetch = True
        except IOError as e:
            self.logMessage(2, "non-critical error reading cached device infos: %s" % (e))
            should_fetch = True
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.logMessage(2, "unexpected error during readOrBuild: %s %s %s" % (exc_type, fname, exc_tb.tb_lineno))
        self.logMessage(0, "should fetch new info from fritzbox: %s" % (should_fetch))
        if should_fetch:
            self.fetchAndCacheDeviceInfos()
        self.logMessage(0, "end of readOrBuildDeviceInfoCache")


    # fetchAndCacheDeviceInfos calls getDevicesDict and then stores the result in 
    # a cachefile on the ramdisk
    def fetchAndCacheDeviceInfos(self):
        self.logMessage(0, "fetching device info for all devices from fritzbox")
        try:
            self.getDevicesDict()
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.logMessage(2, "unexpected error during getDevicesDict: %s %s %s" % (exc_type, fname, exc_tb.tb_lineno))

        self.logMessage(0, "device info fetched: %s" % (self.device_infos))
        try:
            f = open(self.cacheFileString(), 'w')
            print ('%s' % (json.dumps(self.device_infos)), file = f)
            f.close()
        except IOError as e:
            self.logMessage(2, "error writing cached device info %s" % (e))
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.logMessage(2, "unexpected error writing cached device info result %s %s %s" % (exc_type, fname, exc_tb.tb_lineno))
        self.logMessage(0, "cached device infos to ramdisk")


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
        self.logMessage(0, "end of switchDevice")


    # getActualPowerForce returns current observed power and the state of the switch relais.
    # The JSON answer is either written to the according smarthome device return file
    # or dumped to stdout if no such file exists (for local development)
    def getActualPower(self):
        if self.sessionID == INVALID_SESSIONID:
            self.logMessage(2, "Kann ohne valide Anmeldung keine neuen Daten holen.")
            return
        self.logMessage(0, "start of getActualPower")
        self.fetchAndCacheDeviceInfos()
        if not self.switchname in self.device_infos:
            self.logMessage(2, "no such device found at fritzbox: %s" % (self.switchname))
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

