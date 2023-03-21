import json
import time
import logging
log = logging.getLogger(__name__)


class Sbase0:
    _basePath = '/var/www/html/openWB'
    _prefixpy = _basePath+'/packages/modules/smarthome/'

    def readret(self):
        with open(self._basePath+'/ramdisk/smarthome_device_ret' +
                  str(self.device_nummer), 'r') as f1:
            answer = json.loads(json.load(f1))
        return answer

    def checkbefsend(self):
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

    def checksend(self, answer):
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
