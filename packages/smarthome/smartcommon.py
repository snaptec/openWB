#!/usr/bin/python3
from modules.smarthome.ratiotherm.smartratiotherm import Sratiotherm
from modules.smarthome.viessmann.smartviessmann import Sviessmann
from modules.smarthome.tasmota.smarttasmota import Stasmota
from modules.smarthome.lambda_.smartlambda import Slambda
from modules.smarthome.vampair.smartvampair import Svampair
from modules.smarthome.stiebel.smartstiebel import Sstiebel
from modules.smarthome.shelly.smartshelly import Sshelly
from modules.smarthome.mystrom.smartmystrom import Smystrom
from modules.smarthome.mqtt.smartmqtt import Smqtt
from modules.smarthome.http.smarthttp import Shttp
from modules.smarthome.idm.smartidm import Sidm
from modules.smarthome.elwa.smartelwa import Selwa
from modules.smarthome.askoheat.smartaskoheat import Saskoheat
from modules.smarthome.nxdacxx.smartnxdacxx import Snxdacxx
from modules.smarthome.acthor.smartacthor import Sacthor
from modules.smarthome.avmhomeautomation.smartavm import Savm
from smarthome.smartbase import Sbase
from typing import Dict, List, Any, Tuple
import paho.mqtt.client as mqtt
import re
import time
import os
import math
import logging
log = logging.getLogger(__name__)
mydevices = []  # type: List[Any]
mqtt_cache = {}  # type: Dict[str, str]
parammqtt = []  # type: List[Any]
# will be populated with open 1.9 / openwb 2.0 specifc param
mqttcg = 'none'
mqttcs = 'none'
mqttsdevstat = 'none'
mqttsglobstat = 'none'
mqtttopicdisengageable = 'none'
ramdiskwrite = True
mqttport = 0
bp = '/var/www/html/openWB'
numberOfSupportedDevices = 9  # limit number of smarthome devices
resetmaxeinschaltdauer = 0
maxspeicher = 0
firststart = True


def on_connect(client, userdata, flags, rc) -> None:
    global mqttcg
    global mqttsdevstat
    #  mqttcg = 'openWB/config/get/SmartHome/'
    #  client.subscribe("openWB/config/get/SmartHome/#", 2)
    client.subscribe(mqttcg + '#', 2)
    #  mqttsdevstat = 'openWB/SmartHome/Devices'
    #  client.subscribe("openWB/SmartHome/Devices/#", 2)
    client.subscribe(mqttsdevstat + '/#', 2)


def logmq(topic: str, devicenumb: int, keyword: str, value: str) -> None:
    global parammqtt
    global ramdiskwrite
    #  richtig  topic single
    if (devicenumb < 1) or (devicenumb > numberOfSupportedDevices):
        pass
    else:
        log.info("(" + str(devicenumb) + ") Key " + str(keyword) + " Value " + str(value))
        parammqtt.append([devicenumb, keyword, value])
        if ramdiskwrite:
            with open(bp+'/ramdisk/smartparam.sh', 'a') as f:
                print('%s' % ('mosquitto_pub -p 1886 -t ' +
                              '"' + topic + '/' + str(devicenumb) + '/' + keyword +
                              '" -r -m "' + str(value) + '"'), file=f)


def logmqgl(keyword: str, value: str) -> None:
    #  richtig  topic global
    log.info("( global ) Key " + str(keyword) + " Value " + str(value))
    if ramdiskwrite:
        with open(bp+'/ramdisk/smartparam.sh', 'a') as f:
            print('%s' % ('mosquitto_pub -p 1886 -t ' +
                          '"openWB/LegacySmartHome/config/get/' + keyword +
                          '" -r -m "' + str(value) + '"'), file=f)


