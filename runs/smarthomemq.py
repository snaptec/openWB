#!/usr/bin/python3
import paho.mqtt.client as mqtt
import time
import re
import os
import logging
import math
from usmarthome.global0 import log, log_config
from usmarthome.smartbase import Sbase
from usmarthome.smartavm import Savm
from usmarthome.smartacthor import Sacthor
from usmarthome.smartnxdacxx import Snxdacxx
from usmarthome.smartelwa import Selwa
from usmarthome.smartidm import Sidm
from usmarthome.smarthttp import Shttp
from usmarthome.smartmqtt import Smqtt
from usmarthome.smartmystrom import Smystrom
from usmarthome.smartshelly import Sshelly
from usmarthome.smartstiebel import Sstiebel
from usmarthome.smartvampair import Svampair
from usmarthome.smartlambda import Slambda
from usmarthome.smarttasmota import Stasmota
from usmarthome.smartviessmann import Sviessmann

mqtt_cache = {}
mydevices = []
bp = '/var/www/html/openWB'
numberOfSupportedDevices = 9  # limit number of smarthome devices


def initlog():
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    log_config.setLevel(logging.DEBUG)
    fh = logging.FileHandler(bp+'/ramdisk/smartcon.log', encoding='utf8')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    log_config.addHandler(fh)
    log.setLevel(logging.DEBUG)
    fh = logging.FileHandler(bp+'/ramdisk/smarthome.log', encoding='utf8')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    log.addHandler(fh)


def on_connect(client, userdata, flags, rc):
    client.subscribe("openWB/config/get/SmartHome/Devices/#", 2)
    client.subscribe("openWB/SmartHome/Devices/#", 2)


def on_message(client, userdata, msg):
    # wenn exception hier wird mit nächster msg weitergemacht
    # macht paho unter phyton 3 immer so
    global parammqtt
    devicenumb = re.sub(r'\D', '', msg.topic)
    input = msg.payload.decode("utf-8")
    if ("openWB/config/get/SmartHome/Devices" in msg.topic):
        keyword = re.sub('openWB/config/get/SmartHome/Devices/'
                         + str(devicenumb) + '/', '', msg.topic)
    if ("openWB/SmartHome/Devices" in msg.topic):
        keyword = re.sub('openWB/SmartHome/Devices/'
                         + str(devicenumb) + '/', '', msg.topic)
    value = str(input)
    if (("/" in keyword) or (int(devicenumb) < 1) or
       (int(devicenumb) > numberOfSupportedDevices)):
        # falsches topic
        log_config.warning("(" + str(devicenumb) + ") skipped Key " +
                           str(keyword) + " Msg " + str(msg.topic) +
                           " Value " + str(value))
    else:
        # richtig  topic
        log_config.info("(" + str(devicenumb) + ") Key " +
                        str(keyword) + " Value " + str(value))
        parammqtt.append([devicenumb, keyword, value])


def checkbootdone():
    global resetmaxeinschaltdauer
    resetmaxeinschaltdauer = 0
    try:
        with open(bp+'/ramdisk/bootinprogress', 'r') as value:
            bootinprogress = int(value.read())
    except Exception as e:
        bootinprogress = 1
        log.warning("Ramdisk not set up. Maybe we are still" +
                    "booting (bootinprogress)." + str(e))
        time.sleep(30)
        return 0
    try:
        with open(bp+'/ramdisk/updateinprogress', 'r') as value:
            updateinprogress = int(value.read())
    except Exception as e:
        updateinprogress = 1
        log.warning("Ramdisk not set up. Maybe we are still" +
                    " booting (updateinprogress)." + str(e))
        time.sleep(30)
        return 0
    if (updateinprogress == 1):
        log.warning("Update in progress.")
        time.sleep(30)
        return 0
    if (bootinprogress == 1):
        log.warning("Boot in progress.")
        time.sleep(30)
        return 0
    return 1
# Lese aus der Ramdisk Regelrelevante Werte ein


def loadregelvars():
    global uberschuss
    global uberschussoffset
    global speicherleistung
    global speichersoc
    global speichervorhanden
    global wattbezug
    global numberOfSupportedDevices
    global maxspeicher
    global mydevices
    try:
        with open(bp+'/ramdisk/speichervorhanden', 'r') as value:
            speichervorhanden = int(value.read())
        if (speichervorhanden == 1):
            with open(bp+'/ramdisk/speicherleistung', 'r') as value:
                speicherleistung = int(float(value.read()))
            with open(bp+'/ramdisk/speichersoc', 'r') as value:
                speichersoc = int(float(value.read()))
        else:
            speicherleistung = 0
            speichersoc = 100
    except Exception as e:
        log.warning("Fehler beim Auslesen der Ramdisk " +
                    "(speichervorhanden,speicherleistung,speichersoc): " +
                    str(e))
        speichervorhanden = 0
        speicherleistung = 0
        speichersoc = 100
    try:
        with open(bp+'/ramdisk/wattbezug', 'r') as value:
            wattbezug = int(float(value.read())) * -1
    except Exception as e:
        log.warning("Fehler beim Auslesen der Ramdisk (wattbezug):"
                    + str(e))
        wattbezug = 0
    uberschuss = wattbezug + speicherleistung
    try:
        with open(bp+'/ramdisk/smarthomehandlermaxbatterypower', 'r') as value:
            maxspeicher = int(value.read())
    except Exception as e:
        log.warning("Fehler beim Auslesen der Ramdisk " +
                    "(smarthomehandlermaxbatterypower): " + str(e))
        maxspeicher = 0
    uberschussoffset = wattbezug + speicherleistung - maxspeicher
    log.info("EVU Bezug(-)/Einspeisung(+): " + str(wattbezug) +
             " max Speicherladung: " + str(maxspeicher))
    log.info("Uberschuss: " + str(uberschuss) +
             " Uberschuss mit Offset: " + str(uberschussoffset))
    log.info("Speicher Entladung(-)/Ladung(+): " +
             str(speicherleistung) + " SpeicherSoC: " + str(speichersoc))
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


