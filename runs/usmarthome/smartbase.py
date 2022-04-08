#!/usr/bin/python3

import subprocess
import json
import time
import os
from datetime import datetime, timezone


class Sbase0:
    _basePath = '/var/www/html/openWB'
    _prefixpy = _basePath+'/modules/smarthome/'

    def logClass(self, level, msg):
        if (int(level) >= 2):
            local_time = datetime.now(timezone.utc).astimezone()
            file = open('/var/www/html/openWB/ramdisk/smarthome.log',
                        'a', encoding='utf8')
            if (int(level) == 0):
                file.write(local_time.strftime(format="%Y-%m-%d %H:%M:%S")
                           + '-: ' + str(msg) + '\n')
            if (int(level) == 1):
                file.write(local_time.strftime(format="%Y-%m-%d %H:%M:%S")
                           + '-: ' + str(msg) + '\n')
            if (int(level) == 2):
                file.write(local_time.strftime(format="%Y-%m-%d %H:%M:%S")
                           + '-: ' + str(msg) + '\n')
            file.close


class Slbase(Sbase0):
    def __init__(self):
        #
        # setting
        print('__init__ Slbase executed')
        self.device_nummer = 0
        self.device_name = 'none'
        self.device_type = 'none'
        self.temp0 = '300'
        self.temp1 = '300'
        self.temp2 = '300'
        self.devuberschuss = 0
        self.newwatt = 0
        self.newwattk = 0
        self.relais = 0
        self._smart_param = {}
        self._device_differentmeasureoment = 0
        self._device_configured = '0'
        self._device_ip = 'none'
        self._device_measuretype = 'none'
        self._device_measureip = 'none'
        self._device_measureportsdm = '8899'
        self._device_measureid = '0'
        self._device_measuresmaser = '123'
        self._device_measuresmaage = 15
        self._device_leistungurl = 'none'
        self._device_measureurl = 'none'
        self._device_measureurlc = 'none'
        self._device_measurejsonurl = 'none'
        self._device_measurejsonpower = 'none'
        self._device_measurejsoncounter = 'none'
        self._device_measureavmactor = 'none'
        self._device_measureavmusername = 'none'
        self._device_measureavmpassword = 'none'
        self._device_actor = 'none'
        self._device_username = 'none'
        self._device_password = 'none'

    def updatepar(self, input_param):
        self._smart_param = input_param.copy()
        self.device_nummer = int(self._smart_param.get('device_nummer', '0'))
        for key, value in self._smart_param.items():
            try:
                valueint = int(value)
            except Exception:
                valueint = 0
            # params known to be used in sbase, to avoid logging
            if (key in ['device_nummer', 'device_mineinschaltdauer',
                        'device_finishTime', 'device_ausschaltschwelle',
                        'device_manual_control', 'device_canSwitch',
                        'device_standbyDuration', 'device_startTime',
                        'device_onuntilTime', 'device_einschaltverzoegerung',
                        'device_standbyPower', 'device_einschaltschwelle',
                        'device_ausschaltverzoegerung',
                        'device_speichersocbeforestop',
                        'device_homeConsumtion',
                        'device_deactivateWhileEvCharging',
                        'device_startupMulDetection', 'device_onTime',
                        'device_speichersocbeforestart', 'device_endTime',
                        'device_maxeinschaltdauer', 'mode',
                        'WHImported_temp', 'RunningTimeToday',
                        'oncountnor', 'OnCntStandby',
                        'device_startupDetection']):
                pass
            elif (key == 'device_differentMeasurement'):
                self._device_differentmeasurement = valueint
            elif (key == 'device_type'):
                self.device_type = value
            elif (key == 'device_configured'):
                self._device_configured = value
            elif (key == 'device_name'):
                self.device_name = value
            elif (key == 'device_temperatur_configured'):
                self.device_temperatur_configured = valueint
            elif (key == 'device_ip'):
                self._device_ip = value
            elif (key == 'device_measureType'):
                self._device_measuretype = value
            elif (key == 'device_measureip'):
                self._device_measureip = value
            elif (key == 'device_measurePortSdm'):
                self._device_measureportsdm = value
            elif (key == 'device_measuresmaage'):
                self._device_measuresmaage = valueint
            elif (key == 'device_measuresmaser'):
                self._device_measuresmaser = value
            elif (key == 'device_measureid'):
                self._device_measureid = value
            elif (key == 'device_leistungurl'):
                self._device_leistungurl = value
            elif (key == 'device_measureurl'):
                self._device_measureurl = value
            elif (key == 'device_measureurlc'):
                self._device_measureurlc = value
            elif (key == 'device_measurejsonurl'):
                self._device_measurejsonurl = value
            elif (key == 'device_measurejsonpower'):
                self._device_measurejsonpower = value
            elif (key == 'device_measurejsoncounter'):
                self._device_measurejsoncounter = value
            elif (key == 'device_measureavmactor'):
                self._device_measureavmactor = value
            elif (key == 'device_measureavmusername'):
                self._device_measureavmusername = value
            elif (key == 'device_measureavmpassword'):
                self._device_measureavmpassword = value
            elif (key == 'device_actor'):
                self._device_actor = value
            elif (key == 'device_username'):
                self._device_username = value
            elif (key == 'device_password'):
                self._device_password = value
            else:
                self.logClass(2, "(" + str(self.device_nummer) + ") "
                              + __class__.__name__ + " überlesen " + key +
                              " " + value)

    def __del__(self):
        print('__del__ Slbase executed ')


class Slmqtt(Slbase):
    def __init__(self):
        # setting
        super().__init__()
        print('__init__ Slmqtt excuted')

    def getwattread(self):
        self._watt(self._device_ip)

    def sepwattread(self):
        self._watt(self._device_measureip)
        return self.newwatt, self.newwattk

    def _watt(self, ip):
        argumentList = ['python3', self._prefixpy + 'mqtt/watt.py',
                        str(self.device_nummer), str(ip),
                        str(self.devuberschuss)]
        try:
            proc = subprocess.Popen(argumentList)
            proc.communicate()
            f1 = open(self._basePath+'/ramdisk/smarthome_device_ret' +
                      str(self.device_nummer), 'r')
            answerj = json.load(f1)
            f1.close()
            answer = json.loads(answerj)
            self.newwatt = int(answer['power'])
            self.newwattk = int(answer['powerc'])
            self.relais = int(answer['on'])
        except Exception as e1:
            self.logClass(2, "Leistungsmessung %s %d %s Fehlermeldung: %s "
                          % ('mqtt', self.device_nummer, ip, str(e1)))


class Slshelly(Slbase):
    def __init__(self):
        # setting
        super().__init__()
        print('__init__ Slshelly excuted')

    def getwattread(self):
        self._watt(self._device_ip)

    def sepwattread(self):
        self._watt(self._device_measureip)
        return self.newwatt, self.newwattk

    def _watt(self, ip):
        argumentList = ['python3', self._prefixpy + 'shelly/watt.py',
                        str(self.device_nummer), str(ip), '0']
        try:
            proc = subprocess.Popen(argumentList)
            proc.communicate()
            f1 = open(self._basePath+'/ramdisk/smarthome_device_ret' +
                      str(self.device_nummer), 'r')
            answerj = json.load(f1)
            f1.close()
            answer = json.loads(answerj)
            self.newwatt = int(answer['power'])
            self.newwattk = int(answer['powerc'])
            self.relais = int(answer['on'])
            if (self.device_temperatur_configured > 0):
                self.temp0 = str(answer['temp0'])
                f = open(self._basePath+'/ramdisk/device' + str(self.device_nummer) + '_temp0', 'w')
                f.write(str(self.temp0))
                f.close()
            else:
                self.temp0 = '300'
            if (self.device_temperatur_configured > 1):
                self.temp1 = str(answer['temp1'])
                f = open(self._basePath+'/ramdisk/device' + str(self.device_nummer) + '_temp1', 'w')
                f.write(str(self.temp1))
                f.close()
            else:
                self.temp1 = '300'
            if (self.device_temperatur_configured > 2):
                self.temp2 = str(answer['temp2'])
                f = open(self._basePath+'/ramdisk/device' + str(self.device_nummer) + '_temp2', 'w')
                f.write(str(self.temp2))
                f.close()
            else:
                self.temp2 = '300'
        except Exception as e1:
            self.logClass(2, "Leistungsmessung %s %d %s Fehlermeldung: %s "
                          % ('Shelly', self.device_nummer, ip, str(e1)))


