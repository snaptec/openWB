#!/usr/bin/python3
import time
import os
from typing import Dict, Tuple
from smarthome.smartbase0 import Sbase0
from smarthome.smartmeas import Slsdm630, Sllovato, Slsdm120, Slwe514, Slfronius
from smarthome.smartmeas import Sljson, Slsmaem, Slshelly, Sltasmota, Slmqtt
from smarthome.smartmeas import Slhttp, Slavm, Slmystrom, Slb23
from smarthome.smartbut import Sbshelly
from datetime import datetime, timezone
import logging
log = logging.getLogger(__name__)


class Sbase(Sbase0):
    # Instance variablen für ein und Auschaltgruppe
    einschwelle = 0
    einverz = 0
    eindevices = 0
    #
    ausdevices = 0
    ausschaltwatt = 0
    einrelais = 0
    nureinschaltinsec = 0
    eindevstatus = 0

    def __init__(self) -> None:
        # setting
        super().__init__()

    def prewatt(self, uberschuss: int, uberschussoffset: int) -> None:
        self._uberschuss = uberschuss
        self._uberschussoffset = uberschussoffset
        if (self._deviceconfiguredold == "9") and (self._deviceconfigured ==
                                                   "1"):
            if self._device_deactivatewhileevcharging > 0:
                # nach startup alle aktiven devices mit Autoladen aus als
                # other fuehren
                self.c_mantime_f = 'Y'
                self.c_mantime = int(time.time())
            self._deviceconfiguredold = self._deviceconfigured
        self.abschalt = 0
        if self._device_deactivatewhileevcharging > 0:
            if (self._c_eintime_f == 'Y'):
                # alle abschaltbaren devices während mindestlaufzeit
                # als other führen
                timesta = int(time.time()) - self._c_eintime
                if (self._device_mineinschaltdauer < timesta):
                    self.abschalt = 1
                else:
                    self.abschalt = 0
            else:
                self.abschalt = 1
            # prepare end
        self.getueb()

    def postwatt(self) -> None:
        (self.newwatt, self.newwattk) = self.sepwatt(self.newwatt,
                                                     self.newwattk)
        # bei reiner Leistungsmessung relais nur nach Watt setzten
        if ((self.newwatt > self._device_nonewatt)
           and (self.device_type == 'none')):
            self.relais = 1
        # bei laufender Anlauferkennung deivce nicht aktiv setzten
        if (self.relais == 1) and (self.devstatus != 20):
            self.relais = 1
        else:
            self.relais = 0
        self.mqtt_param = {}
        #  pref = 'openWB/SmartHome/Devices/' + str(self.device_nummer) + '/'
        pref = '/' + str(self.device_nummer) + '/'
        self.mqtt_param[pref + 'RelayStatus'] = str(self.relais)
        if (self.c_mantime_f == 'Y') and (self.device_manual != 1):
            # nach Ausschalten manueller Modus mindestens 30 Sek +
            # max( ausschaltverzögerung,mindeseinschaltdauer
            #  als nicht abschaltbarer
            # device fuehren, damit nicht ungewollt pv überwchuss erkannt wird
            manverz = max(self._device_ausschaltverzoegerung,
                          self._device_mineinschaltdauer) + 30
            timesince = int(time.time()) - int(self.c_mantime)
            if (manverz < timesince):
                log.info("(" + str(self.device_nummer) + ") von Manuell "
                         + "auf Automatisch gestellt oder startup,"
                         + " Uebergangsfrist abgelaufen" +
                         self.c_mantime_f)
                self.c_mantime_f = 'N'
            else:
                log.info("(" + str(self.device_nummer) + ") von Manuell" +
                         " auf Automatisch gestellt oder startup," +
                         " Übergangsfrist laueft noch " + str(manverz) +
                         " > " + str(timesince))
                self.abschalt = 0
        self._oldwatt = self.newwatt
        with open(self._basePath+'/ramdisk/device' + str(self.device_nummer) +
                  '_watt', 'w') as f:
            f.write(str(self._oldwatt))
        with open(self._basePath+'/ramdisk/device' + str(self.device_nummer) +
                  '_relais', 'w') as f:
            f.write(str(self.relais))
        try:
            with open(self._basePath+'/ramdisk/smarthome_device_' +
                      str(self.device_nummer) + 'watt0pos', 'r') as value:
                importtemp = int(value.read())
                if (self.newwattk > 0):
                    # Shadow calculation for devices mit gelierten Zaehler (z.b. sdm630)
                    self.newwattks = self.simcount(self._oldwatt, "smarthome_device_" +
                                                   str(self.device_nummer),
                                                   "device" + str(self.device_nummer) + "_wh",
                                                   "device" + str(self.device_nummer) + "_whe",
                                                   str(self.device_nummer), self.newwattk)
                    #                              str(self.device_nummer), 0)
                    # um Simulation zweiter Zaehler zu aktivieren
                    #
                else:
                    # uebernehmen gerechneten Zaehlerstand für alle anderen devices (z.b. shelly)
                    self.newwattk = self.simcount(self._oldwatt, "smarthome_device_" +
                                                  str(self.device_nummer),
                                                  "device" + str(self.device_nummer) + "_wh",
                                                  "device" + str(self.device_nummer) + "_whe",
                                                  str(self.device_nummer), 0)

        except Exception:
            # first run simcount also update
            # add start point for shadow
            importtemp = self._whimported_tmp
            with open(self._basePath+'/ramdisk/smarthome_device_' +
                      str(self.device_nummer) + 'watt0pos', 'w') as f:
                f.write(str(importtemp))
            with open(self._basePath+'/ramdisk/smarthome_device_' +
                      str(self.device_nummer) + 'watt0neg', 'w') as f:
                f.write(str("0"))
            if (self.newwattk > 0):
                log.info("(" + str(self.device_nummer) +
                         ") Simcount Startwert aus Z1 (HW) übernommen " +
                         str(self.newwattk) + " kwh " + str(self.newwattk * 3600) + " wh")
                self.newwattks = self.simcount(self._oldwatt,
                                               "smarthome_device_" +
                                               str(self.device_nummer),
                                               "device" + str(self.device_nummer) + "_wh",
                                               "device" + str(self.device_nummer) + "_whe",
                                               str(self.device_nummer), self.newwattk)
            else:
                log.info("(" + str(self.device_nummer) +
                         ") Simcount Startwert aus mqtt übernommen " +
                         str(self._whimported_tmp) + " wh")
                self.newwattk = int(self.simcount(self._oldwatt, "smarthome_device_" +
                                                  str(self.device_nummer),
                                                  "device" + str(self.device_nummer) + "_wh",
                                                  "device" + str(self.device_nummer) + "_whe",
                                                  str(self.device_nummer), 0))
        if (self.relais == 1):
            newtime = int(time.time())
            if (self.c_oldstampeinschaltdauer_f == 'Y'):
                timediff = newtime - self.c_oldstampeinschaltdauer
                self.runningtime = self.runningtime + int(timediff)
                self.c_oldstampeinschaltdauer = newtime
            else:
                self.c_oldstampeinschaltdauer = newtime
                self.c_oldstampeinschaltdauer_f = 'Y'
        else:
            self.c_oldstampeinschaltdauer = 0
            self.c_oldstampeinschaltdauer_f = 'N'
        self.mqtt_param[pref + 'RunningTimeToday'] = str(self.runningtime)
        # Einschaltzeit des Relais setzen
        if (self._oldrelais == 0):
            if (self.relais == 1):
                self._c_eintime = int(time.time())
                self._c_eintime_f = 'Y'
            else:
                self._c_eintime = 0
                self._c_eintime_f = 'N'
        self._oldrelais = self.relais
        if (self.device_temperatur_configured == 0):
            self.mqtt_param[pref + 'TemperatureSensor0'] = '300'
            self.mqtt_param[pref + 'TemperatureSensor1'] = '300'
            self.mqtt_param[pref + 'TemperatureSensor2'] = '300'
        elif (self.device_temperatur_configured == 1):
            self.mqtt_param[pref + 'TemperatureSensor0'] = self.temp0
            self.mqtt_param[pref + 'TemperatureSensor1'] = '300'
            self.mqtt_param[pref + 'TemperatureSensor2'] = '300'
        elif (self.device_temperatur_configured == 2):
            self.mqtt_param[pref + 'TemperatureSensor0'] = self.temp0
            self.mqtt_param[pref + 'TemperatureSensor1'] = self.temp1
            self.mqtt_param[pref + 'TemperatureSensor2'] = '300'
        else:
            self.mqtt_param[pref + 'TemperatureSensor0'] = self.temp0
            self.mqtt_param[pref + 'TemperatureSensor1'] = self.temp1
            self.mqtt_param[pref + 'TemperatureSensor2'] = self.temp2
        self.mqtt_param[pref + 'Watt'] = str(self._oldwatt)
        self.mqtt_param[pref + 'Wh'] = str(self._wh)
        self.mqtt_param[pref + 'WHImported_temp'] = str(self._wpos)
        self.mqtt_param[pref + 'oncountnor'] = self.oncountnor
        self.mqtt_param[pref + 'OnCntStandby'] = self.oncntstandby
        # nur bei Status 10 on status mitnehmen
        if (self.devstatus == 10):
            sendstatus = self.relais + self.devstatus
        else:
            sendstatus = self.devstatus
        self.mqtt_param[pref + 'Status'] = str(sendstatus)
        if (self.gruppe == 'A'):
            Sbase.ausschaltwatt = Sbase.ausschaltwatt + self._oldwatt
        elif (self.gruppe == 'E'):
            if (self.relais == 1):
                Sbase.einrelais = 1
            Sbase.eindevstatus = max(Sbase.eindevstatus, self.devstatus)

    def updatepar(self, input_param: Dict[str, str]) -> None:
        self._smart_param = input_param.copy()
        self.device_nummer = int(self._smart_param.get('device_nummer', '0'))
        for key, value in self._smart_param.items():
            try:
                valueint = int(value)
            except Exception:
                valueint = 0
            if (key in ['device_nummer']):
                pass
            elif (key == 'device_canSwitch'):
                self.device_canswitch = valueint
            elif (key == 'device_deactivateWhileEvCharging'):
                self._device_deactivatewhileevcharging = valueint
            elif (key == 'device_mineinschaltdauer'):
                self._device_mineinschaltdauer = valueint * 60
            elif (key == 'device_mindayeinschaltdauer'):
                self._device_mindayeinschaltdauer = valueint * 60
            elif (key == 'device_maxeinschaltdauer'):
                self._device_maxeinschaltdauer = valueint * 60
            elif (key == 'device_homeConsumtion'):
                self.device_homeconsumtion = valueint
            elif (key == 'device_setauto'):
                self.device_setauto = valueint
            elif (key == 'device_differentMeasurement'):
                self._device_differentmeasurement = valueint
            elif (key == 'device_temperatur_configured'):
                self.device_temperatur_configured = valueint
            elif (key == 'device_speichersocbeforestop'):
                self._device_speichersocbeforestop = valueint
            elif (key == 'device_speichersocbeforestart'):
                self._device_speichersocbeforestart = valueint
            elif (key == 'device_startupDetection'):
                self._device_startupdetection = valueint
            elif (key == 'device_standbyPower'):
                self._device_standbypower = valueint
            elif (key == 'device_standbyDuration'):
                self._device_standbyduration = valueint
            elif (key == 'device_standbypower'):
                self._device_standbypower = valueint
            elif (key == 'device_standbyduration'):
                self._device_standbyduration = valueint
            elif (key == 'device_startupMulDetection'):
                self._device_startupmuldetection = valueint
            elif (key == 'device_einschaltschwelle'):
                self._device_einschaltschwelle = valueint
            elif (key == 'device_ausschaltschwelle'):
                self._device_ausschaltschwelle = valueint * -1
            elif (key == 'device_einschaltverzoegerung'):
                self._device_einschaltverzoegerung = valueint * 60
            elif (key == 'device_ausschaltverzoegerung'):
                self._device_ausschaltverzoegerung = valueint * 60
            elif (key == 'device_nonewatt'):
                self._device_nonewatt = valueint
            elif (key == 'device_type'):
                self.device_type = value
            elif (key == 'device_lambdaueb'):
                self.device_lambdaueb = value
            elif (key == 'device_configured'):
                self._device_configured = value
            elif (key == 'device_name'):
                self.device_name = value
            elif (key == 'device_ip'):
                self._device_ip = value
            elif (key == 'device_measureType'):
                self._device_measuretype = value
            elif (key == 'device_measureip'):
                self._device_measureip = value
            elif (key == 'device_measurePortSdm'):
                self._device_measureportsdm = valueint
            elif (key == 'device_dacport'):
                self._device_dacport = valueint
            elif (key == 'device_measureid'):
                self._device_measureid = valueint
            elif (key == 'device_finishTime'):
                self._device_finishtime = value
            elif (key == 'device_startTime'):
                self._device_starttime = value
            elif (key == 'device_endTime'):
                self._device_endtime = value
            elif (key == 'device_onTime'):
                self._device_ontime = value
            elif (key == 'device_offTime'):
                self._device_offtime = value
            elif (key == 'device_onuntilTime'):
                self._device_onuntiltime = value
            elif (key == 'mode'):
                self.device_manual = valueint
            elif (key == 'device_updatesec'):
                self._device_updatesec = valueint
            elif (key == 'device_chan'):
                self._device_chan = valueint
            elif (key == 'device_manual_control'):
                self.device_manual_control = valueint
            elif (key == 'device_deactivateper'):
                self._device_deactivateper = valueint
            elif (key == 'device_pbtype'):
                self._device_pbtype = value