def on_message(client, userdata, msg) -> None:
    # wenn exception hier wird mit nächster msg weitergemacht
    # macht paho unter phyton 3 immer so
    # für neuer python 3.7 version gibt es absturz
    global maxspeicher
    try:
        devicenumb = int(re.sub(r'\D', '', msg.topic))
    except Exception:
        devicenumb = 0
    value = msg.payload.decode("utf-8")
    try:
        valueint = int(value)
    except Exception:
        valueint = 0
    # mqttcg = 'openWB/config/get/SmartHome/'
    if (mqttcg + 'Devices' in msg.topic):
        keyword = re.sub(mqttcg + 'Devices/' + str(devicenumb) + '/', '', msg.topic)
        logmq("openWB/LegacySmartHome/config/get/Devices", devicenumb, keyword, value)
    # mqttsdevstat = 'openWB/SmartHome/Devices'
    elif (mqttsdevstat in msg.topic):
        keyword = re.sub(mqttsdevstat + "/" + str(devicenumb) + '/', '', msg.topic)
        logmq("openWB/LegacySmartHome/Devices", devicenumb, keyword, value)
    # mqttcg = 'openWB/config/get/SmartHome/'
    elif (mqttcg + "maxBatteryPower" in msg.topic):
        keyword = re.sub(mqttcg, '', msg.topic)
        logmqgl(keyword, value)
        maxspeicher = int(valueint)
    else:
        log.warning(" Skipped msg " + msg.topic + " Value " + value)


def getdevicevalues(uberschuss: int, uberschussoffset: int, pvwatt: int, chargestatus: bool) -> None:
    global mydevices
    totalwatt = 0
    totalwattot = 0
    totalminhaus = 0
    # dyn daten einschaltgruppe
    Sbase.ausschaltwatt = 0
    Sbase.einrelais = 0
    Sbase.eindevstatus = 0
    mqtt_all = {}
    for mydevice in mydevices:
        mydevice.pvwatt = pvwatt
        mydevice.chargestatus = chargestatus
        mydevice.getwatt(uberschuss, uberschussoffset)
        watt = mydevice.newwatt
        wattk = mydevice.newwattk
        wattks = mydevice.newwattks
        relais = mydevice.relais
        # temp0 = mydevice.temp0
        # temp1 = mydevice.temp1
        # temp2 = mydevice.temp2
        if ((mydevice.abschalt == 1) and (relais == 1)
           and (mydevice.device_manual != 1)):
            totalwatt = totalwatt + watt
        else:
            totalwattot = totalwattot + watt
        if (mydevice.device_homeconsumtion == 0):
            totalminhaus = totalminhaus + watt
        log.info("(" + str(mydevice.device_nummer) + ") " +
                 str(mydevice.device_name) + " rel: " + str(relais) +
                 " oncnt/onstandby/time: " + str(mydevice.oncountnor) + "/"
                 + str(mydevice.oncntstandby) + "/" +
                 str(mydevice.runningtime) + " Status/Üeb: " +
                 str(mydevice.devstatus) + "/" +
                 str(mydevice.ueberschussberechnung) + " akt: " + str(watt) +
                 " Z1: " + str(wattk) + " Z2: " + str(wattks))
        #  mqtt_all.update(mydevice.mqtt_param)
        for keyread, value in mydevice.mqtt_param.items():
            key = mqttsdevstat + keyread
            mqtt_all[key] = value
    # device_total_watt is needed for calculation the proper überschuss
    # (including switchable smarthomedevices)
    if ramdiskwrite:
        with open(bp+'/ramdisk/devicetotal_watt', 'w') as f:
            f.write(str(totalwatt))
        with open(bp+'/ramdisk/devicetotal_watt_other', 'w') as f:
            f.write(str(totalwattot))
        with open(bp+'/ramdisk/devicetotal_watt_hausmin', 'w') as f:
            f.write(str(totalminhaus))
    log.info("Total Watt abschaltbarer smarthomedevices: " +
             str(totalwatt))
    log.info("Total Watt nichtabschaltbarer smarthomedevices: "
             + str(totalwattot))
    log.info("Total Watt nicht im Hausverbrauch: " +
             str(totalminhaus))
    log.info("Anzahl devices in Auschaltgruppe: " +
             str(Sbase.ausdevices) + " akt: " + str(Sbase.ausschaltwatt) +
             " Anzahl devices in Einschaltgruppe: " + str(Sbase.eindevices)
             )
    nurhh = math.floor(Sbase.nureinschaltinsec / 3600)
    nurmm = math.floor((Sbase.nureinschaltinsec - (nurhh * 3600)) / 60)
    nurss = (Sbase.nureinschaltinsec - (nurhh * 3600) - (nurmm * 60))
    log.info("Einschaltgruppe rel: " + str(Sbase.einrelais) +
             " Summe Einschaltschwelle: " +
             str(Sbase.einschwelle) + " max Einschaltverzögerung " +
             str(Sbase.einverz) + " nur Einschaltgruppe prüfen bis: " +
             str('%.2d' % nurhh) + ":" + str('%.2d' % nurmm) + ":" +
             str('%.2d' % nurss) +
             " in Total sec " + str(Sbase.nureinschaltinsec)
             )
    # mqttsglobstat = 'openWB/SmartHome/Status/'
    mqtt_all[mqttsglobstat + 'maxspeicherladung'] = maxspeicher
    # mqtttopicdisengageable = 'openWB/SmartHome/Status/wattschalt'
    mqtt_all[mqtttopicdisengageable] = totalwatt
    mqtt_all[mqttsglobstat + 'wattnichtschalt'] = totalwattot
    mqtt_all[mqttsglobstat + 'wattnichtHaus'] = totalminhaus
    mqtt_all[mqttsglobstat + 'uberschuss'] = uberschuss
    mqtt_all[mqttsglobstat + 'uberschussoffset'] = uberschussoffset
    sendmq(mqtt_all)


