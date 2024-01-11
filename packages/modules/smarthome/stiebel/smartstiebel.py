#!/usr/bin/python3
from smarthome.smartbase import Sbase
import logging
log = logging.getLogger(__name__)


class Sstiebel(Sbase):
    def __init__(self) -> None:
        # setting
        super().__init__()

    def getwatt(self, uberschuss: int, uberschussoffset: int) -> None:
        self.prewatt(uberschuss, uberschussoffset)
        argumentList = ['python3', self._prefixpy + 'stiebel/watt.py',
                        str(self.device_nummer), str(self._device_ip),
                        str(self.devuberschuss)]
        try:
            self.callpro(argumentList)
            self.answer = self.readret()
            self.newwatt = int(self.answer['power'])
            self.newwattk = int(self.answer['powerc'])
            self.relais = int(self.answer['on'])
        except Exception as e1:
            log.warning("(" + str(self.device_nummer) +
                        ") Leistungsmessung %s %d %s Fehlermeldung: %s "
                        % ('Stiebel', self.device_nummer,
                           str(self._device_ip), str(e1)))
        self.postwatt()

    def turndevicerelais(self, zustand: int, ueberschussberechnung: int, updatecnt: int) -> None:
        self.preturn(zustand, ueberschussberechnung, updatecnt)
        if (zustand == 1):
            pname = "/on.py"
        else:
            pname = "/off.py"
        argumentList = ['python3', self._prefixpy + 'stiebel' + pname,
                        str(self.device_nummer), str(self._device_ip),
                        str(self.devuberschuss)]
        try:
            self.callpro(argumentList)
        except Exception as e1:
            log.warning("(" + str(self.device_nummer) +
                        ") on / off  %s %d %s Fehlermeldung: %s "
                        % ('Stiebel', self.device_nummer,
                           str(self._device_ip), str(e1)))