# openWB/config/set/SmartHome/Devices/<ID>/mode auf 1 setzen -> Gerät wird
# als 'Manuell' in der Geräteliste geführt
# openWB/config/set/SmartHome/Devices/<ID>/device_manual_control -> 0
# signalisiert dass das Gerät ausgeschaltet ist, 1 signalisiert Betrieb
            elif (key == 'WHImported_temp'):
                if (self._first_run == 1):
                    self._whimported_tmp = valueint
                    log.info("(" + str(self.device_nummer) +
                             ") aus mqtt übernommen " + key +
                             " " + value)
            elif (key == 'RunningTimeToday'):
                if (self._first_run == 1):
                    self.runningtime = valueint
                    log.info("(" + str(self.device_nummer) +
                             ") aus mqtt übernommen " + key +
                             " " + value)
            elif (key == 'oncountnor'):
                if (self._first_run == 1):
                    self.oncountnor = value
                    log.info("(" + str(self.device_nummer) +
                             ") aus mqtt übernommen " + key +
                             " " + value)
            elif (key == 'OnCntStandby'):
                if (self._first_run == 1):
                    self.oncntstandby = value
                    # status normal setzen
                    self.devstatus = 10
                    log.info("(" + str(self.device_nummer) +
                             ") aus mqtt übernommen " + key +
                             " " + value)
            else:
                log.info("(" + str(self.device_nummer) + ") "
                         + "Sbase überlesen " + key +
                         " " + value)
        self._first_run = 0
        #  pref = 'openWB/SmartHome/Devices/' + str(self.device_nummer) + '/'
        pref = '/' + str(self.device_nummer) + '/'
        self.mqtt_param_del[pref + 'RelayStatus'] = '0'
        self.mqtt_param_del[pref + 'Watt'] = '0'
        self.mqtt_param_del[pref + 'oncountnor'] = '0'
        self.mqtt_param_del[pref + 'OnCntStandby'] = '0'
        self.mqtt_param_del[pref + 'Status'] = '0'
        self.mqtt_param_del[pref + 'TemperatureSensor0'] = '300'
        self.mqtt_param_del[pref + 'TemperatureSensor1'] = '300'
        self.mqtt_param_del[pref + 'TemperatureSensor2'] = '300'
        self.mqtt_param_del[pref + 'RunningTimeToday'] = '0'
        if (self._device_deactivateper == 100):
            self.gruppe = 'E'
            Sbase.eindevices = Sbase.eindevices + 1
            workein = self._device_einschaltschwelle
            Sbase.einschwelle = Sbase.einschwelle + workein
            workeinverz = self._device_einschaltverzoegerung + 30
            Sbase.einverz = max(Sbase.einverz, workeinverz)
        elif (self._device_deactivateper > 0):
            self.gruppe = 'A'
            Sbase.ausdevices = Sbase.ausdevices + 1
        else:
            self.gruppe = 'none'
        if (self.device_type == 'none'):
            self.device_canswitch = 0
        if (self._device_pbtype == 'shellypb'):
            if (self._old_pbtype == 'none'):
                self._mydevicepb = Sbshelly()
                self._old_pbtype = 'shelly'
                log.info("(" + str(self.device_nummer) +
                         ") control Button. Neues Button" +
                         " device erzeugt Shelly")
            else:
                log.info("(" + str(self.device_nummer) +
                         ") Control Button. Nur Parameter " +
                         " update ")
            self._mydevicepb.updatepar(input_param)
        if ((self._device_pbtype == 'none') and
           (self._old_pbtype == 'shelly')):
            del self._mydevicepb
            self._old_pbtype = 'none'
            log.info("(" + str(self.device_nummer) +
                     ") Control Button gelöscht")
        if (self._device_differentmeasurement == 1):
            if (self._oldmeasuretype1 == self._device_measuretype):
                log.info("(" + str(self.device_nummer) +
                         ") Separate Messung. Nur Parameter" +
                         " update " + self._device_measuretype)
                self._mydevicemeasure.updatepar(self._smart_param)
            else:
                if (self._oldmeasuretype1 == 'empty'):
                    pass
                else:
                    log.info("(" + str(self.device_nummer) +
                             ") Separate Messung. Altes Measure"
                             + "device gelöscht " + self._oldmeasuretype1)
                    del self._mydevicemeasure
                if (self._device_measuretype == 'sdm630'):
                    self._mydevicemeasure = Slsdm630()
                elif (self._device_measuretype == 'lovato'):
                    self._mydevicemeasure = Sllovato()
                elif (self._device_measuretype == 'b23'):
                    self._mydevicemeasure = Slb23()
                elif (self._device_measuretype == 'sdm120'):
                    self._mydevicemeasure = Slsdm120()
                elif (self._device_measuretype == 'we514'):
                    self._mydevicemeasure = Slwe514()
                elif (self._device_measuretype == 'fronius'):
                    self._mydevicemeasure = Slfronius()
                elif (self._device_measuretype == 'json'):
                    self._mydevicemeasure = Sljson()
                elif (self._device_measuretype == 'smaem'):
                    self._mydevicemeasure = Slsmaem()
                elif (self._device_measuretype == 'shelly'):
                    self._mydevicemeasure = Slshelly()
                elif (self._device_measuretype == 'tasmota'):
                    self._mydevicemeasure = Sltasmota()
                elif (self._device_measuretype == 'mqtt'):
                    self._mydevicemeasure = Slmqtt()
                elif (self._device_measuretype == 'http'):
                    self._mydevicemeasure = Slhttp()
                elif (self._device_measuretype == 'avm'):
                    self._mydevicemeasure = Slavm()
                elif (self._device_measuretype == 'mystrom'):
                    self._mydevicemeasure = Slmystrom()
                else:
                    log.info("(" + str(self.device_nummer) +
                             ") Measuretype nicht untertützt " +
                             self._device_measuretype)
                self._mydevicemeasure.updatepar(self._smart_param)
                self._oldmeasuretype1 = self._device_measuretype
                log.info("(" + str(self.device_nummer) +
                         ") Separate Messung. Neues Measure" +
                         "device erzeugt " + self._device_measuretype)
        if ((self._device_differentmeasurement == 0) and
           (self._oldmeasuretype1 != 'empty')):
            log.info("(" + str(self.device_nummer) +
                     ") Separate Messung ausgeschaltet."
                     " Altes Measure" +
                     "device gelöscht " + self._oldmeasuretype1)
            del self._mydevicemeasure
            self._oldmeasuretype1 = 'empty'
        with open(self._basePath+'/ramdisk/smarthome_device_minhaus_' +
                  str(self.device_nummer), 'w') as f:
            f.write(str(self.device_homeconsumtion))

    def getueb(self) -> None:
        #    (1 = mit Speicher, 2 = mit offset , 0 = manual eingeschaltet)
        if (self.ueberschussberechnung == 2):
            self.devuberschuss = self._uberschussoffset
        else:
            self.devuberschuss = self._uberschuss

    def preturn(self, zustand: int, ueberschussberechnung: int, updatecnt: int) -> None:
        self.ueberschussberechnung = ueberschussberechnung
        with open(self._basePath+'/ramdisk/device' + str(self.device_nummer) +
                  '_req_relais', 'w') as f:
            f.write(str(zustand))
        if (zustand == 1):
            if updatecnt == 1:
                self.oncountnor = str(int(self.oncountnor) + 1)
            else:
                self.oncntstandby = str(int(self.oncntstandby) + 1)
            log.info("(" + str(self.device_nummer) +
                     ") angeschaltet. Überschussberechnung (1 = mit " +
                     " Speicher, 2 = mit Offset) " +
                     str(self.ueberschussberechnung))
            if updatecnt == 1:
                self._c_eintime_f = 'Y'
                self._c_eintime = int(time.time())

    def sepwatt(self, newwatt: int, newwattk: int) -> Tuple[int, int]:
        if (self._device_differentmeasurement == 0):
            return newwatt, newwattk
        # ueberschuss übertragen
        self._mydevicemeasure.devuberschuss = self.devuberschuss
        self._mydevicemeasure.sepwattread()
        self.newwatt = self._mydevicemeasure.newwatt
        self.newwattk = self._mydevicemeasure.newwattk
        return self.newwatt, self.newwattk

    def conditions(self, speichersoc: int) -> None:
        # do not do anything in case none type or can switch = no
        # or device manuam mode
        if ((self.device_canswitch == 0) or
           (self.device_manual == 1)):
            return
        work_ausschaltschwelle = self._device_ausschaltschwelle
        work_ausschaltverzoegerung = self._device_ausschaltverzoegerung
        local_time = datetime.now(timezone.utc).astimezone()
        localhour = int(local_time.strftime("%H"))
        localminute = int(local_time.strftime("%M"))
        localinsec = int((localhour * 60 * 60) + (localminute * 60))
        if (localinsec < Sbase.nureinschaltinsec) and (Sbase.eindevices > 0):
            log.info("(" + str(self.device_nummer) + ") " +
                     self.device_name + " Prüfe nur Einschaltgruppe ")
            if (self.gruppe == 'E'):
                pass
            else:
                log.info("(" + str(self.device_nummer) + ") " +
                         self.device_name + " kein Regelung")
                return
        # onnow = 0 -> normale Regelung
        # onnow = 1 -> Zeitpunkt erreciht, immer ein ohne Ueberschuss regelung
        onnow = 0
        # offnow = 0 -> normale Regelung
        # offnow = 1 -> Zeitpunkt erreicht, immer aus ohne Ueberschuss regelung
        offnow = 0
        if (self._device_ontime != '00:00'):
            onhour = int(str("0") + str(self._device_ontime).partition(':')[0])
            onminute = int(str(self._device_ontime)[-2:])
            log.info("(" + str(self.device_nummer) + ") " +
                     self.device_name + " Immer an nach definiert " +
                     str(onhour) + ":" + str('%.2d' % onminute) +
                     " aktuelle Zeit " + str(localhour) + ":" +
                     str('%.2d' % localminute))
            if ((onhour > localhour) or ((onhour == localhour)
               and (onminute >= localminute))):
                pass
            else:
                log.info("(" + str(self.device_nummer) + ") " +
                         self.device_name +
                         " schalte ein wegen Immer an nach")
                onnow = 1

        if (self._device_offtime != '00:00'):
            offh = int(str("0") + str(self._device_offtime).partition(':')[0])
            offminute = int(str(self._device_offtime)[-2:])
            log.info("(" + str(self.device_nummer) + ") " +
                     self.device_name + " Immer aus nach definiert " +
                     str(offh) + ":" + str('%.2d' % offminute) +
                     " aktuelle Zeit " + str(localhour) + ":" +
                     str('%.2d' % localminute))
            if ((offh > localhour) or ((offh == localhour)
               and (offminute >= localminute))):
                pass
            else:
                log.info("(" + str(self.device_nummer) + ") " +
                         self.device_name +
                         " schalte aus wegen Immer aus nach")
                offnow = 1

        if (self._device_onuntiltime != '00:00'):
            onuntilh = int(str("0")
                           + str(self._device_onuntiltime).partition(':')[0])
            onuntilminute = int(str(self._device_onuntiltime)[-2:])
            log.info("(" + str(self.device_nummer) + ") " +
                     self.device_name + " Immer an vor definiert " +
                     str(onuntilh) + ":" + str('%.2d' % onuntilminute)
                     + " aktuelle Zeit " + str(localhour) + ":" +
                     str('%.2d' % localminute))
            if ((onuntilh < localhour) or ((onuntilh == localhour)
               and (onuntilminute <= localminute))):
                pass
            else:
                log.info("(" + str(self.device_nummer) + ") " +
                         self.device_name +
                         " schalte ein wegen Immer an vor")
                onnow = 1
        minrunningtime = max(self._device_mineinschaltdauer, self._device_mindayeinschaltdauer)
        if ((self._device_finishtime != '00:00')
           and (self.runningtime < minrunningtime) and self.devstatus != 30):
            finishhour = int(str("0") +
                             str(self._device_finishtime).partition(':')[0])
            finishminute = int(str(self._device_finishtime)[-2:])
            startspatsec = int((finishhour * 60 * 60) + (finishminute * 60) -
                               max((minrunningtime - self.runningtime), 0))
            log.info("(" + str(self.device_nummer) + ") " +
                     self.device_name +
                     " finishtime definiert " +
                     str(finishhour) + ":" + str('%.2d' % finishminute)
                     + " aktuelle Zeit " + str(localhour) + ":" +
                     str('%.2d' % localminute) +
                     " max(Mineinschaltdauer (Sec), Mineinschaltdauer pro Tag (Sec)) "
                     + str(minrunningtime))
            if (((finishhour > localhour) or ((finishhour == localhour)
               and (finishminute >= localminute)))
                    and (startspatsec < localinsec)):
                log.info("(" + str(self.device_nummer) + ") " +
                         self.device_name +
                         " schalte ein wegen finishtime" +
                         " spätester Start in sec " + str(startspatsec) +
                         " aktuelle sec " + str(localinsec))
                self.turndevicerelais(1, 0, 1)
                self.devstatus = 30
                return
        if self.devstatus == 30:
            log.info("(" + str(self.device_nummer) + ") " +
                     self.device_name +
                     " finishtime laueft, pruefe max(Mineinschaltdauer (Sec), Mineinschaltdauer pro Tag (Sec)) ")
            if (self._c_eintime_f == 'Y'):
                if (minrunningtime < self.runningtime):
                    log.info("(" + str(self.device_nummer) + ") " +
                             self.device_name +
                             " Zeit erreicht," +
                             " finishtime erreicht")
                    self.devstatus = 10
                    return
                else:
                    log.info("(" + str(self.device_nummer) + ") " +
                             self.device_name +
                             " finishtime laueft, max(Mineinschaltdauer (Sec), Mineinschaltdauer pro Tag (Sec)) " +
                             "nicht erreicht, " +
                             str(minrunningtime) +
                             " > " + str(self.runningtime))
                    return
            else:
                log.info("(" + str(self.device_nummer) + ") " +
                         self.device_name +
                         " Mindesteinschaltdauer nicht bekannt," +
                         " finishtime erreicht")
                self.devstatus = 10
                return
        # here startup device_self._device_startupdetection
        if (((self._device_startupdetection == 0) or (onnow == 1))
           and (self.devstatus == 20)):
            self.devstatus = 10
            self.turndevicerelais(0, 0, 1)
            log.info("(" + str(self.device_nummer) + ") " +
                     self.device_name +
                     " Anlauferkennung nun abgeschaltet ")
            return
        # remove condition that device has to be off
        if ((self._device_startupdetection == 1)
           and (self.oncntstandby == str("0"))
           and (self.oncountnor == str("0"))
           and (self.devstatus != 20)):
            self.devstatus = 20
            log.info("(" + str(self.device_nummer) + ") " +
                     self.device_name +
                     " Anlauferkennung nun aktiv, eingeschaltet ")
            self.turndevicerelais(1, 0, 0)
            return
        if (self.devstatus == 20):
            if (self.newwatt) > self._device_standbypower:
                if (self._c_anlaufz_f == 'Y'):
                    timesince = int(time.time()) - int((self._c_anlaufz))
                    if (self._device_standbyduration < timesince):
                        log.info("(" + str(self.device_nummer) + ") " +
                                 self.device_name +
                                 " standbycheck abgelaufen " +
                                 str(self._device_standbyduration) +
                                 " ,sec pruefe Einschaltschwelle " +
                                 str(self._device_standbypower))
                        self.devstatus = 10
                        self._c_anlaufz_f = 'N'
                        if ((self.devuberschuss >
                           self._device_einschaltschwelle) or (onnow == 1)):
                            self._c_ausverz_f = 'N'
                            self._c_einverz_f = 'N'
                            log.info("(" + str(self.device_nummer) +
                                     ") " + self.device_name +
                                     " Überschuss " +
                                     str(self.devuberschuss) +
                                     " größer Einschaltschwelle oder" +
                                     " Immer an zeit erreicht, schalte " +
                                     "ein (ohne Einschaltverzoegerung) " +
                                     str(self._device_einschaltschwelle))
                            self.turndevicerelais(1,
                                                  self.ueberschussberechnung,
                                                  1)
                        else:
                            log.info("(" + str(self.device_nummer) +
                                     ") " + self.device_name +
                                     " Überschuss " +
                                     str(self.devuberschuss) +
                                     " kleiner Einschaltschwelle," +
                                     " schalte aus " +
                                     str(self._device_einschaltschwelle))
                            self.turndevicerelais(0, 0, 1)
                        return
                    else:
                        log.info("(" + str(self.device_nummer) + ") " +
                                 self.device_name +
                                 " standbycheck noch nicht erreicht " +
                                 str(self._device_standbyduration) + " > "
                                 + str(timesince))
                else:
                    self._c_anlaufz_f = 'Y'
                    self._c_anlaufz = int(time.time())
                    log.info("(" + str(self.device_nummer) + ") " +
                             self.device_name + " standbycheck gestartet "
                             + str(self.newwatt) + " > " +
                             str(self._device_standbypower))
            else:
                self._c_anlaufz_f = 'N'
                log.info("(" + str(self.device_nummer) + ") " +
                         self.device_name +
                         " unter standbyschwelle , timer geloescht")
        if (self._device_maxeinschaltdauer > self.runningtime):
            log.info("(" + str(self.device_nummer) + ") " +
                     self.device_name +
                     " Maximale Einschaltdauer nicht erreicht")
        else:
            if (self.relais == 1):
                log.info("(" + str(self.device_nummer) + ") " +
                         self.device_name +
                         " Maximale Einschaltdauer erreicht schalte ab")
                self.turndevicerelais(0, 0, 1)
            else:
                log.info("(" + str(self.device_nummer) + ")" +
                         self.device_name +
                         " Maximale Einschaltdauer erreicht" +
                         " bereits abgeschaltet")
            return
        # Auto ladung
        if self._device_deactivatewhileevcharging > 0:
            if (self.relais == 1):
                log.info("(" + str(self.device_nummer) + ") " +
                         self.device_name +
                         " Soll reduziert/abgeschaltet werden" +
                         " bei Ladung, pruefe " + str(self.chargestatus))
                if self.chargestatus:
                    log.info("(" + str(self.device_nummer) + ") " +
                             self.device_name +
                             " Ladung läuft, pruefe Mindestlaufzeit")
                    if (self._c_eintime_f == 'Y'):
                        timesta = int(time.time()) - int(self._c_eintime)
                        if (self._device_mineinschaltdauer < timesta):
                            if self._device_deactivatewhileevcharging == 2:
                                log.info("(" + str(self.device_nummer)
                                         + ") " + self.device_name +
                                         " Mindesteinschaltdauer" +
                                         "  erreicht, schalte aus")
                                self.turndevicerelais(0, 0, 1)
                                return
                            else:
                                if (self._dynregel == 0):
                                    log.info("(" +
                                             str(self.device_nummer) +
                                             ") " + self.device_name +
                                             " Mindesteinschaltdauer " +
                                             "erreicht, " +
                                             "Ausschaltschwelle 0 " +
                                             "gesetzt")
                                    work_ausschaltverzoegerung = 0
                                    if (work_ausschaltschwelle < 0):
                                        work_ausschaltschwelle = 0
                                else:
                                    log.info("(" +
                                             str(self.device_nummer)
                                             + ") " + self.device_name +
                                             " Gerät mit dyn Regelung")
                        else:
                            log.info("(" + str(self.device_nummer) +
                                     ") " + self.device_name +
                                     " Mindesteinschaltdauer nicht" +
                                     " erreicht, " +
                                     str(self._device_mineinschaltdauer) +
                                     " > " + str(timesta))
                    else:
                        if self._device_deactivatewhileevcharging == 2:
                            log.info("(" + str(self.device_nummer) +
                                     ") " + self.device_name +
                                     " Mindesteinschaltdauer nicht" +
                                     " bekannt,schalte aus")
                            self.turndevicerelais(0, 0, 1)
                            return
                        else:
                            if (self._dynregel == 0):
                                log.info("(" +
                                         str(self.device_nummer) +
                                         ") " + self.device_name +
                                         " Mindesteinschaltdauer " +
                                         "nicht bekannt, " +
                                         "Ausschaltschwelle 0 " +
                                         "gesetzt")
                                work_ausschaltverzoegerung = 0
                                if (work_ausschaltschwelle < 0):
                                    work_ausschaltschwelle = 0
                            else:
                                log.info("(" +
                                         str(self.device_nummer)
                                         + ") " + self.device_name +
                                         " Gerät mit dyn Regelung")
                else:
                    log.info("(" + str(self.device_nummer) + ") " +
                             self.device_name +
                             " Ladung läuft nicht, pruefe weiter")
            else:
                if self._device_deactivatewhileevcharging == 2:
                    log.info("(" + str(self.device_nummer) + ") " +
                             self.device_name +
                             " Soll nicht eingeschaltet werden bei" +
                             " Ladung, pruefe " + str(self.chargestatus))
                    if self.chargestatus:
                        log.info("(" + str(self.device_nummer) + ") "
                                 + self.device_name + " Ladung läuft, " +
                                 "wird nicht eingeschaltet")
                        return
        # Auto ladung ende
        # Art vom ueberschussberechnung pruefen
        if (self._device_speichersocbeforestart == 0):
            # Berechnung aus, Ueberschuss mit Speicher nehmen
            self.devuberschuss = self._uberschuss
            newueberschussberechnung = 1
        else:
            if ((speichersoc < self._device_speichersocbeforestart) and
               (speichersoc < 97)):
                # unter dem Speicher soc, nur EVU Ueberschuss
                # Berechnung mit Ueberschuss nur mit Speicherentladung
                self.devuberschuss = self._uberschussoffset
                newueberschussberechnung = 2
            else:
                # sonst drueber oder gleich Speicher soc Berechnung
                # mit Ueberschuss mit Speicher nehmen
                # oder nehmen wenn speicher fast voll
                self.devuberschuss = self._uberschuss
                newueberschussberechnung = 1
        if (self.ueberschussberechnung != newueberschussberechnung):
            self.ueberschussberechnung = newueberschussberechnung
            log.info("(" + str(self.device_nummer) + ") " +
                     self.device_name + " SoC " + str(speichersoc) +
                     " Einschalt SoC " +
                     str(self._device_speichersocbeforestart) +
                     " Ueberschuss " + str(self.devuberschuss))
            log.info("(" + str(self.device_nummer) + ") " +
                     self.device_name +
                     " Ueberschussberechnung anders (1 = mit Speicher," +
                     " 2 = mit Offset) " +
                     str(self.ueberschussberechnung))
        if (self.devstatus == 20):
            log.info("(" + str(self.device_nummer) + ") " +
                     self.device_name +
                     " Anlauferkennung immer noch aktiv, keine Ueberprüf"
                     + "ung auf Einschalt oder Ausschaltschwelle ")
            return
        # Device mit Anlauferkennung (mehrfach pro tag)
        # welches im PV Modus ist ?
        if ((self.devstatus == 10) and (self._device_startupmuldetection == 1)
           and (self._device_startupdetection == 1)
           and (int(self.oncountnor) > 0)):
            if (self._c_eintime_f == 'Y'):
                timesta = int(time.time()) - int(self._c_eintime)
                if (self._device_mineinschaltdauer < timesta):
                    log.info("(" + str(self.device_nummer) + ") "
                             + self.device_name +
                             " Mindesteinschaltdauer erreicht," +
                             " restarte Anlauferkennung ")
                    self._c_eintime_f = 'N'
                    self.devstatus = 20
                    self.oncntstandby = str("0")
                    self.oncountnor = str("0")
                    log.info("(" + str(self.device_nummer) + ") " +
                             self.device_name +
                             " Anlauferkennung nun aktiv, eingeschaltet ")
                    self.turndevicerelais(1, 0, 0)
                    return
            else:
                log.info("(" + str(self.device_nummer) + ") " +
                         self.device_name +
                         " Mindesteinschaltdauer nicht bekannt" +
                         " restarte Anlauferkennung ")
                self.devstatus = 20
                self.oncntstandby = str("0")
                self.oncountnor = str("0")
                log.info("(" + str(self.device_nummer) + ") " +
                         self.device_name +
                         " Anlauferkennung nun aktiv, eingeschaltet ")
                self.turndevicerelais(1, 0, 0)
                return
        # periodisch hart ausschalten
        if ((self.relais == 1) and (self.gruppe == 'A') and
           (Sbase.eindevices == 0)):
            log.info("(" + str(self.device_nummer) + ") " +
                     self.device_name +
                     " Soll periodisch ausgeschaltet werden " +
                     " (1 = volle Stunde / " +
                     " 2 = volle Stunde + halbe Stunde) pruefe " +
                     str(self._device_deactivateper))
            if (((self._device_deactivateper == 2) and (localminute == 30)) or
               (localminute == 00)):
                log.info("(" + str(self.device_nummer) +
                         ") " + self.device_name +
                         " erfolgreich, schalte aus ")
                self.turndevicerelais(0, 0, 1)
                self._c_ausverz_f = 'N'
                return
        # periodisch prüfen ob ausschalten
        if ((self.relais == 1) and (self.gruppe == 'A') and
           (Sbase.eindevices > 0)):
            log.info("(" + str(self.device_nummer) + ") " +
                     self.device_name +
                     " Soll periodisch geprüft werden " +
                     " (1 = volle Stunde / " +
                     " 2 = volle Stunde + halbe Stunde) " +
                     str(self._device_deactivateper))
            if (((self._device_deactivateper == 2) and (localminute == 30)) or
               (localminute == 00)):
                log.info("(" + str(self.device_nummer) +
                         ") " + self.device_name +
                         " akt Leistungsaufnahme Abschaltgruppe " +
                         str(Sbase.ausschaltwatt) +
                         " Summe benötigte Einschaltschwelle: " +
                         str(Sbase.einschwelle) + " Überschuss " +
                         str(self._uberschuss))
                if (((Sbase.ausschaltwatt + self._uberschuss) >
                   Sbase.einschwelle) and Sbase.einrelais == 0 and
                   Sbase.eindevstatus == 10):
                    log.info("(" + str(self.device_nummer) +
                             ") " + self.device_name +
                             " erfolgreich, schalte aus ")
                    self.turndevicerelais(0, 0, 1)
                    self._c_ausverz_f = 'N'
                    # rechne Zeit exclusive einschaltgruppe
                    local_time = datetime.now(timezone.utc).astimezone()
                    localh = int(local_time.strftime("%H"))
                    localminute = int(local_time.strftime("%M"))
                    localinsec = int((localh * 60 * 60) + (localminute * 60))
                    Sbase.nureinschaltinsec = localinsec + Sbase.einverz
                    return
        if (((self.devuberschuss > self._device_einschaltschwelle)
           or (onnow == 1)) and (offnow == 0)):
            self._c_ausverz_f = 'N'
            log.info("(" + str(self.device_nummer) + ") " +
                     str(self.device_name) + " Überschuss " +
                     str(self.devuberschuss) + " größer Einschaltschwelle"
                     + " oder Immer an zeit erreicht " +
                     str(self._device_einschaltschwelle))
            if (self.relais == 0):
                log.info("(" + str(self.device_nummer) + ") " +
                         self.device_name + " SoC " + str(speichersoc) +
                         " Einschalt SoC " +
                         str(self._device_speichersocbeforestart) +
                         " Ueberschuss " + str(self.devuberschuss))
                log.info("(" + str(self.device_nummer) + ") " +
                         self.device_name + " Ueberschussberechnung (1 ="
                         + " mit Speicher, 2 = mit Offset) " +
                         str(self.ueberschussberechnung))
                if (self._device_starttime != '00:00'):
                    starthour = int(str("0") +
                                    str(self._device_starttime).
                                    partition(':')[0])
                    startminute = int(str(self._device_starttime)[-2:])
                    log.info("(" + str(self.device_nummer) + ") " +
                             self.device_name +
                             " Fruehster Start um definiert " +
                             str(starthour) + ":" +
                             str('%.2d' % startminute) +
                             " aktuelle Zeit " + str(localhour) + ":" +
                             str('%.2d' % localminute))
                    if ((starthour > localhour) or ((starthour == localhour)
                       and (startminute >= localminute))):
                        log.info("(" + str(self.device_nummer) + ") " +
                                 self.device_name +
                                 " Fruehster Start noch nicht erreicht ")
                        return
                if (self._device_endtime != '00:00'):
                    endhour = int(str("0") +
                                  str(self._device_endtime).partition(':')[0])
                    endminute = int(str(self._device_endtime)[-2:])
                    log.info("(" + str(self.device_nummer) + ") " +
                             self.device_name +
                             " Spaetester Start um definiert " +
                             str(endhour) + ":" + str('%.2d' % endminute)
                             + " aktuelle Zeit " + str(localhour) + ":"
                             + str('%.2d' % localminute))
                    if ((endhour > localhour) or ((endhour == localhour)
                       and (endminute >= localminute))):
                        pass
                    else:
                        log.info("(" + str(self.device_nummer) + ") " +
                                 self.device_name +
                                 " Spaetester Start vorbei ")
                        return
                if (self._c_einverz_f == 'Y'):
                    timesince = int(time.time()) - int(self._c_einverz)
                    if (self._device_einschaltverzoegerung < timesince):
                        log.info("(" + str(self.device_nummer) + ") "
                                 + self.device_name +
                                 " Einschaltverzögerung erreicht, " +
                                 "schalte ein " +
                                 str(self._device_einschaltschwelle))
                        self.turndevicerelais(1, self.ueberschussberechnung, 1)
                        self._c_einverz_f = 'N'
                    else:
                        log.info("(" + str(self.device_nummer) + ") " +
                                 self.device_name +
                                 " Einschaltverzögerung nicht erreicht. "
                                 + str(self._device_einschaltverzoegerung)
                                 + " > " + str(timesince))
                else:
                    self._c_einverz_f = 'Y'
                    self._c_einverz = int(time.time())
                    log.info("(" + str(self.device_nummer) + ") " +
                             self.device_name +
                             " Einschaltverzögerung gestartet")
            else:
                log.info("(" + str(self.device_nummer) + ") " +
                         self.device_name +
                         " Einschaltverzögerung erreicht, bereits ein")
                self._c_einverz_f = 'N'
        else:
            self._c_einverz_f = 'N'
            if (self.devuberschuss < work_ausschaltschwelle) or (offnow == 1):
                if (speichersoc > self._device_speichersocbeforestop):
                    log.info("(" + str(self.device_nummer) + ") " +
                             self.device_name +
                             " SoC höher als Abschalt SoC," +
                             " lasse Gerät weiterlaufen")
                    return
                else:
                    log.info("(" + str(self.device_nummer) + ") " +
                             self.device_name +
                             " SoC niedriger als Abschalt SoC," +
                             " prüfe weiter")
                log.info("(" + str(self.device_nummer) + ") " +
                         self.device_name + " Überschuss " +
                         str(self.devuberschuss) +
                         " kleiner Ausschaltschwelle  " +
                         str(work_ausschaltschwelle) +
                         " oder immer aus erreicht ")
                if (self.relais == 1):
                    if (self._c_ausverz_f == 'Y'):
                        timesince = int(time.time()) - int(self._c_ausverz)
                        if (work_ausschaltverzoegerung < timesince):
                            if (self._c_eintime_f == 'Y'):
                                timesta = int((time.time()) -
                                              int(self._c_eintime))
                                if (self._device_mineinschaltdauer < timesta):
                                    log.info("(" +
                                             str(self.device_nummer) +
                                             ") " + self.device_name +
                                             " Ausschaltverzögerung &" +
                                             " Mindesteinschaltdauer " +
                                             "erreicht, schalte aus " +
                                             str(work_ausschaltschwelle))
                                    self.turndevicerelais(0, 0, 1)
                                    self._c_ausverz_f = 'N'
                                else:
                                    s1 = str(self._device_mineinschaltdauer)
                                    log.info("(" +
                                             str(self.device_nummer) +
                                             ") " + self.device_name +
                                             " Ausschaltverzögerung errei"
                                             + "cht, Mindesteinschalt" +
                                             "dauer nicht erreicht, " +
                                             s1 + " > " + str(timesta))
                            else:
                                log.info("(" + str(self.device_nummer)
                                         + ") " + self.device_name +
                                         " Mindesteinschaltdauer nicht" +
                                         " bekannt, schalte aus")
                                self.turndevicerelais(0, 0, 1)
                        else:
                            log.info("(" + str(self.device_nummer) +
                                     ") " + self.device_name +
                                     " Ausschaltverzögerung nicht" +
                                     " erreicht. " +
                                     str(work_ausschaltverzoegerung) +
                                     " > " + str(timesince))
                    else:
                        log.info("(" + str(self.device_nummer) + ") " +
                                 self.device_name +
                                 " Ausschaltverzögerung gestartet ")
                        self._c_ausverz_f = 'Y'
                        self._c_ausverz = int(time.time())

                else:
                    log.info("(" + str(self.device_nummer) + ") " +
                             self.device_name +
                             " Ausschaltverzögerung erreicht,bereits aus")
                    self._c_ausverz_f = 'N'
            else:
                log.info("(" + str(self.device_nummer) + ") " +
                         self.device_name + " Überschuss kleiner als" +
                         " Einschaltschwelle und größer als " +
                         "Ausschaltschwelle. Ueberschuss " +
                         str(self.devuberschuss))
                self._c_einverz_f = 'N'
                self._c_ausverz_f = 'N'

    def simcount(self, watt2: int, pref: str, importfn: str, exportfn: str, nummer: str, wattks: int) -> int:
        # if (nummer == "1"):
        #    debug = True
        # else:
        #   debug = False
        seconds2 = time.time()
        watt1 = 0
        seconds1 = 0.0
        # Zaehler mitgeliefert in WH , zurueckrechnen fuer simcount
        if wattks > 0:
            wattposkh = wattks
            wattnegkh = 0
            wattposh = wattks * 3600
            wattnegh = 0
            with open(self._basePath+'/ramdisk/'+pref+'watt0pos', 'w') as f:
                f.write(str(wattposh))
            self._wpos = wattposh
            with open(self._basePath+'/ramdisk/'+pref+'watt0neg', 'w') as f:
                f.write(str(wattnegh))
            with open(self._basePath+'/ramdisk/' + importfn, 'w') as f:
                f.write(str(round(wattposkh, 2)))
            with open(self._basePath+'/ramdisk/' + exportfn, 'w') as f:
                f.write(str(wattnegkh))
            # start punkt für simulation schreiben
            value1 = "%22.6f" % seconds2
            with open(self._basePath+'/ramdisk/'+pref+'sec0', 'w') as f:
                f.write(str(value1))
            with open(self._basePath+'/ramdisk/'+pref+'wh0', 'w') as f:
                f.write(str(watt2))
            self._wh = round(wattposkh, 2)
            return self._wh
        # emulate import  export
        if os.path.isfile(self._basePath+'/ramdisk/'+pref+'sec0'):
            with open(self._basePath+'/ramdisk/'+pref+'sec0', 'r') as f:
                seconds1 = float(f.read())
            with open(self._basePath+'/ramdisk/'+pref+'wh0', 'r') as f:
                watt1 = int(f.read())
            with open(self._basePath+'/ramdisk/'+pref+'watt0pos', 'r') as f:
                wattposh = int(f.read())
            with open(self._basePath+'/ramdisk/'+pref+'watt0neg', 'r') as f:
                wattnegh = int(f.read())
            with open(self._basePath+'/ramdisk/'+pref+'wh0', 'w') as f:
                f.write(str(watt2))
            seconds1 = seconds1 + 1
            deltasec = seconds2 - seconds1
            stepsize = int((watt2-watt1)/(deltasec + 1))
            # if debug:
            #    log.info("(" + str(nummer) +
            #             ")D star wh " + str(wattposh) +
            #              " kwh " + str(int(wattposh/3600)) +
            #              " seconds1 " + str(seconds1) +
            #              " watt1 " + str(watt1) +
            #              " seconds2 " + str(seconds2) +
            #              " deltasec " + str(deltasec) +
            #              " stepsize " + str(stepsize) +
            #              " watt2 " + str(watt2))
            while seconds1 < seconds2:
                if watt1 < 0:
                    wattnegh = wattnegh + watt1
                else:
                    wattposh = wattposh + watt1
                # if debug:
                #     log.info("(" + str(nummer) +
                #              ")D calc wh " + str(wattposh) +
                #              " kwh " + str(int(wattposh/3600)) +
                #              " seconds1 " + str(seconds1) +
                #              " watt1 " + str(watt1))
                watt1 = watt1 + stepsize
                if stepsize <= 0:
                    watt1 = max(watt1, watt2)
                else:
                    watt1 = min(watt1, watt2)
                seconds1 = seconds1 + 1
            seconds1 = seconds1 - 1
            value1 = "%22.6f" % seconds1
            with open(self._basePath+'/ramdisk/'+pref+'sec0', 'w') as f:
                f.write(str(value1))
            wattnegkh = int((wattnegh*-1)/3600)
            with open(self._basePath+'/ramdisk/'+pref+'watt0pos', 'w') as f:
                f.write(str(wattposh))
            self._wpos = wattposh
            with open(self._basePath+'/ramdisk/'+pref+'watt0neg', 'w') as f:
                f.write(str(wattnegh))
            wattposkh = int(wattposh/3600)
            with open(self._basePath+'/ramdisk/' + importfn, 'w') as f:
                f.write(str(round(wattposkh, 2)))
            with open(self._basePath+'/ramdisk/' + exportfn, 'w') as f:
                f.write(str(wattnegkh))
        else:
            value1 = "%22.6f" % seconds2
            with open(self._basePath+'/ramdisk/'+pref+'sec0', 'w') as f:
                f.write(str(value1))
            with open(self._basePath+'/ramdisk/'+pref+'wh0', 'w') as f:
                f.write(str(watt2))
            with open(self._basePath+'/ramdisk/'+pref+'watt0pos', 'r') as f:
                wattposh = int(f.read())
            wattposkh = int(wattposh/3600)
        self._wh = round(wattposkh, 2)
        return self._wh

    def getwatt(self, uberschuss: int, uberschussoffset: int) -> None:
        self.prewatt(uberschuss, uberschussoffset)
        self.newwatt = 0
        self.newwattk = 0
        self.relais = 0
        self.postwatt()

    def turndevicerelais(self, zustand: int, ueberschussberechnung: int, updatecnt: int) -> None:
        pass

    def updatebutton(self) -> None:
        self.newdevice_manual = self.device_manual
        self.newdevice_manual_control = self.device_manual_control
        self.btchange = 0
        if (self._old_pbtype == 'none'):
            return
        self._mydevicepb.showstat(self.device_manual, self.relais)
        (newmanual, newmanual_control) = self._mydevicepb.checkbut(
            self.device_manual, self.relais,
            self.device_manual_control)
        if ((self.newdevice_manual == newmanual) and
           self.newdevice_manual_control == newmanual_control):
            #   keine Änderung
            return
        self.newdevice_manual = newmanual
        self.newdevice_manual_control = newmanual_control
        log.info("(" + str(self.device_nummer) + ") " +
                 self.device_name +
                 " Umschaltung manual modus alt/neu " +
                 str(self.device_manual) + "/" +
                 str(self.newdevice_manual) +
                 " on off alt/neu " + str(self.device_manual_control) +
                 "/" + str(self.newdevice_manual_control))
        if (self.newdevice_manual == self.device_manual):
            #  Änderung bezüglich on off
            self.btchange = 2
        else:
            #  Änderung bezüglich mode
            self.btchange = 1
