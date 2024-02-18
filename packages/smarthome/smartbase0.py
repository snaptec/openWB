import json
import time
import os
import subprocess
import logging
from typing import Any, Dict
from typing import List
log = logging.getLogger(__name__)


class Sbase0:
    _basePath = '/var/www/html/openWB'
    _prefixpy = _basePath+'/packages/modules/smarthome/'

    def readret(self) -> Dict[str, Any]:
        with open(self._basePath+'/ramdisk/smarthome_device_ret' +
                  str(self.device_nummer), 'r') as f1:
            answer = json.loads(json.load(f1))
        return answer

    def __init__(self) -> None:
        # setting
        super().__init__()
        self.mqtt_param = {}  # type: Dict[str, str]
        self.mqtt_param_del = {}  # type: Dict[str, str]
        self.device_name = 'none'
        self.devstatus = 10
        # (10 = ueberschuss gesteuert oder manual,
        # 20 = Anlauferkennung aktiv
        # (ausschalten wenn Leistungsaufnahme > Schwelle)
        #  30 = gestartet um fertig bis zu erreichen
        # default 10
        self._first_run = 1
        self.chargestatus = False
        self.device_nummer = 0
        self.temp0 = '300'
        self.temp1 = '300'
        self.temp2 = '300'
        self.newwatt = 0
        self.newwattk = 0
        self.newwattks = 0
        self.pvwatt = 0
        self.relais = 0
        self.devuberschuss = 0
        self.device_temperatur_configured = 0
        self.ueberschussberechnung = 1
        self.abschalt = 0
        self.device_homeconsumtion = 0
        self.device_manual = 0
        self.device_manual_control = 0
        self.newdevice_manual = 0
        self.newdevice_manual_control = 0
        self.device_type = 'none'
        self._smart_param = {}  # type: Dict[str, str]
        self._uberschussoffset = 0
        self._uberschuss = 0
        self.device_canswitch = 0
        self._device_deactivatewhileevcharging = 0
        self._device_mineinschaltdauer = 0
        self._device_mindayeinschaltdauer = 0
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
        self._device_measureportsdm = 8899
        self._device_dacport = 8899
        self._device_measureid = 0
        self._device_finishtime = '00:00'
        self._device_starttime = '00:00'
        self._device_endtime = '00:00'
        self._device_ontime = '00:00'
        self._device_offtime = '00:00'
        self._device_onuntiltime = '00:00'
        self._device_nonewatt = 0
        self._device_deactivateper = 0
        self._device_pbtype = 'none'
        self._device_lambdaueb = 'UP'
        self._old_pbtype = 'none'
        self._mydevicepb = 'none'  # type: Any
        self._oldrelais = 2
        self._oldwatt = 0
        self._device_chan = 0
        self._device_updatesec = 0
        # mqtt per
        self._whimported_tmp = 0
        self.runningtime = 0
        self.oncountnor = '0'
        self.oncntstandby = '0'
        self._wh = 0
        self._wpos = 0
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
        self._c_updatetime = 0
        self._seclastup = 0
        self._dynregel = 0
        self.device_setauto = 0
        self.gruppe = 'none'
        self.btchange = 0
        self._mydevicemeasure = 'none'  # type: Any
        self.device_nummer = 0

    def checkbefsend(self) -> int:
        newtime = int(time.time())
        if (self._c_updatetime == 0):
            self._c_updatetime = newtime - 180
        self._seclastup = newtime - int(self._c_updatetime)
        # forcesend = 0 default acthor time period applies
        # forcesend = 1 default overwritten send now
        # forcesend = 9 default overwritten no send
        if (self._device_updatesec == 0):
            forcesend = 0
        else:
            if (self._seclastup > self._device_updatesec):
                forcesend = 1
            else:
                forcesend = 9
        return forcesend

    def checksend(self, answer: Any) -> None:
        try:
            send = int(answer['send'])
            sendpower = int(answer['sendpower'])
            if (send == 1):
                self._c_updatetime = int(time.time())
                log.info("(" + str(self.device_nummer) +
                         ") Gerät wurde upgedatet, " +
                         "neue Vorgabe %s Periode %s"
                         % (str(sendpower), str(self._seclastup)))
        except Exception as e1:
            log.warning("(" + str(self.device_nummer) +
                        ") checksend Fehlermeldung: %s "
                        % (str(e1)))

    def callpro(self, argumentList: List[str]) -> None:
        try:
            my_env = os.environ.copy()
            my_env["PYTHONPATH"] = "/var/www/html/openWB/packages"
            proc = subprocess.Popen(argumentList, stderr=subprocess.PIPE,
                                    universal_newlines=True, env=my_env)
            _, errs = proc.communicate()
            if errs:
                log.error("%s" % (errs))
        except Exception:
            log.exception("Subprocess Fehlermeldung: argumentList %s " % argumentList[1])