def sendmq(mqtt_input: Dict[str, str]) -> None:
    global mqtt_cache
    client = mqtt.Client("openWB-SmartHome-bulkpublisher-" + str(os.getpid()))
    client.connect("localhost", mqttport)
    for key, value in mqtt_input.items():
        valueold = mqtt_cache.get(key, 'not in cache')
        if (valueold == value):
            pass
        else:
            log.info("Mq pub " + str(key) + "=" +
                     str(value) + " old " + str(valueold))
            if (mqttcs in str(key)):
                log.info("Mq no caching " + str(key))
            else:
                mqtt_cache[key] = value
            client.publish(key, payload=value, qos=0, retain=True)
            client.loop(timeout=2.0)
    client.disconnect()


def conditions(speichersoc: int) -> None:
    global mydevices
    for mydevice in mydevices:
        mydevice.conditions(speichersoc)


def update_devices() -> None:
    global parammqtt
    global mydevices
    global mqtt_cache
    client = mqtt.Client("openWB-SmartHome-bulkpublisher-" + str(os.getpid()))
    client.connect("localhost", mqttport)
    # statische daten einschaltgruppe
    Sbase.ausdevices = 0
    Sbase.eindevices = 0
    Sbase.einverz = 0
    Sbase.einschwelle = 0
    # Nur einschaltgruppe in Sekunden
    Sbase.nureinschaltinsec = 0
    for i in range(1, numberOfSupportedDevices+1):
        device_configured = 0
        device_type = 'none'
        input_param = {}
        input_param['device_nummer'] = str(i)
        for devicenumb, keyword, value in parammqtt:
            if (str(i) == str(devicenumb)):
                if (keyword == 'device_configured'):
                    device_configured = value
                if (keyword == 'device_type'):
                    device_type = value
                input_param[keyword] = value
        if (device_configured == "1"):
            createnew = 1
            for mydevice in mydevices:
                if (str(i) == str(mydevice.device_nummer)):
                    log.info("(" + str(i) + ") " +
                             "Device bereits erzeugt")
                    if (device_type == mydevice.device_type):
                        log.info("(" + str(i) + ") " +
                                 "Typ gleich, nur Parameter update")
                        createnew = 0
                        mydevice.updatepar(input_param)
                    else:
                        log.info("(" + str(i) + ") " +
                                 "Typ ungleich " + mydevice.device_type)
                        mydevice.device_nummer = 0
                        mydevice._device_configured = '9'
                        # del mydevice
                        mydevices.remove(mydevice)
                        log.info("(" + str(i) + ") " +
                                 "Device gelöscht")
                    break
            if (createnew == 1):
                log.info("(" + str(i) +
                         ") Neues Devices oder Typänderung: " +
                         str(device_type))
                if (device_type == 'shelly'):
                    mydevice = Sshelly()
                elif (device_type == 'stiebel'):
                    mydevice = Sstiebel()
                elif (device_type == 'vampair'):
                    mydevice = Svampair()
                elif (device_type == 'lambda'):
                    mydevice = Slambda()
                elif (device_type == 'ratiotherm'):
                    mydevice = Sratiotherm()
                elif (device_type == 'tasmota'):
                    mydevice = Stasmota()
                elif (device_type == 'avm'):
                    mydevice = Savm()
                elif (device_type == 'viessmann'):
                    mydevice = Sviessmann()
                elif (device_type == 'acthor'):
                    mydevice = Sacthor()
                elif (device_type == 'NXDACXX'):
                    mydevice = Snxdacxx()
                elif (device_type == 'elwa'):
                    mydevice = Selwa()
                elif (device_type == 'askoheat'):
                    mydevice = Saskoheat()
                elif (device_type == 'idm'):
                    mydevice = Sidm()
                elif (device_type == 'mqtt'):
                    mydevice = Smqtt()
                elif (device_type == 'http'):
                    mydevice = Shttp()
                elif (device_type == 'mystrom'):
                    mydevice = Smystrom()
                else:
                    mydevice = Sbase()
                mydevice.updatepar(input_param)
                mydevices.append(mydevice)
        else:
            log.info("(" + str(i) + ") " +
                     "Device nicht (länger) definiert")
            for mydevice in mydevices:
                if (str(i) == str(mydevice.device_nummer)):
                    # cleant up mqtt
                    for keyread, value in mydevice.mqtt_param_del.items():
                        key = mqttsdevstat + keyread
                        valueold = mqtt_cache.pop(key, 'not in cache')
                        log.info("Mq pub " + str(key) + "=" +
                                 str(value) + " old " + str(valueold))
                        client.publish(key, payload=value, qos=0, retain=True)
                        client.loop(timeout=2.0)
                    mydevice.device_nummer = 0
                    mydevice._device_configured = '9'
                    # del mydevice
                    mydevices.remove(mydevice)
                    log.info("(" + str(i) + ") " +
                             "Device gelöscht")
    client.disconnect()