class Slavm(Slbase):
    def __init__(self):
        # setting
        super().__init__()
        print('__init__ Slavm excuted')

    def getwattread(self):
        self._watt(self._device_ip, self._device_actor,
                   self._device_username,
                   self._device_password)

    def sepwattread(self):
        self._watt(self._device_measureip,
                   self._device_measureavmactor,
                   self._device_measureavmusername,
                   self._device_measureavmpassword)
        return self.newwatt, self.newwattk

    def _watt(self, ip, act, user, pw):
        argumentList = ['python3', self._prefixpy +
                        'avmhomeautomation/watt.py',
                        str(self.device_nummer), str(ip),
                        '0', '0',
                        act, user, pw]
        try:
            proc = subprocess.Popen(argumentList)
            proc.communicate()
            f1 = open(self._basePath+'/ramdisk/smarthome_device_ret' +
                      str(self.device_nummer), 'r')
            answerj = json.load(f1)
            f1.close()
            answer = json.loads(answerj)
            self.newwatt = int(answer['power'])
            self.newwattk = int(answer['powerc'])
            self.relais = int(answer['on'])
        except Exception as e1:
            self.logClass(2, "Leistungsmessung %s %d %s Fehlermeldung: %s "
                          % ('Avm ', self.device_nummer, ip, str(e1)))


class Sltasmota(Slbase):
    def __init__(self):
        # setting
        super().__init__()
        print('__init__ Sltasmota excuted')

    def getwattread(self):
        self._watt(self._device_ip)

    def sepwattread(self):
        self._watt(self._device_measureip)
        return self.newwatt, self.newwattk

    def _watt(self, ip):
        argumentList = ['python3', self._prefixpy + 'tasmota/watt.py',
                        str(self.device_nummer), str(ip), '0']
        try:
            proc = subprocess.Popen(argumentList)
            proc.communicate()
            f1 = open(self._basePath+'/ramdisk/smarthome_device_ret' +
                      str(self.device_nummer), 'r')
            answerj = json.load(f1)
            f1.close()
            answer = json.loads(answerj)
            self.newwatt = int(answer['power'])
            self.newwattk = int(answer['powerc'])
            self.relais = int(answer['on'])
        except Exception as e1:
            self.logClass(2, "Leistungsmessung %s %d %s Fehlermeldung: %s "
                          % ('Tasmota', self.device_nummer, ip, str(e1)))


class Slhttp(Slbase):
    def __init__(self):
        # setting
        super().__init__()
        print('__init__ Slhttp excuted')

    def getwattread(self):
        self._watt(self._device_leistungurl, 'none')

    def sepwattread(self):
        self._watt(self._device_measureurl, self._device_measureurlc)
        return self.newwatt, self.newwattk

    def _watt(self, url, urlc):
        argumentList = ['python3', self._prefixpy + 'http/watt.py',
                        str(self.device_nummer), '0', str(self.devuberschuss),
                        url, urlc]
        try:
            proc = subprocess.Popen(argumentList)
            proc.communicate()
            f1 = open(self._basePath+'/ramdisk/smarthome_device_ret' +
                      str(self.device_nummer), 'r')
            answerj = json.load(f1)
            f1.close()
            answer = json.loads(answerj)
            self.newwatt = int(answer['power'])
            self.newwattk = int(answer['powerc'])
            self.relais = int(answer['on'])
        except Exception as e1:
            self.logClass(2, "Leistungsmessung %s %d Fehlermeldung: %s "
                          % ('http', self.device_nummer, str(e1)))


class Slmystrom(Slbase):
    def __init__(self):
        # setting
        super().__init__()
        print('__init__ Slmystrom excuted')

    def getwattread(self):
        self._watt(self._device_ip)

    def sepwattread(self):
        self._watt(self._device_measureip)
        return self.newwatt, self.newwattk

    def _watt(self, ip):
        argumentList = ['python3', self._prefixpy + 'mystrom/watt.py',
                        str(self.device_nummer), str(ip), '0']
        try:
            proc = subprocess.Popen(argumentList)
            proc.communicate()
            f1 = open(self._basePath+'/ramdisk/smarthome_device_ret' +
                      str(self.device_nummer), 'r')
            answerj = json.load(f1)
            f1.close()
            answer = json.loads(answerj)
            self.newwatt = int(answer['power'])
            self.newwattk = int(answer['powerc'])
            self.relais = int(answer['on'])
            if (self.device_temperatur_configured > 0):
                self.temp0 = str(answer['temp0'])
                f = open(self._basePath+'/ramdisk/device' + str(self.device_nummer) + '_temp0', 'w')
                f.write(str(self.temp0))
                f.close()
            else:
                self.temp0 = '300'
        except Exception as e1:
            self.logClass(2, "Leistungsmessung %s %d %s Fehlermeldung: %s "
                          % ('Mystrom', self.device_nummer, ip, str(e1)))


class Slsmaem(Slbase):
    def __init__(self):
        # setting
        super().__init__()
        print('__init__ Slsmaem excuted')

    def sepwattread(self):
        argumentList = ['python3', self._prefixpy + 'smaem/watt.py',
                        str(self.device_nummer), str(self._device_measureip),
                        str(self._device_measuresmaser),
                        str(self._device_measuresmaage)]
        try:
            proc = subprocess.Popen(argumentList)
            proc.communicate()
            f1 = open(self._basePath+'/ramdisk/smarthome_device_ret' +
                      str(self.device_nummer), 'r')
            answerj = json.load(f1)
            f1.close()
            answer = json.loads(answerj)
            self.newwatt = int(answer['power'])
            self.newwattk = int(answer['powerc'])
        except Exception as e1:
            self.logClass(2, "Leistungsmessung %s %d %s Fehlermeldung: %s "
                          % ('smaem ', self.device_nummer,
                             str(self._device_measureip), str(e1)))
        return self.newwatt, self.newwattk


class Slwe514(Slbase):
    def __init__(self):
        # setting
        super().__init__()
        print('__init__ Slwe514 excuted')

    def sepwattread(self):
        argumentList = ['python3', self._prefixpy + 'we514/watt.py',
                        str(self.device_nummer), str(self._device_measureip),
                        str(self._device_measureid)]
        try:
            proc = subprocess.Popen(argumentList)
            proc.communicate()
            f1 = open(self._basePath+'/ramdisk/smarthome_device_ret' +
                      str(self.device_nummer), 'r')
            answerj = json.load(f1)
            f1.close()
            answer = json.loads(answerj)
            self.newwatt = int(answer['power'])
            self.newwattk = int(answer['powerc'])
        except Exception as e1:
            self.logClass(2, "Leistungsmessung %s %d %s Fehlermeldung: %s "
                          % ('we514 ', self.device_nummer,
                             str(self._device_measureip), str(e1)))
        return self.newwatt, self.newwattk


class Sljson(Slbase):
    def __init__(self):
        # setting
        super().__init__()
        print('__init__ Sljson excuted')

    def sepwattread(self):
        argumentList = ['python3', self._prefixpy + 'json/watt.py',
                        str(self.device_nummer),
                        self._device_measurejsonurl,
                        self._device_measurejsonpower,
                        self._device_measurejsoncounter]
        try:
            proc = subprocess.Popen(argumentList)
            proc.communicate()
            f1 = open(self._basePath+'/ramdisk/smarthome_device_ret' +
                      str(self.device_nummer), 'r')
            answerj = json.load(f1)
            f1.close()
            answer = json.loads(answerj)
            self.newwatt = int(answer['power'])
            self.newwattk = int(answer['powerc'])
        except Exception as e1:
            self.logClass(2, "Leistungsmessung %s %s Fehlermeldung: %s "
                          % ('json ', self.device_nummer, str(e1)))
        return self.newwatt, self.newwattk


