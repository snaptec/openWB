#!/usr/bin/python3
from smarthome.smartbase import Sbase, Slhttp
from typing import Dict
import logging
log = logging.getLogger(__name__)


class Shttp(Sbase):
    def __init__(self) -> None:
        # setting
        super().__init__()
        self._old_measuretype0 = 'none'
        self._device_einschalturl = 'none'
        self._device_ausschalturl = 'none'

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
            #    try:
            #        valueint = int(value)
            #    except Exception:
            #        valueint = 0
            if (key == 'device_nummer'):
                pass
            elif (key == 'device_einschalturl'):
                self._device_einschalturl = value
            elif (key == 'device_ausschalturl'):
                self._device_ausschalturl = value
            else:
                log.info("(" + str(self.device_nummer) + ") " +
                         " http überlesen " + key +
                         " " + value)
        if (self._old_measuretype0 == 'none'):
            self._mydevicemeasure0 = Slhttp()
            self._old_measuretype0 = 'http'
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
            url = self._device_einschalturl
        else:
            pname = "/off.py"
            url = self._device_ausschalturl

        argumentList = ['python3', self._prefixpy + 'http' + pname,
                        str(self.device_nummer), '0',
                        str(self.devuberschuss), url]
        try:
            self.callpro(argumentList)
        except Exception as e1:
            log.warning("(" + str(self.device_nummer) +
                        ") on / off %s %d %s Fehlermeldung: %s "
                        % ('Http', self.device_nummer,
                           str(self._device_ip), str(e1)))
