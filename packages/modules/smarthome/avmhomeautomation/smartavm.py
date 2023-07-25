#!/usr/bin/python3
from smarthome.smartbase import Sbase, Slavm
from typing import Dict
import logging
log = logging.getLogger(__name__)


class Savm(Sbase):
    def __init__(self) -> None:
        # setting
        super().__init__()
        self._old_measuretype0 = 'none'
        self._device_actor = 'none'
        self._device_username = 'none'
        self._device_password = 'none'

    def getwatt(self, uberschuss: int, uberschussoffset: int) -> None:
        self.prewatt(uberschuss, uberschussoffset)
        self._mydevicemeasure0.devuberschuss = self.devuberschuss
        self._mydevicemeasure0.getwattread()
        self.newwatt = self._mydevicemeasure0.newwatt
        self.newwattk = self._mydevicemeasure0.newwattk
        self.relais = self._mydevicemeasure0.relais

        self.postwatt()

    def updatepar(self,  input_param: Dict[str, str]) -> None:
        super().updatepar(input_param)
        self._smart_paramadd = input_param.copy()
        self.device_nummer = int(self._smart_paramadd.get('device_nummer',
                                                          '0'))
        for key, value in self._smart_paramadd.items():
            if (key == 'device_actor'):
                self._device_actor = value
            elif (key == 'device_username'):
                self._device_username = value
            elif (key == 'device_password'):
                self._device_password = value
            else:
                log.info("(" + str(self.device_nummer) + ") " +
                         " AVM überlesen " + key +
                         " " + value)

        if (self._old_measuretype0 == 'none'):
            self._mydevicemeasure0 = Slavm()
            self._old_measuretype0 = 'avm'
            log.info("(" + str(self.device_nummer) +
                     ") Integrierte Leistungsmessung. Neues Measure" +
                     " device erzeugt " + self.device_type)
        else:
            log.info("(" + str(self.device_nummer) +
                     ") Integrierte Leistungsmessung. Nur Parameter" +
                     " update " + self.device_type)
        self._mydevicemeasure0.updatepar(input_param)

    def turndevicerelais(self, zustand: int, ueberschussberechnung: int, updatecnt: int) -> None:
        self.preturn(zustand, ueberschussberechnung, updatecnt)
        if (zustand == 1):
            pname = "/on.py"
        else:
            pname = "/off.py"

        argumentList = ['python3', self._prefixpy + 'avmhomeautomation'
                        + pname,
                        str(self.device_nummer), str(self._device_ip),
                        '0', '0',
                        self._device_actor,
                        self._device_username,
                        self._device_password]
        try:
            self.callpro(argumentList)
        except Exception as e1:
            log.warning("(" + str(self.device_nummer) +
                        ") on / off %s %d %s Fehlermeldung: %s "
                        % ('avm', self.device_nummer,
                           str(self._device_ip), str(e1)))
