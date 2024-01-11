#!/usr/bin/python3
from smarthome.smartbase import Sbase, Slshelly
from typing import Dict
import logging
log = logging.getLogger(__name__)


class Sshelly(Sbase):
    def __init__(self) -> None:
        # setting
        super().__init__()
        self._old_measuretype0 = 'none'
        self._device_shpassword = 'none'
        self._device_shusername = 'none'
        self._device_shauth = 0

    def getwatt(self, uberschuss: int, uberschussoffset: int) -> None:
        self.prewatt(uberschuss, uberschussoffset)
        self._mydevicemeasure0.devuberschuss = self.devuberschuss
        self._mydevicemeasure0.getwattread()
        self.newwatt = self._mydevicemeasure0.newwatt
        self.newwattk = self._mydevicemeasure0.newwattk
        self.relais = self._mydevicemeasure0.relais
        self.temp0 = self._mydevicemeasure0.temp0
        self.temp1 = self._mydevicemeasure0.temp1
        self.temp2 = self._mydevicemeasure0.temp2
        self.postwatt()

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
            if (key == 'device_shusername'):
                self._device_shusername = value
            elif (key == 'device_shpassword'):
                self._device_shpassword = value
            elif (key == 'device_shauth'):
                self._device_shauth = valueint
            else:
                log.info("(" + str(self.device_nummer) + ") Sshelly überlesen " + key +
                         " " + value)
        if (self._old_measuretype0 == 'none'):
            self._mydevicemeasure0 = Slshelly()
            self._old_measuretype0 = 'shelly'
            log.info("(" + str(self.device_nummer) +
                     ") Integrierte Leistungsmessung. Neues Measure" +
                     " device erzeugt " + self.device_type)
        else:
            log.info("(" + str(self.device_nummer) +
                     ") Integrierte Leistungsmessung. Nur Parameter " +
                     " update " + self.device_type)
        self._mydevicemeasure0.updatepar(input_param)

    def turndevicerelais(self, zustand: int, ueberschussberechnung: int, updatecnt: int) -> None:
        self.preturn(zustand, ueberschussberechnung, updatecnt)
        if (zustand == 1):
            pname = "/on.py"
        else:
            pname = "/off.py"

        argumentList = ['python3', self._prefixpy + 'shelly' + pname,
                        str(self.device_nummer), str(self._device_ip), '0',
                        str(self._device_chan),
                        str(self._device_shauth),
                        self._device_shusername,
                        self._device_shpassword]
        try:
            self.callpro(argumentList)
        except Exception as e1:
            log.warning("(" + str(self.device_nummer) +
                        ") on / off %s %d %s Fehlermeldung: %s "
                        % ('Shelly', self.device_nummer,
                           str(self._device_ip), str(e1)))
