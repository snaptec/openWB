#!/usr/bin/python3
from smarthome.smartbase import Sbase
from smarthome.global0 import log
import subprocess


class Sratiotherm(Sbase):
    def __init__(self):
        # setting
        super().__init__()
        print('__init__ Sratiotherm executed')

    def getwatt(self, uberschuss, uberschussoffset):
        self.prewatt(uberschuss, uberschussoffset)
        forcesend = self.checkbefsend()
        argumentList = ['python3', self._prefixpy + 'ratiotherm/watt.py',
                        str(self.device_nummer), str(self._device_ip),
                        str(self.devuberschuss),
                        str(forcesend)]
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
                        % ('ratiotherm', self.device_nummer,
                           str(self._device_ip), str(e1)))
        self.postwatt()

    def turndevicerelais(self, zustand, ueberschussberechnung, updatecnt):
        self.preturn(zustand, ueberschussberechnung, updatecnt)
        if (zustand == 1):
            pname = "/on.py"
        else:
            pname = "/off.py"
        argumentList = ['python3', self._prefixpy + 'ratiotherm' + pname,
                        str(self.device_nummer), str(self._device_ip),
                        str(self.devuberschuss)]
        try:
            self.proc = subprocess.Popen(argumentList)
            self.proc.communicate()
        except Exception as e1:
            log.warning("(" + str(self.device_nummer) +
                        ") on / off  %s %d %s Fehlermeldung: %s "
                        % ('ratiotherm', self.device_nummer,
                           str(self._device_ip), str(e1)))