def readmq() -> None:
    global parammqtt
    global mydevices
    log.info("Config reRead start / Parameter check")
    if ramdiskwrite:
        with open(bp+'/ramdisk/smartparam.sh', 'w') as f:
            print('%s' % ('#!/bin/bash'), file=f)
    parammqtt = []
    client = mqtt.Client("openWB-mqttsmarthome")
    client.on_connect = on_connect
    client.on_message = on_message
    startTime = time.time()
    waitTime = 5
    client.connect("localhost", mqttport)
    while True:
        client.loop()
        elapsedTime = time.time() - startTime
        if elapsedTime > waitTime:
            client.disconnect()
            break
    log.info("Config reRead / Parameter check done")
    update_devices()
    log.info("Config reRead done")
    if ramdiskwrite:
        with open(bp+'/ramdisk/smartparam.sh', 'a') as f:
            print('%s' % ('echo 1 > /var/www/html/openWB/ramdisk/rereadsmarthomedevices'), file=f)


def resetmaxeinschaltdauerfunc() -> None:
    global resetmaxeinschaltdauer
    global mydevices
    mqtt_reset = {}
    hour = time.strftime("%H")
    if (int(hour) == 0):
        if (int(resetmaxeinschaltdauer) == 0):
            for i in range(1, (numberOfSupportedDevices+1)):
                for mydevice in mydevices:
                    if (str(i) == str(mydevice.device_nummer)):
                        # mqttsdevstat = 'openWB/SmartHome/Devices'
                        pref = mqttsdevstat + '/' + str(i) + '/'
                        mydevice.runningtime = 0
                        mqtt_reset[pref + 'RunningTimeToday'] = '0'
                        log.info("(" + str(i) +
                                 ") RunningTime auf 0 gesetzt")
                        mydevice.oncountnor = '0'
                        mqtt_reset[pref + 'oncountnor'] = '0'
                # Sofern Anlauferkennung laueft counter nicht zuruecksetzen
                        if (mydevice.devstatus != 20):
                            mydevice.oncntstandby = '0'
                            mqtt_reset[pref + 'OnCntStandby'] = '0'
                        mydevice.c_oldstampeinschaltdauer = 0
                        mydevice.c_oldstampeinschaltdauer_f = 'N'
                        # mqttcs = 'openWB/config/set/SmartHome/'
                        pref = mqttcs + 'Devices/' + str(i) + '/'
                        if ((mydevice.device_setauto == 1) and
                           (mydevice.device_manual == 1)):
                            log.info("(" + str(i) +
                                     ") Umschaltung auf automatisch Modus ")
                            mqtt_reset[pref + 'mode'] = '0'
            resetmaxeinschaltdauer = 1
            # Nur einschaltgruppe in Sekunden für neuen Tag zurücksetzten
            Sbase.nureinschaltinsec = 0
            sendmq(mqtt_reset)
    if (int(hour) == 1):
        resetmaxeinschaltdauer = 0


