#!/usr/bin/python3
from smarthome.smartbase import Sbase
from typing import Dict
import logging
log = logging.getLogger(__name__)


class Sacthor(Sbase):
    def __init__(self) -> None:
        # setting
        super().__init__()
        self._smart_paramadd = {}  # type: Dict[str, str]
        self._device_acthortype = 'none'
        self._device_acthorpower = 'none'
        self.device_nummer = 0
        self._dynregel = 1

    def updatepar(self, input_param: Dict[str, str]) -> None:
        super().updatepar(input_param)
        self._smart_paramadd = input_param.copy()
        self.device_nummer = int(self._smart_paramadd.get('device_nummer',
                                                          '0'))
        # fest 3 setzen
        # Wassertemperatur lesen
        # Temp0 Warmwasser 1001
        # Temp1 1030 <- Optional wenn 0, nicht angeschlossen dann ersetzt durch 300 (keine Anzeige)
        # Temp2 1031 <- Optional wenn 0, nicht angeschlossen dann ersetzt durch 300 (keine Anzeige)
        self.device_temperatur_configured = 3
        for key, value in self._smart_paramadd.items():
            if (key == 'device_nummer'):
                pass
            elif (key == 'device_acthortype'):
                self._device_acthortype = value
            elif (key == 'device_acthorpower'):
                self._device_acthorpower = value
            else:
                log.warning("(" + str(self.device_nummer) + ") " +
                            "Sacthor überlesen " + key +
                            " " + value)

    def getwatt(self, uberschuss: int, uberschussoffset: int) -> None:
        self.prewatt(uberschuss, uberschussoffset)
        forcesend = self.checkbefsend()
        argumentList = ['python3', self._prefixpy + 'acthor/watt.py',
                        str(self.device_nummer), str(self._device_ip),
                        str(self.devuberschuss), self._device_acthortype,
                        self._device_acthorpower, str(forcesend),
                        str(self.newwatt), str(self._oldmeasuretype1)]
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
            self.temp1 = str(self.answer['temp1'])
            with open(self._basePath+'/ramdisk/device' +
                      str(self.device_nummer) + '_temp1', 'w') as f:
                f.write(str(self.temp1))
            self.temp2 = str(self.answer['temp2'])
            with open(self._basePath+'/ramdisk/device' +
                      str(self.device_nummer) + '_temp2', 'w') as f:
                f.write(str(self.temp2))
            self.checksend(self.answer)
        except Exception as e1:
            log.warning("(" + str(self.device_nummer) +
                        ") Leistungsmessung %s %d %s Fehlermeldung: %s "
                        % ('Acthor ', self.device_nummer,
                           str(self._device_ip), str(e1)))
        self.postwatt()

    def turndevicerelais(self, zustand: int, ueberschussberechnung: int, updatecnt: int) -> None:
        self.preturn(zustand, ueberschussberechnung, updatecnt)
        if (zustand == 1):
            pname = "/on.py"
        else:
            pname = "/off.py"
        argumentList = ['python3', self._prefixpy + 'acthor' + pname,
                        str(self.device_nummer), str(self._device_ip),
                        str(self.devuberschuss)]
        try:
            self.callpro(argumentList)
        except Exception as e1:
            log.warning("(" + str(self.device_nummer) +
                        ") on / off  %s %d %s Fehlermeldung: %s "
                        % ('Acthor ', self.device_nummer,
                           str(self._device_ip), str(e1)))