class Slfronius(Slbase):
    def __init__(self):
        # setting
        super().__init__()
        print('__init__ Slfronius excuted')

    def sepwattread(self):
        argumentList = ['python3', self._prefixpy + 'fronius/watt.py',
                        str(self.device_nummer), str(self._device_measureip),
                        str(self._device_measureid)]
        try:
            proc = subprocess.Popen(argumentList)
            proc.communicate()
            f1 = open(self._basePath+'/ramdisk/smarthome_device_ret' +
                      str(self.device_nummer), 'r')
            answerj = json.load(f1)
            f1.close()
            answer = json.loads(answerj)
            self.newwatt = int(answer['power'])
            self.newwattk = int(answer['powerc'])
        except Exception as e1:
            self.logClass(2, "Leistungsmessung %s %d %s Fehlermeldung: %s "
                          % ('fronius ', self.device_nummer,
                             str(self._device_measureip), str(e1)))
        return self.newwatt, self.newwattk


class Slsdm630(Slbase):
    def __init__(self):
        # setting
        super().__init__()
        print('__init__ Slsdm630 excuted')

    def sepwattread(self):
        argumentList = ['python3', self._prefixpy + 'sdm630/sdm630.py',
                        str(self.device_nummer), str(self._device_measureip),
                        str(self._device_measureid),
                        str(self._device_measureportsdm)]
        try:
            proc = subprocess.Popen(argumentList)
            proc.communicate()
            f1 = open(self._basePath+'/ramdisk/smarthome_device_ret' +
                      str(self.device_nummer), 'r')
            answerj = json.load(f1)
            f1.close()
            answer = json.loads(answerj)
            self.newwatt = int(answer['power'])
            self.newwattk = int(answer['powerc'])
        except Exception as e1:
            self.logClass(2, "Leistungsmessung %s %d %s Fehlermeldung: %s "
                          % ('Sdm630 ', self.device_nummer,
                             str(self._device_measureip), str(e1)))
        return self.newwatt, self.newwattk


class Slsdm120(Slbase):
    def __init__(self):
        # setting
        super().__init__()
        print('__init__ Slsdm120 excuted')

    def sepwattread(self):
        argumentList = ['python3', self._prefixpy + 'sdm120/sdm120.py',
                        str(self.device_nummer), str(self._device_measureip),
                        str(self._device_measureid),
                        str(self._device_measureportsdm)]
        try:
            proc = subprocess.Popen(argumentList)
            proc.communicate()
            f1 = open(self._basePath+'/ramdisk/smarthome_device_ret' +
                      str(self.device_nummer), 'r')
            answerj = json.load(f1)
            f1.close()
            answer = json.loads(answerj)
            self.newwatt = int(answer['power'])
            self.newwattk = int(answer['powerc'])
        except Exception as e1:
            self.logClass(2, "Leistungsmessung %s %d %s Fehlermeldung: %s "
                          % ('Sdm120 ', self.device_nummer,
                             str(self._device_measureip), str(e1)))
        return self.newwatt, self.newwattk


