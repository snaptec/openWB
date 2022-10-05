#!/usr/bin/python3
from usmarthome.smartbase import Sbase
from usmarthome.global0 import log
import subprocess


class Snxdacxx(Sbase):
    def __init__(self):
        # setting
        super().__init__()
        print('__init__ Snxdacxx executed')
        self._smart_paramadd = {}
        self._device_nxdacxxueb = 0
        self.device_nummer = 0
        self._dynregel = 1

    def updatepar(self, input_param):
        super().updatepar(input_param)
        self._smart_paramadd = input_param.copy()
        self.device_nummer = int(self._smart_paramadd.get('device_nummer',
                                                          '0'))
        for key, value in self._smart_paramadd.items():
            try:
                valueint = int(value)
            except Exception:
                valueint = 0
            if (key == 'device_nummer'):
                pass
            elif (key == 'device_nxdacxxueb'):
                self._device_nxdacxxueb = valueint
            else:
                log.warning("(" + str(self.device_nummer) + ") " +
                            __class__.__name__ + " überlesen " + key +
                            " " + value)

    def getwatt(self, uberschuss, uberschussoffset):
        self.prewatt(uberschuss, uberschussoffset)
        forcesend = self.checkbefsend()
        argumentList = ['python3', self._prefixpy + 'nxdacxx/watt.py',
                        str(self.device_nummer), str(self._device_ip),
                        str(self.devuberschuss),
                        str(self._device_nxdacxxueb), str(forcesend)]
        try:
            self.proc = subprocess.Popen(argumentList)
            self.proc.communicate()
            self.answer = self.readret()
            self.newwatt = int(self.answer['power'])
            self.newwattk = int(self.answer['powerc'])
            self.relais = int(self.answer['on'])
            self.checksend(self.answer)
        except Exception as e1:
            log.warning("(" + str(self.device_nummer) +
                        ") Leistungsmessung %s %d %s Fehlermeldung: %s "
                        % ('n4dac02 ', self.device_nummer,
                           str(self._device_ip), str(e1)))
        self.postwatt()

    def turndevicerelais(self, zustand, ueberschussberechnung, updatecnt):
        self.preturn(zustand, ueberschussberechnung, updatecnt)
        if (zustand == 1):
            pname = "/on.py"
        else:
            pname = "/off.py"
        argumentList = ['python3', self._prefixpy + 'nxdacxx' + pname,
                        str(self.device_nummer), str(self._device_ip),
                        str(self.devuberschuss)]
        try:
            self.proc = subprocess.Popen(argumentList)
            self.proc.communicate()
        except Exception as e1:
            log.warning("(" + str(self.device_nummer) +
                        ") on / off  %s %d %s Fehlermeldung: %s "
                        % ('n4dac02 ', self.device_nummer,
                           str(self._device_ip), str(e1)))
