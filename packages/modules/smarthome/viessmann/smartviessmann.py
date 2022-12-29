#!/usr/bin/python3
from smarthome.smartbase import Sbase
from smarthome.global0 import log
import subprocess
import json


class Sviessmann(Sbase):
    def __init__(self):
        # setting
        super().__init__()
        print('__init__ Sviessmann executed')

    def getwatt(self, uberschuss, uberschussoffset):
        self.prewatt(uberschuss, uberschussoffset)
        argumentList = ['python3', self._prefixpy + 'viessmann/watt.py',
                        str(self.device_nummer), str(self._device_ip),
                        str(self.devuberschuss)]
        try:
            self.proc = subprocess.Popen(argumentList)
            self.proc.communicate()
            self.f1 = open(self._basePath+'/ramdisk/smarthome_device_ret' +
                           str(self.device_nummer), 'r')
            self.answerj = json.load(self.f1)
            self.f1.close()
            self.answer = json.loads(self.answerj)
            self.newwatt = int(self.answer['power'])
            self.newwattk = int(self.answer['powerc'])
            self.relais = int(self.answer['on'])
        except Exception as e1:
            log.warning("(" + str(self.device_nummer) +
                        ") Leistungsmessung %s %d %s Fehlermeldung: %s "
                        % ('viessmann', self.device_nummer,
                           str(self._device_ip), str(e1)))
        self.postwatt()

    def turndevicerelais(self, zustand, ueberschussberechnung, updatecnt):
        self.preturn(zustand, ueberschussberechnung, updatecnt)
        if (zustand == 1):
            pname = "/on.py"
        else:
            pname = "/off.py"
        argumentList = ['python3', self._prefixpy + 'viessmann ' + pname,
                        str(self.device_nummer), str(self._device_ip),
                        str(self.devuberschuss)]
        try:
            self.proc = subprocess.Popen(argumentList)
            self.proc.communicate()
        except Exception as e1:
            log.warning("(" + str(self.device_nummer) +
                        ") on / off  %s %d %s Fehlermeldung: %s "
                        % ('viessmann ', self.device_nummer,
                           str(self._device_ip), str(e1)))
