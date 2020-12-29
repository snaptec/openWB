#!/usr/bin/python
# coding: utf8

#########################################################
#
# liest von Tibber die stündlichen Preise für heute und morgen,
# erstellt daraus die Datei für den Graphen und liefert den aktuell
# gültigen Strompreis
#
# setzt aktuellen Strompreis auf 99.99ct/kWh, wenn nichts empfangen wird
#
# benötigt als Parameter den persönlichen Tibber-Token und die homeID
# des Anschlusses
#
# TODO: schreibt derzeit (testweise) noch auf awattar-ramdisk, Implementierung per 
# korrekter MQTT-Topics folgt
#
# 2020 Michael Ortenstein
# This file is part of openWB
#
#########################################################

import requests
import json
import time
import os
import sys

# übergebene Token auslesen
tibberToken = str(sys.argv[1])
homeID = str(sys.argv[2])

# Variablen initialisieren
readPriceSuccessfull = False
headers = {'Authorization': 'Bearer ' + tibberToken, 'Content-Type': 'application/json'}
data = '{ "query": "{viewer {home(id:\\"' + homeID + '\\") {currentSubscription {priceInfo {today {total startsAt} tomorrow {total startsAt}}}}}}" }'

# Hilfsfunktionen
def writeLogEntry(message):
    # schreibt Eintrag ins Log
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    with open('/var/www/html/openWB/ramdisk/openWB.log', 'a') as f:
        f.write(timestamp + ' Modul tibbergetprices.py: ' + message + '\n')

# Hauptprogramm
# Tibber-API abfragen
response = requests.post('https://api.tibber.com/v1-beta/gql', headers=headers, data=data)

if response:
    # Tibber Antwort ist angekommen
    if not 'errors' in response.text:
        # keine Fehler, parse json
        prices = json.loads(response.text)
        # extrahiere Preise für heute, sortiert nach Zeitstempel
        todayPrices = sorted(prices['data']['viewer']['home']['currentSubscription']['priceInfo']['today'], key=lambda k: (k['startsAt'], k['total']))
        # extrahiere Preise für morgen, sortiert nach Zeitstempel
        tomorrowPrices = sorted(prices['data']['viewer']['home']['currentSubscription']['priceInfo']['tomorrow'], key=lambda k: (k['startsAt'], k['total']))

        if len(todayPrices) == 24:
            # alle 24 Stundenpreise für heute erhalten, schreibe in Ramdisk, Preise konvertiert in Eurocent
            with open('/var/www/html/openWB/ramdisk/awattarprice', 'w') as awattarpricefile, \
                 open('/var/www/html/openWB/ramdisk/awattargraphlist', 'w') as awattargraphlistfile:
                # aktuelle Stunde als int
                currentHour = int(time.strftime('%H', time.localtime(time.time())))
                for tibberHour, price in enumerate(todayPrices):
                    # Preisliste mit den heutigen Preisen füllen
                    if tibberHour >= currentHour:
                        awattargraphlistfile.write('%i,%2.2f\n' % (tibberHour, (price['total']) * 100))
                        if tibberHour == currentHour:
                            awattarpricefile.write('%2.2f\n' % (price['total'] * 100))
                            readPriceSuccessfull = True
                # jetzt die Preise für morgen
                if len(tomorrowPrices) == 24:
                    # alle 24 Stundenpreise für morgen erhalten, schreibe in Ramdisk, Preise konvertiert in Eurocent
                    for tibberHour, price in enumerate(tomorrowPrices):
                        awattargraphlistfile.write('%i,%2.2f\n' % (tibberHour, (price['total']) * 100))
            # publish MQTT-Daten für den Graphen
            os.system('mosquitto_pub -r -t openWB/global/awattar/pricelist -m "$(cat /var/www/html/openWB/ramdisk/awattargraphlist)"')
    else:
        # Fehler in Antwort
        writeLogEntry('Fehler in Tibber-Antwort.')
else:
    # keine Antwort
    writeLogEntry('404 NOT FOUND - keine Tibber-Antwort.\n')

if not readPriceSuccessfull:
    # aktueller Preis wurde nicht gelesen, dann Preis auf 99.99ct/kWh setzen
    with open('/var/www/html/openWB/ramdisk/awattarprice', 'w') as awattarpricefile:
        writeLogEntry('Kein aktueller Preis erkannt, setze 99.99ct/kWh.\n')
        awattarpricefile.write('99.99\n')