def getdevicevalues():
    global mydevices
    global uberschuss
    global uberschussoffset
    totalwatt = 0
    totalwattot = 0
    totalminhaus = 0
    # dyn daten einschaltgruppe
    Sbase.ausschaltwatt = 0
    Sbase.einrelais = 0
    Sbase.eindevstatus = 0
    mqtt_all = {}
    for mydevice in mydevices:
        mydevice.getwatt(uberschuss, uberschussoffset)
        watt = mydevice.newwatt
        wattk = mydevice.newwattk
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
                 " Z: " + str(wattk))
        mqtt_all.update(mydevice.mqtt_param)
    # device_total_watt is needed for calculation the proper überschuss
    # (including switchable smarthomedevices)

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
    mqtt_all['openWB/SmartHome/Status/maxspeicherladung'] = maxspeicher
    mqtt_all['openWB/SmartHome/Status/wattschalt'] = totalwatt
    mqtt_all['openWB/SmartHome/Status/wattnichtschalt'] = totalwattot
    mqtt_all['openWB/SmartHome/Status/wattnichtHaus'] = totalminhaus
    mqtt_all['openWB/SmartHome/Status/uberschuss'] = uberschuss
    mqtt_all['openWB/SmartHome/Status/uberschussoffset'] = uberschussoffset
    sendmq(mqtt_all)


def sendmq(mqtt_input):
    global mqtt_cache
    client = mqtt.Client("openWB-SmartHome-bulkpublisher-" + str(os.getpid()))
    client.connect("localhost")
    for key, value in mqtt_input.items():
        valueold = mqtt_cache.get(key, 'not in cache')
        if (valueold == value):
            pass
        else:
            log.info("Mq pub " + str(key) + "=" +
                     str(value) + " old " + str(valueold))
            mqtt_cache[key] = value
            client.publish(key, payload=value, qos=0, retain=True)
            client.loop(timeout=2.0)
    client.disconnect()


def conditions():
    global mydevices
    global speichersoc
    for mydevice in mydevices:
        mydevice.conditions(speichersoc)


def update_devices():
    global parammqtt
    global mydevices
    global mqtt_cache
    client = mqtt.Client("openWB-SmartHome-bulkpublisher-" + str(os.getpid()))
    client.connect("localhost")
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
                    for key, value in mydevice.mqtt_param_del.items():
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


def readmq():
    global parammqtt
    global mydevices
    log_config.info("Config reRead start")
    log.info("Config reRead start")
    parammqtt = []
    client = mqtt.Client("openWB-mqttsmarthome")
    client.on_connect = on_connect
    client.on_message = on_message
    startTime = time.time()
    waitTime = 5
    client.connect("localhost")
    while True:
        client.loop()
        elapsedTime = time.time() - startTime
        if elapsedTime > waitTime:
            client.disconnect()
            break
    update_devices()
    log_config.info("Config reRead done")
    log.info("Config reRead done")


def resetmaxeinschaltdauerfunc():
    global resetmaxeinschaltdauer
    global numberOfSupportedDevices
    global mydevices
    mqtt_reset = {}
    hour = time.strftime("%H")
    if (int(hour) == 0):
        if (int(resetmaxeinschaltdauer) == 0):
            for i in range(1, (numberOfSupportedDevices+1)):
                for mydevice in mydevices:
                    if (str(i) == str(mydevice.device_nummer)):
                        pref = 'openWB/SmartHome/Devices/' + str(i) + '/'
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


if __name__ == "__main__":
    initlog()
    log.info("*** Smarthome mq Start ***")
    log_config.info("*** Smarthome mq Start ***")
    while True:
        if (checkbootdone() == 1):
            break
        time.sleep(5)
    readmq()
    time.sleep(5)
    while True:
        #        update_devices()
        mqtt_man = {}
        sendmess = 0
        loadregelvars()
        resetmaxeinschaltdauerfunc()
        getdevicevalues()
        conditions()
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
                                 mydevice.device_name +
                                 " manueller Modus aktiviert, keine Regelung")
        for i in range(1, (numberOfSupportedDevices+1)):
            pref = 'openWB/config/set/SmartHome/Devices/' + str(i) + '/'
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
        time.sleep(5)
