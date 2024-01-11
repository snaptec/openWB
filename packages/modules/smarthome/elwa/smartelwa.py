#!/usr/bin/python3
from smarthome.smartbase import Sbase
from typing import Dict
import logging
log = logging.getLogger(__name__)


class Selwa(Sbase):
    def __init__(self) -> None:
        # setting
        super().__init__()
        self._dynregel = 1

    def updatepar(self, input_param: Dict[str, str]) -> None:
        super().updatepar(input_param)
        # fest 1 setzen Warmwasser modbus 1001
        self.device_temperatur_configured = 1

    def getwatt(self, uberschuss: int, uberschussoffset: int) -> None:
        self.prewatt(uberschuss, uberschussoffset)
        forcesend = self.checkbefsend()
        argumentList = ['python3', self._prefixpy + 'elwa/watt.py',
                        str(self.device_nummer), str(self._device_ip),
                        str(self.devuberschuss), str(forcesend)]
        try:
            self.callpro(argumentList)
            self.answer = self.readret()
            self.newwatt = int(self.answer['power'])
            self.newwattk = int(self.answer['powerc'])
            self.relais = int(self.answer['on'])
            self.temp0 = str(self.answer['temp0'])
            with open(self._basePath+'/ramdisk/device' +
                      str(self.device_nummer) + '_temp0', 'w') as f:
                f.write(str(self.temp0))
            self.checksend(self.answer)
        except Exception as e1:
            log.warning("(" + str(self.device_nummer) +
                        ") Leistungsmessung %s %d %s Fehlermeldung: %s "
                        % ('elwa ', self.device_nummer,
                           str(self._device_ip), str(e1)))
        self.postwatt()

    def turndevicerelais(self, zustand: int, ueberschussberechnung: int, updatecnt: int) -> None:
        self.preturn(zustand, ueberschussberechnung, updatecnt)
        if (zustand == 1):
            pname = "/on.py"
        else:
            pname = "/off.py"
        argumentList = ['python3', self._prefixpy + 'elwa' + pname,
                        str(self.device_nummer), str(self._device_ip),
                        str(self.devuberschuss)]
        try:
            self.callpro(argumentList)
        except Exception as e1:
            log.warning("(" + str(self.device_nummer) +
                        ") on / off  %s %d %s Fehlermeldung: %s "
                        % ('elwa ', self.device_nummer,
                           str(self._device_ip), str(e1)))
