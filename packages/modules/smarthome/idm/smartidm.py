#!/usr/bin/python3
from smarthome.smartbase import Sbase
from typing import Dict
import logging
log = logging.getLogger(__name__)


class Sidm(Sbase):
    def __init__(self) -> None:
        # setting
        super().__init__()
        self._device_idmnav = '2'
        self.device_nummer = 0
        self._device_idmueb = 'UZ'
        self._device_maxueb = 0

    def updatepar(self, input_param: Dict[str, str]) -> None:
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
            elif (key == 'device_idmnav'):
                self._device_idmnav = value
            elif (key == 'device_idmueb'):
                self._device_idmueb = value
            elif (key == 'device_maxueb'):
                self._device_maxueb = valueint
            else:
                log.info("(" + str(self.device_nummer) + ") " +
                         " IDM überlesen " + key +
                         " " + value)

    def getwatt(self, uberschuss: int, uberschussoffset: int) -> None:
        self.prewatt(uberschuss, uberschussoffset)
        forcesend = self.checkbefsend()
        argumentList = ['python3', self._prefixpy + 'idm/watt.py',
                        str(self.device_nummer), str(self._device_ip),
                        str(self.devuberschuss), str(self._device_idmnav),
                        str(self.pvwatt),
                        str(self._device_idmueb),
                        str(self._device_maxueb),
                        str(forcesend)]
        try:
            self.callpro(argumentList)
            self.answer = self.readret()
            self.newwatt = int(self.answer['power'])
            self.newwattk = int(self.answer['powerc'])
            self.relais = int(self.answer['on'])
            self.checksend(self.answer)
        except Exception as e1:
            log.warning("(" + str(self.device_nummer) +
                        ") Leistungsmessung %s %d %s Fehlermeldung: %s "
                        % ('idm ', self.device_nummer,
                           str(self._device_ip), str(e1)))
        self.postwatt()

    def turndevicerelais(self, zustand: int, ueberschussberechnung: int, updatecnt: int) -> None:
        self.preturn(zustand, ueberschussberechnung, updatecnt)
        if (zustand == 1):
            pname = "/on.py"
        else:
            pname = "/off.py"
        argumentList = ['python3', self._prefixpy + 'idm' + pname,
                        str(self.device_nummer), str(self._device_ip),
                        str(self.devuberschuss), str(self._device_idmnav)]
        try:
            self.callpro(argumentList)
        except Exception as e1:
            log.warning("(" + str(self.device_nummer) +
                        ") on / off  %s %d %s Fehlermeldung: %s "
                        % ('idm ', self.device_nummer,
                           str(self._device_ip), str(e1)))