def loadregelvars(wattbezug: int, speicherleistung: int, speichersoc: int,
                  pvwatt: int,  chargestatus: bool) -> Tuple[int, int]:
    global maxspeicher
    global mydevices
    uberschuss = wattbezug + speicherleistung
    uberschussoffset = wattbezug + speicherleistung - maxspeicher
    log.info("EVU Bezug(-)/Einspeisung(+): " + str(wattbezug) +
             " max Speicherladung: " + str(maxspeicher))
    log.info("Uberschuss: " + str(uberschuss) +
             " Uberschuss mit Offset: " + str(uberschussoffset) + " Pv: " + str(pvwatt))
    log.info("Speicher Entladung(-)/Ladung(+): " +
             str(speicherleistung) + " SpeicherSoC: " + str(speichersoc) + " Ladung: " + str(chargestatus))
    reread = 0
    try:
        with open(bp+'/ramdisk/rereadsmarthomedevices', 'r') as value:
            reread = int(value.read())
    except Exception:
        reread = 1
    if (reread == 1):
        with open(bp+'/ramdisk/rereadsmarthomedevices', 'w') as f:
            f.write(str(0))
        readmq()
    for i in range(1, (numberOfSupportedDevices+1)):
        try:
            with open(bp+'/ramdisk/smarthome_device_manual_'
                      + str(i), 'r') as value:
                for mydevice in mydevices:
                    if (str(i) == str(mydevice.device_nummer)):
                        mydevice.device_manual = int(value.read())
        except Exception:
            pass
        try:
            with open(bp+'/ramdisk/smarthome_device_manual_control_'
                      + str(i), 'r') as value:
                for mydevice in mydevices:
                    if (str(i) == str(mydevice.device_nummer)):
                        mydevice.device_manual_control = int(value.read())
        except Exception:
            pass
    return uberschuss, uberschussoffset


def initparam(inpcg: str, inpcs: str, inpsdevstat: str, inpsglobstat: str, inptopicdisengageable: str,
              inpramdiskwrite: bool, inpport: int) -> None:
    global mqttcg
    global mqttcs
    global mqttsdevstat
    global mqttsglobstat
    global mqtttopicdisengageable
    global ramdiskwrite
    global mqttport
    mqttcg = inpcg
    mqttcs = inpcs
    mqttsdevstat = inpsdevstat
    mqttsglobstat = inpsglobstat
    mqtttopicdisengageable = inptopicdisengageable
    ramdiskwrite = inpramdiskwrite
    mqttport = inpport


def mainloop(wattbezug: int, speicherleistung: int, speichersoc: int, pvwatt: int = 0,
             chargestatus: bool = False) -> None:
    global firststart
    if firststart:
        readmq()
        firststart = False
    mqtt_man = {}
    sendmess = 0
    uberschuss, uberschussoffset = loadregelvars(wattbezug, speicherleistung, speichersoc, pvwatt, chargestatus)
    resetmaxeinschaltdauerfunc()
    getdevicevalues(uberschuss, uberschussoffset, pvwatt, chargestatus)
    conditions(speichersoc)
    # do the manual stuff
    for i in range(1, (numberOfSupportedDevices+1)):
        for mydevice in mydevices:
            if (str(i) == str(mydevice.device_nummer)):
                if (mydevice.device_manual == 1):
                    if (mydevice.device_manual_control == 0):
                        if (mydevice.relais == 1):
                            mydevice.turndevicerelais(0, 0, 1)
                    if (mydevice.device_manual_control == 1):
                        if (mydevice.relais == 0):
                            mydevice.turndevicerelais(1, 0, 1)
                    mydevice.c_mantime_f = 'Y'
                    mydevice.c_mantime = time.time()
                    log.info("(" + str(i) + ") " +
                             mydevice.device_name + " manueller Modus aktiviert, keine Regelung")
    for i in range(1, (numberOfSupportedDevices+1)):
        # mqttcs = 'openWB/config/set/SmartHome/'
        pref = mqttcs + 'Devices/' + str(i) + '/'
        for mydevice in mydevices:
            if (str(i) == str(mydevice.device_nummer)):
                mydevice.updatebutton()
                if (mydevice.btchange == 1):
                    sendmess = 1
                    mqtt_man[pref + 'mode'] = mydevice.newdevice_manual
                if (mydevice.btchange == 2):
                    sendmess = 1
                    workman = mydevice.newdevice_manual_control
                    mqtt_man[pref + 'device_manual_control'] = workman
    if (sendmess == 1):
        sendmq(mqtt_man)
