#!/usr/bin/python3
from smarthome.smartbase import Sbase
from typing import Dict
import logging
log = logging.getLogger(__name__)


class Snxdacxx(Sbase):
    def __init__(self) -> None:
        # setting
        super().__init__()
        self._smart_paramadd = {}  # type: dict [str,str]
        self._device_nxdacxxueb = 0
        self._device_nxdacxxtype = 0
        self.device_nummer = 0
        self._dynregel = 1

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
            elif (key == 'device_nxdacxxueb'):
                self._device_nxdacxxueb = valueint
            elif (key == 'device_nxdacxxtype'):
                self._device_nxdacxxtype = valueint
            else:
                log.warning("(" + str(self.device_nummer) + ") " +
                            "Snxdacxx überlesen " + key +
                            " " + value)

    def getwatt(self, uberschuss: int, uberschussoffset: int) -> None:
        self.prewatt(uberschuss, uberschussoffset)
        forcesend = self.checkbefsend()
        argumentList = ['python3', self._prefixpy + 'nxdacxx/watt.py',
                        str(self.device_nummer), str(self._device_ip),
                        str(self.devuberschuss),
                        str(self._device_nxdacxxueb), str(forcesend),
                        str(self._device_dacport),
                        str(self._device_nxdacxxtype),
                        str(self.newwatt)]
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
                        % (' Dac ', self.device_nummer,
                           str(self._device_ip), str(e1)))
        self.postwatt()

    def turndevicerelais(self, zustand: int, ueberschussberechnung: int, updatecnt: int) -> None:
        self.preturn(zustand, ueberschussberechnung, updatecnt)
        if (zustand == 1):
            pname = "/on.py"
        else:
            pname = "/off.py"
        argumentList = ['python3', self._prefixpy + 'nxdacxx' + pname,
                        str(self.device_nummer), str(self._device_ip),
                        str(self.devuberschuss),
                        str(self._device_dacport),
                        str(self._device_nxdacxxtype)]
        try:
            self.callpro(argumentList)
        except Exception as e1:
            log.warning("(" + str(self.device_nummer) +
                        ") on / off  %s %d %s Fehlermeldung: %s "
                        % ('Dac ', self.device_nummer,
                           str(self._device_ip), str(e1)))