class Sbase(Sbase0):
    def __init__(self):
        # setting
        print('__init__ Sbase executed')
        self.mqtt_param = {}
        self.mqtt_param_del = {}
        self.device_name = 'none'
        self.devstatus = 10
        # (10 = ueberschuss gesteuert oder manual,
        # 20 = Anlauferkennung aktiv
        # (ausschalten wenn Leistungsaufnahme > Schwelle)
        #  30 = gestartet um fertig bis zu erreichen
        # default 10
        self._first_run = 1
        self.device_nummer = 0
        self.temp0 = '300'
        self.temp1 = '300'
        self.temp2 = '300'
        self.newwatt = 0
        self.newwattk = 0
        self.relais = 0
        self.devuberschuss = 0
        self.device_temperatur_configured = 0
        self.ueberschussberechnung = 1
        self.abschalt = 0
        self.device_homeconsumtion = 0
        self.device_manual = 0
        self.device_type = 'none'
        self._smart_param = {}
        self._uberschussoffset = 0
        self._uberschuss = 0
        self.device_canswitch = 0
        self._device_deactivatewhileevcharging = 0
        self._device_mineinschaltdauer = 0
        self._device_maxeinschaltdauer = 0
        self._device_differentmeasurement = 0
        self._device_speichersocbeforestop = 100
        self._device_speichersocbeforestart = 0
        self._device_startupdetection = 0
        self._device_standbypower = 0
        self._device_standbyduration = 0
        self._device_startupmuldetection = 0
        self._device_einschaltschwelle = 0
        self._device_ausschaltschwelle = 0
        self._device_einschaltverzoegerung = 0
        self._device_ausschaltverzoegerung = 0
        self._device_configured = '0'
        self._device_ip = 'none'
        self._device_measuretype = 'none'
        self._device_measureip = 'none'
        self._device_measureportsdm = '8899'
        self._device_measureid = '0'
        self._device_finishtime = '00:00'
        self._device_starttime = '00:00'
        self._device_endtime = '00:00'
        self._device_ontime = '00:00'
        self._device_onuntiltime = '00:00'

        self.device_manual_control = 0

        self._oldrelais = '2'
        self._oldwatt = 0
        # mqtt per
        self._whimported_tmp = 0
        self.runningtime = 0
        self.oncountnor = '0'
        self.oncntstandby = '0'

        self._wh = 0
        self._wpos = 0
        # DeviceValues.update( {str(nummer) + "wh" : round(wattposkh, 2)})
        self._deviceconfigured = '1'
        self._deviceconfiguredold = '9'
        # not none !
        self._oldmeasuretype1 = 'empty'
        self.c_oldstampeinschaltdauer = 0
        self.c_oldstampeinschaltdauer_f = 'N'
        self.c_mantime = 0
        self.c_mantime_f = 'N'
        self._c_eintime = 0
        self._c_eintime_f = 'N'
        self._c_anlaufz = 0
        self._c_anlaufz_f = 'N'
        self._c_ausverz = 0
        self._c_ausverz_f = 'N'
        self._c_einverz = 0
        self._c_einverz_f = 'N'


    def __del__(self):

        print('__del__ Sbase executed ')

    def prewatt(self, uberschuss, uberschussoffset):
        self._uberschuss = uberschuss
        self._uberschussoffset = uberschussoffset
        if (self._deviceconfiguredold == "9") and (self._deviceconfigured ==
                                                   "1"):
            if self._device_deactivatewhileevcharging > 0:
                # nach startup alle aktiven devices mit Autoladen aus als
                # other fuehren
                self.c_mantime_f = 'Y'
                self.c_mantime = int(time.time())
            self._deviceconfiguredold = self._deviceconfigured
        self.abschalt = 0
        if self._device_deactivatewhileevcharging > 0:
            if (self._c_eintime_f == 'Y'):
                # alle abschaltbaren devices während mindestlaufzeit
                # als other führen
                timesta = int(time.time()) - self._c_eintime
                if (self._device_mineinschaltdauer < timesta):
                    self.abschalt = 1
                else:
                    self.abschalt = 0
            else:
                self.abschalt = 1
            # prepare end
        self.getueb()

    def postwatt(self):
        (self.newwatt, self.newwattk) = self.sepwatt(self.newwatt,
                                                     self.newwattk)
        # bei reiner Leistungsmessung relais nur nach Watt setzten
        if (self.newwatt > 1) and (self.device_type == 'none'):
            self.relais = 1
        # bei laufender Anlauferkennung deivce nicht aktiv setzten
        if (self.relais == 1) and (self.devstatus != 20):
            self.relais = 1
        else:
            self.relais = 0
        self.mqtt_param = {}
        pref = 'openWB/SmartHome/Devices/' + str(self.device_nummer) + '/'
        self.mqtt_param[pref + 'RelayStatus'] = self.relais
        if (self.c_mantime_f == 'Y') and (self.device_manual != 1):
            # nach Ausschalten manueller Modus mindestens 30 Sek +
            # max( ausschaltverzögerung,mindeseinschaltdauer
            #  als nicht abschaltbarer
            # device fuehren, damit nicht ungewollt pv überwchuss erkannt wird
            manverz = max(self._device_ausschaltverzoegerung,
                          self._device_mineinschaltdauer) + 30
            timesince = int(time.time()) - int(self.c_mantime)
            if (manverz < timesince):
                self.logClass(2,
                              "(" + str(self.device_nummer) + ") von Manuell "
                              + "auf Automatisch gestellt oder startup,"
                              + " Uebergangsfrist abgelaufen" +
                              self.c_mantime_f)
                self.c_mantime_f = 'N'
            else:
                self.logClass(2,
                              "(" + str(self.device_nummer) + ") von Manuell" +
                              " auf Automatisch gestellt oder startup," +
                              " Uebergangsfrist laueft noch " + str(manverz) +
                              " > " + str(timesince))
                self.abschalt = 0
        self._oldwatt = self.newwatt
        f = open(self._basePath+'/ramdisk/device' + str(self.device_nummer) +
                 '_watt', 'w')
        f.write(str(self._oldwatt))
        f.close()
        f = open(self._basePath+'/ramdisk/device' + str(self.device_nummer) +
                 '_relais', 'w')
        f.write(str(self.relais))
        f.close()
        try:
            with open(self._basePath+'/ramdisk/smarthome_device_' +
                      str(self.device_nummer) + 'watt0pos', 'r') as value:
                importtemp = int(value.read())
                self.simcount(self._oldwatt, "smarthome_device_" +
                              str(self.device_nummer),
                              "device" + str(self.device_nummer) + "_wh",
                              "device" + str(self.device_nummer) + "_whe",
                              str(self.device_nummer), self.newwattk)
        except Exception:
            importtemp = self._whimported_tmp
            f = open(self._basePath+'/ramdisk/smarthome_device_' +
                     str(self.device_nummer) + 'watt0pos', 'w')
            f.write(str(importtemp))
            f.close()
            f = open(self._basePath++'/ramdisk/smarthome_device_' +
                     str(self.device_nummer) + 'watt0neg', 'w')
            f.write(str("0"))
            f.close()
        if (self.relais == 1):
            newtime = int(time.time())
            if (self.c_oldstampeinschaltdauer_f == 'Y'):
                timediff = newtime - self.c_oldstampeinschaltdauer
                self.runningtime = self.runningtime + int(timediff)
                self.c_oldstampeinschaltdauer = newtime
            else:
                self.c_oldstampeinschaltdauer = newtime
                self.c_oldstampeinschaltdauer_f = 'Y'
        else:
            self.c_oldstampeinschaltdauer = 0
            self.c_oldstampeinschaltdauer_f = 'N'
        self.mqtt_param[pref + 'RunningTimeToday'] = self.runningtime
        # Einschaltzeit des Relais setzen
        if (self._oldrelais == 0):
            if (self.relais == 1):
                self._c_eintime = int(time.time())
                self._c_eintime_f = 'Y'
            else:
                self._c_eintime = 0
                self._c_eintime_f = 'N'
        self._oldrelais = self.relais
        if (self.device_temperatur_configured > 0):
            self.mqtt_param[pref + 'TemperatureSensor0'] = self.temp0
        if (self.device_temperatur_configured > 1):
            self.mqtt_param[pref + 'TemperatureSensor1'] = self.temp1
        if (self.device_temperatur_configured > 2):
            self.mqtt_param[pref + 'TemperatureSensor2'] = self.temp2
        self.mqtt_param[pref + 'Watt'] = self._oldwatt
        self.mqtt_param[pref + 'Wh'] = self._wh
        self.mqtt_param[pref + 'WHImported_temp'] = self._wpos
        self.mqtt_param[pref + 'oncountnor'] = self.oncountnor
        self.mqtt_param[pref + 'OnCntStandby'] = self.oncntstandby
        # nur bei Status 10 on status mitnehmen
        if (self.devstatus == 10):
            sendstatus = self.relais + self.devstatus
        else:
            sendstatus = self.devstatus
        self.mqtt_param[pref + 'Status'] = sendstatus

    def updatepar(self, input_param):
        self._smart_param = input_param.copy()
        self.device_nummer = int(self._smart_param.get('device_nummer', '0'))
        for key, value in self._smart_param.items():
            try:
                valueint = int(value)
            except Exception:
                valueint = 0
            if (key in ['device_nummer']):
                pass
            elif (key == 'device_canSwitch'):
                self.device_canswitch = valueint
            elif (key == 'device_deactivateWhileEvCharging'):
                self._device_deactivatewhileevcharging = valueint
            elif (key == 'device_mineinschaltdauer'):
                self._device_mineinschaltdauer = valueint * 60
            elif (key == 'device_maxeinschaltdauer'):
                self._device_maxeinschaltdauer = valueint * 60
            elif (key == 'device_homeConsumtion'):
                self.device_homeconsumtion = valueint
            elif (key == 'device_differentMeasurement'):
                self._device_differentmeasurement = valueint
            elif (key == 'device_temperatur_configured'):
                self.device_temperatur_configured = valueint
            elif (key == 'device_speichersocbeforestop'):
                self._device_speichersocbeforestop = valueint
            elif (key == 'device_speichersocbeforestart'):
                self._device_speichersocbeforestart = valueint
            elif (key == 'device_startupDetection'):
                self._device_startupdetection = valueint
            elif (key == 'device_standbyPower'):
                self._device_standbypower = valueint
            elif (key == 'device_standbyDuration'):
                self._device_standbyduration = valueint
            elif (key == 'device_standbypower'):
                self._device_standbypower = valueint
            elif (key == 'device_standbyduration'):
                self._device_standbyduration = valueint
            elif (key == 'device_startupMulDetection'):
                self._device_startupmuldetection = valueint
            elif (key == 'device_einschaltschwelle'):
                self._device_einschaltschwelle = valueint
            elif (key == 'device_ausschaltschwelle'):
                self._device_ausschaltschwelle = valueint * -1
            elif (key == 'device_einschaltverzoegerung'):
                self._device_einschaltverzoegerung = valueint * 60
            elif (key == 'device_ausschaltverzoegerung'):
                self._device_ausschaltverzoegerung = valueint * 60
            elif (key == 'device_type'):
                self.device_type = value
            elif (key == 'device_configured'):
                self._device_configured = value
            elif (key == 'device_name'):
                self.device_name = value
            elif (key == 'device_ip'):
                self._device_ip = value
            elif (key == 'device_measureType'):
                self._device_measuretype = value
            elif (key == 'device_measureip'):
                self._device_measureip = value
            elif (key == 'device_measurePortSdm'):
                self._device_measureportsdm = value
            elif (key == 'device_measureid'):
                self._device_measureid = value
            elif (key == 'device_finishTime'):
                self._device_finishtime = value
            elif (key == 'device_startTime'):
                self._device_starttime = value
            elif (key == 'device_endTime'):
                self._device_endtime = value
            elif (key == 'device_onTime'):
                self._device_ontime = value
            elif (key == 'device_onuntilTime'):
                self._device_onuntiltime = value
            elif (key == 'mode'):
                self.device_manual = valueint
            elif (key == 'device_manual_control'):
                self.device_manual_control = valueint
