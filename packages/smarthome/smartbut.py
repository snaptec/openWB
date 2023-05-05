from smarthome.smartbase0 import Sbase0
import urllib.request
import json
import logging
log = logging.getLogger(__name__)


class Spbase(Sbase0):
    def __init__(self):
        #
        # setting
        super().__init__()
        self._device_pbip = 'none'
        self.device_nummer = 0

    def updatepar(self, input_param):
        self._smart_param = input_param.copy()
        self.device_nummer = int(self._smart_param.get('device_nummer', '0'))
        for key, value in self._smart_param.items():
            if (key == 'device_pbip'):
                self._device_pbip = value
            else:
                log.info("(" + str(self.device_nummer) + ") "
                         + __class__.__name__ + " überlesen " + key +
                         " " + value)

    def showstat(self, manual, relais):
        pass


class Sbshelly(Spbase):
    def __init__(self):
        # setting
        super().__init__()
        self.counter = 0
        self.led = 9
        self.event_cnt = 0
        self.event = 'none'
        self.oldevent_cnt = 0
        self.oldevent = 'none'

    def showstat(self, manual, relais):
        if (manual == 0):  # automatic mode
            self.pboff()
        else:   # manual mode
            if (relais == 0):
                self.pbon()
            else:
                self.pbblink()

    def checkbut(self, manual, relais, manual_control):
        newmanual = manual
        newmanual_control = manual_control
        try:
            at = str(urllib.request.urlopen("http://" +
                                            str(self._device_pbip)
                                            + "/status",
                                            timeout=3).read().decode("utf-8"))
        except Exception as e1:
            log.warning("Shelly button ch (%d) %s Fehlermeldung: %s "
                        % (self.device_nummer, self._device_pbip, str(e1)))
            return newmanual, newmanual_control
        a = json.loads(at)
        with open(self._basePath+'/ramdisk/smarthome_device_ret' +
                  str(self.device_nummer) + '_shelly_bp', 'w') as f:
            f.write(str(a))
        self.oldevent_cnt = self.event_cnt
        self.oldevent = self.event
        self.event_cnt = int(a['inputs'][0]['event_cnt'])
        self.event = str(a['inputs'][0]['event'])
        if (self.oldevent == 'none'):
            return newmanual, newmanual_control
        if ((self.event == self.oldevent) and
           (self.event_cnt == self.oldevent_cnt)):
            return newmanual, newmanual_control
        log.info("Shelly button pressed (%d) %s %s"
                 % (self.device_nummer, self._device_pbip, self.event))
        # im automatic modus -> ein mal Drücken wechselen auf manual
        if (manual == 0):
            newmanual = 1
            return newmanual, newmanual_control
        # im manual modus  -> ein mal Drücken wechselen  zwischen on und off
        if (self.event == 'S'):
            if (manual_control == 1):
                newmanual_control = 0
            else:
                newmanual_control = 1
            return newmanual, newmanual_control
        # im manual modus  -> mehrmals drücken wechselen auf automat
        newmanual = 0
        return newmanual, newmanual_control

    def pboff(self):
        if (self.led == 0):
            return
        try:
            urllib.request.urlopen("http://" + str(self._device_pbip) +
                                   "/settings?led_status_disable=true",
                                   timeout=3)
            log.info("Shelly button led off (%d) %s"
                     % (self.device_nummer, self._device_pbip))

        except Exception as e1:
            log.warning("Shelly button off (%d) %s Fehlermeldung: %s "
                        % (self.device_nummer, self._device_pbip, str(e1)))
        self.led = 0

    def pbon(self):
        if (self.led == 1):
            return
        try:
            urllib.request.urlopen("http://" + str(self._device_pbip) +
                                   "/settings?led_status_disable=false",
                                   timeout=3)
            log.info("Shelly button led on (%d) %s"
                     % (self.device_nummer, self._device_pbip))
        except Exception as e1:
            log.warning("Shelly button on (%d) %s Fehlermeldung: %s "
                        % (self.device_nummer, self._device_pbip, str(e1)))
        self.led = 1

    def pbblink(self):
        self.counter = self.counter + 1
        if (self.counter < 1):
            return
        self.counter = 0
        if (self.led == 0):
            self.pbon()
        else:
            self.pboff()