# openWB/config/set/SmartHome/Devices/<ID>/mode auf 1 setzen -> Gerät wird
# als 'Manuell' in der Geräteliste geführt
# openWB/config/set/SmartHome/Devices/<ID>/device_manual_control -> 0
# signalisiert dass das Gerät ausgeschaltet ist, 1 signalisiert Betrieb
            elif (key == 'WHImported_temp'):
                if (self._first_run == 1):
                    self._whimported_tmp = valueint
                    self.logClass(2, "(" + str(self.device_nummer) +
                                  ") aus mqtt übernommen " + key +
                                  " " + value)
            elif (key == 'RunningTimeToday'):
                if (self._first_run == 1):
                    self.runningtime = valueint
                    self.logClass(2, "(" + str(self.device_nummer) +
                                  ") aus mqtt übernommen " + key +
                                  " " + value)
            elif (key == 'oncountnor'):
                if (self._first_run == 1):
                    self.oncountnor = value
                    self.logClass(2, "(" + str(self.device_nummer) +
                                  ") aus mqtt übernommen " + key +
                                  " " + value)
            elif (key == 'OnCntStandby'):
                if (self._first_run == 1):
                    self.oncntstandby = value
                    # status normal setzen
                    self.devstatus = 10
                    self.logClass(2, "(" + str(self.device_nummer) +
                                  ") aus mqtt übernommen " + key +
                                  " " + value)
            else:
                self.logClass(2, "(" + str(self.device_nummer) + ") "
                              + __class__.__name__ + " überlesen " + key +
                              " " + value)
        self._first_run = 0
        pref = 'openWB/SmartHome/Devices/' + str(self.device_nummer) + '/'
        self.mqtt_param_del[pref + 'RelayStatus'] = '0'
        self.mqtt_param_del[pref + 'Watt'] = '0'
        self.mqtt_param_del[pref + 'oncountnor'] = '0'
        self.mqtt_param_del[pref + 'OnCntStandby'] = '0'
        self.mqtt_param_del[pref + 'Status'] = '0'
        self.mqtt_param_del[pref + 'TemperatureSensor0'] = '300'
        self.mqtt_param_del[pref + 'TemperatureSensor1'] = '300'
        self.mqtt_param_del[pref + 'TemperatureSensor2'] = '300'
        self.mqtt_param_del[pref + 'RunningTimeToday'] = '0'
        if (self.device_type == 'none'):
            self.device_canswitch = 0
        if (self._device_differentmeasurement == 1):
            if (self._oldmeasuretype1 == self._device_measuretype):
                self.logClass(2, "(" + str(self.device_nummer) +
                              ") Separate Leistungsmessung. Nur Parameter" +
                              " update " + self._device_measuretype)
                self._mydevicemeasure.updatepar(self._smart_param)
            else:
                if (self._oldmeasuretype1 == 'empty'):
                    pass
                else:
                    self.logClass(2, "(" + str(self.device_nummer) +
                                  ") Separate Leistungsmessung. Altes Measure"
                                  + "device gelöscht " + self._oldmeasuretype1)
                    del self._mydevicemeasure
                if (self._device_measuretype == 'sdm630'):
                    self._mydevicemeasure = Slsdm630()
                elif (self._device_measuretype == 'sdm120'):
                    self._mydevicemeasure = Slsdm120()
                elif (self._device_measuretype == 'we514'):
                    self._mydevicemeasure = Slwe514()
                elif (self._device_measuretype == 'fronius'):
                    self._mydevicemeasure = Slfronius()
                elif (self._device_measuretype == 'json'):
                    self._mydevicemeasure = Sljson()
                elif (self._device_measuretype == 'smaem'):
                    self._mydevicemeasure = Slsmaem()
                elif (self._device_measuretype == 'shelly'):
                    self._mydevicemeasure = Slshelly()
                elif (self._device_measuretype == 'tasmota'):
                    self._mydevicemeasure = Sltasmota()
                elif (self._device_measuretype == 'mqtt'):
                    self._mydevicemeasure = Slmqtt()
                elif (self._device_measuretype == 'http'):
                    self._mydevicemeasure = Slhttp()
                elif (self._device_measuretype == 'avm'):
                    self._mydevicemeasure = Slavm()
                elif (self._device_measuretype == 'mystrom'):
                    self._mydevicemeasure = Slmystrom()
                else:
                    self.logClass(2, "(" + str(self.device_nummer) +
                                  ") Measuretype nicht untertützt " +
                                  self._device_measuretype)
                self._mydevicemeasure.updatepar(self._smart_param)
                self._oldmeasuretype1 = self._device_measuretype
                self.logClass(2, "(" + str(self.device_nummer) +
                              ") Separate Leistungsmessung. Neues Measure" +
                              "device erzeugt " + self._device_measuretype)
        if ((self._device_differentmeasurement == 0) and
           (self._oldmeasuretype1 != 'empty')):
            self.logClass(2, "(" + str(self.device_nummer) +
                          ") Separate Leistungsmessung ausgeschaltet"
                          " Altes Measure" +
                          "device gelöscht " + self._oldmeasuretype1)
            del self._mydevicemeasure
            self._oldmeasuretype1 = 'empty'

    def getueb(self):
        #    (1 = mit Speicher, 2 = mit offset , 0 = manual eingeschaltet)
        if (self.ueberschussberechnung == 2):
            self.devuberschuss = self._uberschussoffset
        else:
            self.devuberschuss = self._uberschuss

    def preturn(self, zustand, ueberschussberechnung, updatecnt):
        self.ueberschussberechnung = ueberschussberechnung
        f = open(self._basePath+'/ramdisk/device' + str(self.device_nummer) +
                 '_req_relais', 'w')
        f.write(str(zustand))
        f.close()
        if (zustand == 1):
            if updatecnt == 1:
                self.oncountnor = str(int(self.oncountnor) + 1)
            else:
                self.oncntstandby = str(int(self.oncntstandby) + 1)
            self.logClass(2, "(" + str(self.device_nummer) +
                          ") angeschaltet. Ueberschussberechnung (1 = mit " +
                          " Speicher, 2 = mit Offset) " +
                          str(self.ueberschussberechnung))
            if updatecnt == 1:
                self._c_eintime_f = 'Y'
                self._c_eintime = int(time.time())

    def sepwatt(self, newwatt, newwattk):
        if (self._device_differentmeasurement == 0):
            return newwatt, newwattk
        # ueberschuss übertragen
        self._mydevicemeasure.devuberschuss = self.devuberschuss
        self._mydevicemeasure.sepwattread()
        self.newwatt = self._mydevicemeasure.newwatt
        self.newwattk = self._mydevicemeasure.newwattk
        return self.newwatt, self.newwattk

    def conditions(self, speichersoc):
        # do not do anything in case none type or can switch = no
        # or device manuam mode
        if ((self.device_canswitch == 0) or
           (self.device_manual == 1)):
            return
        file_charge = '/var/www/html/openWB/ramdisk/llkombiniert'
        testcharge = 0
        if os.path.isfile(file_charge):
            f = open(file_charge, 'r')
            testcharge = int(f.read())
            f.close()
        if testcharge <= 1000:
            chargestatus = 0
        else:
            chargestatus = 1
        work_ausschaltschwelle = self._device_ausschaltschwelle
        work_ausschaltverzoegerung = self._device_ausschaltverzoegerung
        local_time = datetime.now(timezone.utc).astimezone()
        localhour = int(local_time.strftime(format="%H"))
        localminute = int(local_time.strftime(format="%M"))
        localinsec = int((localhour * 60 * 60) + (localminute * 60))
        # onnow = 0 -> normale Regelung
        # onnow = 1 -> Zeitpunkt erreciht, immer ein ohne Ueberschuss regelung
        onnow = 0
        if (self._device_ontime != '00:00'):
            onhour = int(str("0") + str(self._device_ontime).partition(':')[0])
            onminute = int(str(self._device_ontime)[-2:])
            self.logClass(2, "(" + str(self.device_nummer) + ") " +
                          self.device_name + " Immer an nach definiert " +
                          str(onhour) + ":" + str('%.2d' % onminute) +
                          " aktuelle Zeit " + str(localhour) + ":" +
                          str('%.2d' % localminute))
            if ((onhour > localhour) or ((onhour == localhour)
               and (onminute >= localminute))):
                pass
            else:
                self.logClass(2, "(" + str(self.device_nummer) + ") " +
                              self.device_name +
                              " schalte ein wegen Immer an nach")
                onnow = 1
        if (self._device_onuntiltime != '00:00'):
            onuntilh = int(str("0")
                           + str(self._device_onuntiltime).partition(':')[0])
            onuntilminute = int(str(self._device_onuntiltime)[-2:])
            self.logClass(2, "(" + str(self.device_nummer) + ") " +
                          self.device_name + " Immer an vor definiert " +
                          str(onuntilh) + ":" + str('%.2d' % onuntilminute)
                          + " aktuelle Zeit " + str(localhour) + ":" +
                          str('%.2d' % localminute))
            if ((onuntilh < localhour) or ((onuntilh == localhour)
               and (onuntilminute <= localminute))):
                pass
            else:
                self.logClass(2, "(" + str(self.device_nummer) + ") " +
                              self.device_name +
                              " schalte ein wegen Immer an vor")
                onnow = 1
        if ((self._device_finishtime != '00:00')
           and (self.oncountnor == str("0"))):
            finishhour = int(str("0") +
                             str(self._device_finishtime).partition(':')[0])
            finishminute = int(str(self._device_finishtime)[-2:])
            startspatsec = int((finishhour * 60 * 60) + (finishminute * 60) -
                               self._device_mineinschaltdauer)
            self.logClass(2, "(" + str(self.device_nummer) + ") " +
                          self.device_name +
                          " finishtime definiert " +
                          str(finishhour) + ":" + str('%.2d' % finishminute)
                          + " aktuelle Zeit " + str(localhour) + ":" +
                          str('%.2d' % localminute) +
                          " Anzahl Starts heute 0 Mineinschaltdauer (Sec)"
                          + str(self._device_mineinschaltdauer))
            if (((finishhour > localhour) or ((finishhour == localhour)
               and (finishminute >= localminute)))
               and (startspatsec <= localinsec)):
                self.logClass(2, "(" + str(self.device_nummer) + ") " +
                              self.device_name +
                              " schalte ein wegen finishtime, spaetester" +
                              "start in sec " + str(startspatsec) +
                              " aktuelle sec " + str(localinsec))
                self.turndevicerelais(1, 0, 1)
                self.devstatus = 30
                return
        if self.devstatus == 30:
            self.logClass(2, "(" + str(self.device_nummer) + ") " +
                          self.device_name +
                          " finishtime laueft, pruefe Mindestlaufzeit")
            if (self._c_eintime_f == 'Y'):
                timesta = int(time.time()) - int(self._c_eintime)
                if (self._device_mineinschaltdauer < timesta):
                    self.logClass(2, "(" + str(self.device_nummer) + ") " +
                                  self.device_name +
                                  " Mindesteinschaltdauer erreicht," +
                                  " finishtime erreicht")
                    self.devstatus = 10
                    return
                else:
                    self.logClass(2, "(" + str(self.device_nummer) + ") " +
                                  self.device_name +
                                  " finishtime laueft, Mindesteinschaltdauer" +
                                  "nicht erreicht, " +
                                  str(self._device_mineinschaltdauer) +
                                  " > " + str(timesta))
                    return
            else:
                self.logClass(2, "(" + str(self.device_nummer) + ") " +
                              self.device_name +
                              " Mindesteinschaltdauer nicht bekannt," +
                              " finishtime erreicht")
                self.devstatus = 10
                return
        # here startup device_self._device_startupdetection
        if (((self._device_startupdetection == 0) or (onnow == 1))
           and (self.devstatus == 20)):
            self.devstatus = 10
            self.turndevicerelais(0, 0, 1)
            self.logClass(2, "(" + str(self.device_nummer) + ") " +
                          self.device_name +
                          " Anlauferkennung nun abgeschaltet ")
            return
        # remove condition that device has to be off
        if ((self._device_startupdetection == 1)
           and (self.oncntstandby == str("0"))
           and (self.oncountnor == str("0"))
           and (self.devstatus != 20)):
            self.devstatus = 20
            self.logClass(2, "(" + str(self.device_nummer) + ") " +
                          self.device_name +
                          " Anlauferkennung nun aktiv, eingeschaltet ")
            self.turndevicerelais(1, 0, 0)
            return
        if (self.devstatus == 20):
            if (self.newwatt) > self._device_standbypower:
                if (self._c_anlaufz_f == 'Y'):
                    timesince = int(time.time()) - int((self._c_anlaufz))
                    if (self._device_standbyduration < timesince):
                        self.logClass(2, "(" + str(self.device_nummer) + ") " +
                                      self.device_name +
                                      " standbycheck abgelaufen " +
                                      str(self._device_standbyduration) +
                                      " ,sec pruefe Einschaltschwelle " +
                                      str(self._device_standbypower))
                        self.devstatus = 10
                        self._c_anlaufz_f = 'N'
                        if ((self.devuberschuss >
                           self._device_einschaltschwelle) or (onnow == 1)):
                            self._c_ausverz_f = 'N'
                            self._c_einverz_f = 'N'
                            self.logClass(2, "(" + str(self.device_nummer) +
                                          ") " + self.device_name +
                                          " Überschuss " +
                                          str(self.devuberschuss) +
                                          " größer Einschaltschwelle oder" +
                                          " Immer an zeit erreicht, schalte " +
                                          "ein (ohne Einschaltverzoegerung) " +
                                          str(self._device_einschaltschwelle))
                            self.turndevicerelais(1,
                                                  self.ueberschussberechnung,
                                                  1)
                        else:
                            self.logClass(2, "(" + str(self.device_nummer) +
                                          ") " + self.device_name +
                                          " Überschuss " +
                                          str(self.devuberschuss) +
                                          " kleiner Einschaltschwelle," +
                                          " schalte aus " +
                                          str(self._device_einschaltschwelle))
                            self.turndevicerelais(0, 0, 1)
                        return
                    else:
                        self.logClass(2, "(" + str(self.device_nummer) + ") " +
                                      self.device_name +
                                      " standbycheck noch nicht erreicht " +
                                      str(self._device_standbyduration) + " > "
                                      + str(timesince))
                else:
                    self._c_anlaufz_f = 'Y'
                    self._c_anlaufz = int(time.time())
                    self.logClass(2, "(" + str(self.device_nummer) + ") " +
                                  self.device_name + " standbycheck gestartet "
                                  + str(self.newwatt) + " > " +
                                  str(self._device_standbypower))
            else:
                self._c_anlaufz_f = 'N'
                self.logClass(2, "(" + str(self.device_nummer) + ") " +
                              self.device_name +
                              " unter standbyschwelle , timer geloescht")
        if (self._device_maxeinschaltdauer > self.runningtime):
            self.logClass(2, "(" + str(self.device_nummer) + ") " +
                          self.device_name +
                          " Maximale Einschaltdauer nicht erreicht")
        else:
            if (self.relais == 1):
                self.logClass(2, "(" + str(self.device_nummer) + ") " +
                              self.device_name +
                              " Maximale Einschaltdauer erreicht schalte ab")
                self.turndevicerelais(0, 0, 1)
            else:
                self.logClass(2, "(" + str(self.device_nummer) + ")" +
                              self.device_name +
                              " Maximale Einschaltdauer erreicht" +
                              " bereits abgeschaltet")
            return
        # Auto ladung
        if self._device_deactivatewhileevcharging > 0:
            if (self.relais == 1):
                self.logClass(2, "(" + str(self.device_nummer) + ") " +
                              self.device_name +
                              " Soll reduziert/abgeschaltet werden" +
                              " bei Ladung, pruefe " + str(testcharge))
                if chargestatus == 1:
                    self.logClass(2, "(" + str(self.device_nummer) + ") " +
                                  self.device_name +
                                  " Ladung läuft, pruefe Mindestlaufzeit")
                    if (self._c_eintime_f == 'Y'):
                        timesta = int(time.time()) - int(self._c_eintime)
                        if (self._device_mineinschaltdauer < timesta):
                            if self._device_deactivatewhileevcharging == 2:
                                self.logClass(2, "(" + str(self.device_nummer)
                                              + ") " + self.device_name +
                                              " Mindesteinschaltdauer" +
                                              "  erreicht, schalte aus")
                                self.turndevicerelais(0, 0, 1)
                                return
                            else:
                                self.logClass(2, "(" + str(self.device_nummer)
                                              + ") " + self.device_name +
                                              " Mindesteinschaltdauer erreicht"
                                              + ",Ausschaltschwelle 0 gesetzt")
                                work_ausschaltverzoegerung = 0
                                if (work_ausschaltschwelle < 0):
                                    work_ausschaltschwelle = 0
                        else:
                            self.logClass(2, "(" + str(self.device_nummer) +
                                          ") " + self.device_name +
                                          " Mindesteinschaltdauer nicht" +
                                          " erreicht, " +
                                          str(self._device_mineinschaltdauer) +
                                          " > " + str(timesta))
                    else:
                        if self._device_deactivatewhileevcharging == 2:
                            self.logClass(2, "(" + str(self.device_nummer) +
                                          ") " + self.device_name +
                                          " Mindesteinschaltdauer nicht" +
                                          " bekannt,schalte aus")
                            self.turndevicerelais(0, 0, 1)
                            return
                        else:
                            self.logClass(2, "(" + str(self.device_nummer) +
                                          ") " + self.device_name +
                                          " Mindesteinschaltdauer nicht" +
                                          " bekannt,setze Ausschaltschwelle" +
                                          " auf 0")
                            work_ausschaltverzoegerung = 0
                            if (work_ausschaltschwelle < 0):
                                work_ausschaltschwelle = 0
                else:
                    self.logClass(2, "(" + str(self.device_nummer) + ") " +
                                  self.device_name +
                                  " Ladung läuft nicht, pruefe weiter")
            else:
                if self._device_deactivatewhileevcharging == 2:
                    self.logClass(2, "(" + str(self.device_nummer) + ") " +
                                  self.device_name +
                                  " Soll nicht eingeschaltet werden bei" +
                                  " Ladung, pruefe " + str(testcharge))
                    if chargestatus == 1:
                        self.logClass(2, "(" + str(self.device_nummer) + ") "
                                      + self.device_name + " Ladung läuft, " +
                                      "wird nicht eingeschaltet")
                        return
        # Auto ladung ende
        # Art vom ueberschussberechnung pruefen
        if (self._device_speichersocbeforestart == 0):
            # Berechnung aus, Ueberschuss mit Speicher nehmen
            self.devuberschuss = self._uberschuss
            newueberschussberechnung = 1
        else:
            if ((speichersoc < self._device_speichersocbeforestart) and
               (speichersoc < 97)):
                # unter dem Speicher soc, nur EVU Ueberschuss
                # Berechnung mit Ueberschuss nur mit Speicherentladung
                self.devuberschuss = self._uberschussoffset
                newueberschussberechnung = 2
            else:
                # sonst drueber oder gleich Speicher soc Berechnung
                # mit Ueberschuss mit Speicher nehmen
                # oder nehmen wenn speicher fast voll
                self.devuberschuss = self._uberschuss
                newueberschussberechnung = 1
        if (self.ueberschussberechnung != newueberschussberechnung):
            self.ueberschussberechnung = newueberschussberechnung
            self.logClass(2, "(" + str(self.device_nummer) + ") " +
                          self.device_name + " SoC " + str(speichersoc) +
                          " Einschalt SoC " +
                          str(self._device_speichersocbeforestart) +
                          " Ueberschuss " + str(self.devuberschuss))
            self.logClass(2, "(" + str(self.device_nummer) + ") " +
                          self.device_name +
                          " Ueberschussberechnung anders (1 = mit Speicher," +
                          " 2 = mit Offset) " +
                          str(self.ueberschussberechnung))
        if (self.devstatus == 20):
            self.logClass(2, "(" + str(self.device_nummer) + ") " +
                          self.device_name +
                          " Anlauferkennung immer noch aktiv, keine Ueberprüf"
                          + "ung auf Einschalt oder Ausschaltschwelle ")
            return
        # Device mit Anlauferkennung (mehrfach pro tag)
        # welches im PV Modus ist ?
        if ((self.devstatus == 10) and (self._device_startupmuldetection == 1)
           and (self._device_startupdetection == 1)
           and (int(self.oncountnor) > 0)):
            if (self._c_eintime_f == 'Y'):
                timesta = int(time.time()) - int(self._c_eintime)
                if (self._device_mineinschaltdauer < timesta):
                    self.logClass(2, "(" + str(self.device_nummer) + ") "
                                  + self.device_name +
                                  " Mindesteinschaltdauer erreicht," +
                                  " restarte Anlauferkennung ")
                    self._c_eintime_f = 'N'
                    self.devstatus = 20
                    self.oncntstandby = str("0")
                    self.oncountnor = str("0")
                    self.logClass(2, "(" + str(self.device_nummer) + ") " +
                                  self.device_name +
                                  " Anlauferkennung nun aktiv, eingeschaltet ")
                    self.turndevicerelais(1, 0, 0)
                    return
            else:
                self.logClass(2, "(" + str(self.device_nummer) + ") " +
                              self.device_name +
                              " Mindesteinschaltdauer nicht bekannt" +
                              " restarte Anlauferkennung ")
                self.devstatus = 20
                self.oncntstandby = str("0")
                self.oncountnor = str("0")
                self.logClass(2, "(" + str(self.device_nummer) + ") " +
                              self.device_name +
                              " Anlauferkennung nun aktiv, eingeschaltet ")
                self.turndevicerelais(1, 0, 0)
                return
        if ((self.devuberschuss > self._device_einschaltschwelle)
           or (onnow == 1)):
            self._c_ausverz_f = 'N'
            self.logClass(2, "(" + str(self.device_nummer) + ") " +
                          str(self.device_name) + " Überschuss " +
                          str(self.devuberschuss) + " größer Einschaltschwelle"
                          + " oder Immer an zeit erreicht " +
                          str(self._device_einschaltschwelle))
            if (self.relais == 0):
                self.logClass(2, "(" + str(self.device_nummer) + ") " +
                              self.device_name + " SoC " + str(speichersoc) +
                              " Einschalt SoC " +
                              str(self._device_speichersocbeforestart) +
                              " Ueberschuss " + str(self.devuberschuss))
                self.logClass(2, "(" + str(self.device_nummer) + ") " +
                              self.device_name + " Ueberschussberechnung (1 ="
                              + " mit Speicher, 2 = mit Offset) " +
                              str(self.ueberschussberechnung))
                if (self._device_starttime != '00:00'):
                    starthour = int(str("0") +
                                    str(self._device_starttime).
                                    partition(':')[0])
                    startminute = int(str(self._device_starttime)[-2:])
                    self.logClass(2, "(" + str(self.device_nummer) + ") " +
                                  self.device_name +
                                  " Fruehster Start um definiert " +
                                  str(starthour) + ":" +
                                  str('%.2d' % startminute) +
                                  " aktuelle Zeit " + str(localhour) + ":" +
                                  str('%.2d' % localminute))
                    if ((starthour > localhour) or ((starthour == localhour)
                       and (startminute >= localminute))):
                        self.logClass(2, "(" + str(self.device_nummer) + ") " +
                                      self.device_name +
                                      " Fruehster Start noch nicht erreicht ")
                        return
                if (self._device_endtime != '00:00'):
                    endhour = int(str("0") +
                                  str(self._device_endtime).partition(':')[0])
                    endminute = int(str(self._device_endtime)[-2:])
                    self.logClass(2, "(" + str(self.device_nummer) + ") " +
                                  self.device_name +
                                  " Spaetester Start um definiert " +
                                  str(endhour) + ":" + str('%.2d' % endminute)
                                  + " aktuelle Zeit " + str(localhour) + ":"
                                  + str('%.2d' % localminute))
                    if ((endhour > localhour) or ((endhour == localhour)
                       and (endminute >= localminute))):
                        pass
                    else:
                        self.logClass(2, "(" + str(self.device_nummer) + ") " +
                                      self.device_name +
                                      " Spaetester Start vorbei ")
                        return
                if (self._c_einverz_f == 'Y'):
                    timesince = int(time.time()) - int(self._c_einverz)
                    if (self._device_einschaltverzoegerung < timesince):
                        self.logClass(2, "(" + str(self.device_nummer) + ") "
                                      + self.device_name +
                                      " Einschaltverzögerung erreicht, " +
                                      "schalte ein " +
                                      str(self._device_einschaltschwelle))
                        self.turndevicerelais(1, self.ueberschussberechnung, 1)
                        self._c_einverz_f = 'N'
                    else:
                        self.logClass(2, "(" + str(self.device_nummer) + ") " +
                                      self.device_name +
                                      " Einschaltverzögerung nicht erreicht. "
                                      + str(self._device_einschaltverzoegerung)
                                      + " > " + str(timesince))
                else:
                    self._c_einverz_f = 'Y'
                    self._c_einverz = int(time.time())
                    self.logClass(2, "(" + str(self.device_nummer) + ") " +
                                  self.device_name +
                                  " Einschaltverzögerung gestartet")
            else:
                self.logClass(2, "(" + str(self.device_nummer) + ") " +
                              self.device_name +
                              " Einschaltverzögerung erreicht, bereits ein")
                self._c_einverz_f = 'N'
        else:
            self._c_einverz_f = 'N'
            if (self.devuberschuss < work_ausschaltschwelle):
                if (speichersoc > self._device_speichersocbeforestop):
                    self.logClass(2, "(" + str(self.device_nummer) + ") " +
                                  self.device_name +
                                  " SoC höher als Abschalt SoC," +
                                  " lasse Gerät weiterlaufen")
                    return
                else:
                    self.logClass(2, "(" + str(self.device_nummer) + ") " +
                                  self.device_name +
                                  " SoC niedriger als Abschalt SoC," +
                                  " prüfe weiter")
                self.logClass(2, "(" + str(self.device_nummer) + ") " +
                              self.device_name + " Überschuss " +
                              str(self.devuberschuss) +
                              " kleiner Ausschaltschwelle " +
                              str(work_ausschaltschwelle))
                if (self.relais == 1):
                    if (self._c_ausverz_f == 'Y'):
                        timesince = int(time.time()) - int(self._c_ausverz)
                        if (work_ausschaltverzoegerung < timesince):
                            if (self._c_eintime_f == 'Y'):
                                timesta = int((time.time()) -
                                              int(self._c_eintime))
                                if (self._device_mineinschaltdauer < timesta):
                                    self.logClass(2, "(" +
                                                  str(self.device_nummer) +
                                                  ") " + self.device_name +
                                                  " Ausschaltverzögerung &" +
                                                  " Mindesteinschaltdauer " +
                                                  "erreicht, schalte aus " +
                                                  str(work_ausschaltschwelle))
                                    self.turndevicerelais(0, 0, 1)
                                    self._c_ausverz_f = 'N'
                                else:
                                    s1 = str(self._device_mineinschaltdauer)
                                    self.logClass(2, "(" +
                                                  str(self.device_nummer) +
                                                  ") " + self.device_name +
                                                  " Ausschaltverzögerung errei"
                                                  + "cht, Mindesteinschalt" +
                                                  "dauer nicht erreicht, " +
                                                  s1 + " > " + str(timesta))
                            else:
                                self.logClass(2, "(" + str(self.device_nummer)
                                              + ") " + self.device_name +
                                              " Mindesteinschaltdauer nicht" +
                                              " bekannt, schalte aus")
                                self.turndevicerelais(0, 0, 1)
                        else:
                            self.logClass(2, "(" + str(self.device_nummer) +
                                          ") " + self.device_name +
                                          " Ausschaltverzögerung nicht" +
                                          " erreicht. " +
                                          str(work_ausschaltverzoegerung) +
                                          " > " + str(timesince))
                    else:
                        self.logClass(2, "(" + str(self.device_nummer) + ") " +
                                      self.device_name +
                                      " Ausschaltverzögerung gestartet ")
                        self._c_ausverz_f = 'Y'
                        self._c_ausverz = int(time.time())

                else:
                    self.logClass(2, "(" + str(self.device_nummer) + ") " +
                                  self.device_name +
                                  " Ausschaltverzögerung erreicht,bereits aus")
                    self._c_ausverz_f = 'N'
            else:
                self.logClass(2, "(" + str(self.device_nummer) + ") " +
                              self.device_name + " Überschuss kleiner als" +
                              " Einschaltschwelle und größer als " +
                              "Ausschaltschwelle. Ueberschuss " +
                              str(self.devuberschuss))
                self._c_einverz_f = 'N'
                self._c_ausverz_f = 'N'

    def simcount(self, watt2, pref, importfn, exportfn, nummer, wattks):
        # Zaehler mitgeliefert in WH , zurueckrechnen fuer simcount
        if wattks > 0:
            wattposkh = wattks
            wattnegkh = 0
            wattposh = wattks * 3600
            wattnegh = 0
            f = open(self._basePath+'/ramdisk/'+pref+'watt0pos', 'w')
            f.write(str(wattposh))
            f.close()
            self._wpos = wattposh
            f = open(self._basePath+'/ramdisk/'+pref+'watt0neg', 'w')
            f.write(str(wattnegh))
            f.close()
            f = open(self._basePath+'/ramdisk/' + importfn, 'w')
            #    f = open(basePath+'/ramdisk/speicherikwh', 'w')
            self._wh = round(wattposkh, 2)
            f.write(str(round(wattposkh, 2)))
            f.close()
            f = open(self._basePath+'/ramdisk/' + exportfn, 'w')
            #   f = open(basePath+'/ramdisk/speicherekwh', 'w')
            f.write(str(wattnegkh))
            f.close()
            return
        # emulate import  export
        seconds2 = time.time()
        watt1 = 0
        seconds1 = 0.0
        if os.path.isfile(self._basePath+'/ramdisk/'+pref+'sec0'):
            f = open(self._basePath+'/ramdisk/'+pref+'sec0', 'r')
            seconds1 = float(f.read())
            f.close()
            f = open(self._basePath+'/ramdisk/'+pref+'wh0', 'r')
            watt1 = int(f.read())
            f.close()
            f = open(self._basePath+'/ramdisk/'+pref+'watt0pos', 'r')
            wattposh = int(f.read())
            f.close()
            f = open(self._basePath+'/ramdisk/'+pref+'watt0neg', 'r')
            wattnegh = int(f.read())
            f.close()
            f = open(self._basePath+'/ramdisk/'+pref+'sec0', 'w')
            value1 = "%22.6f" % seconds2
            f.write(str(value1))
            f.close()
            f = open(self._basePath+'/ramdisk/'+pref+'wh0', 'w')
            f.write(str(watt2))
            f.close()
            seconds1 = seconds1 + 1
            deltasec = seconds2 - seconds1
            deltasectrun = int(deltasec * 1000) / 1000
            stepsize = int((watt2-watt1)/deltasec)
            while seconds1 <= seconds2:
                if watt1 < 0:
                    wattnegh = wattnegh + watt1
                else:
                    wattposh = wattposh + watt1
                watt1 = watt1 + stepsize
                if stepsize < 0:
                    watt1 = max(watt1, watt2)
                else:
                    watt1 = min(watt1, watt2)
                seconds1 = seconds1 + 1
            rest = deltasec - deltasectrun
            seconds1 = seconds1 - 1 + rest
            if rest > 0:
                watt1 = int(watt1 * rest)
                if watt1 < 0:
                    wattnegh = wattnegh + watt1
                else:
                    wattposh = wattposh + watt1
            wattposkh = wattposh/3600
            wattnegkh = (wattnegh*-1)/3600
            f = open(self._basePath+'/ramdisk/'+pref+'watt0pos', 'w')
            f.write(str(wattposh))
            f.close()
            self._wpos = wattposh
            f = open(self._basePath+'/ramdisk/'+pref+'watt0neg', 'w')
            f.write(str(wattnegh))
            f.close()
            f = open(self._basePath+'/ramdisk/' + importfn, 'w')
            #    f = open(basePath+'/ramdisk/speicherikwh', 'w')
            self._wh = round(wattposkh, 2)
            f.write(str(round(wattposkh, 2)))
            f.close()
            f = open(self._basePath+'/ramdisk/' + exportfn, 'w')
            #   f = open(basePath+'/ramdisk/speicherekwh', 'w')
            f.write(str(wattnegkh))
            f.close()
        else:
            f = open(self._basePath+'/ramdisk/'+pref+'sec0', 'w')
            value1 = "%22.6f" % seconds2
            f.write(str(value1))
            f.close()
            f = open(self._basePath+'/ramdisk/'+pref+'wh0', 'w')
            f.write(str(watt2))
            f.close()

    def getwatt(self, uberschuss, uberschussoffset):
        self.prewatt(uberschuss, uberschussoffset)
        self.newwatt = 0
        self.newwattk = 0
        self.relais = 0
        self.postwatt()

    def turndevicerelais(self, zustand, ueberschussberechnung, updatecnt):
        pass
