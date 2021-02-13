#!/usr/bin/python3
# coding: utf8

#########################################################
#
# liest von aWATTar die stündlichen Preise für heute und morgen,
# erstellt daraus die Datei für den Graphen und liefert den aktuell
# gültigen Strompreis
#
# setzt aktuellen Strompreis auf 99.99ct/kWh, wenn nichts empfangen wird
#
# benötigt als Parameter die Landeskennung (at/de), den individuellen Basispreis
# des Anschlusses (kann auch 0 sein) und das Debug-Level
#
# Preisliste in UTC und ct/kWh
#
# 2021 Michael Ortenstein
# This file is part of openWB
#
#########################################################

import os
import sys
import json
from time import sleep
from datetime import datetime, timezone, timedelta
import requests

readPriceSuccessfull = False
preise_ok = False
preisliste = []
landeskennung = ''
basispreis = ''
laenderdaten = {
    'at': {
        'url': 'https://api.awattar.at/v1/marketdata',
        # Berechnung Brutto-Arbeitspreis für Österreich nicht möglich, da wesentlich komplexer.
        # Antwort aWATTar:
        # In Österreich werden Netzentgelte/Abgaben ganz anderes behandelt und sind im Unterschied zu Deutschland
        # auch nicht Teil des Vertrages mit aWATTar. In Österreich haben wir keine Möglichkeit, die Netzentgelte
        # vorab eindeutig zu bestimmen und führen dies normalerweise auch nicht auf. Es ist in Österreich auch möglich,
        # dass die Netzentgelte nicht an uns, sondern direkt an den Netzbetreiber entrichtet werden.
        # In anderen Worten, leider kann man das Verfahren aus Deutschland in Österreich nicht anwenden.
        'umsatzsteuer': 1,
        'awattargebuehr': 0
    },
    'de': {
        'url': 'https://api.awattar.de/v1/marketdata',
        'umsatzsteuer': 1.19,
        'awattargebuehr': 0.25
    }
}

# Hilfsfunktionen
def write_log_entry(message):
    # schreibt Eintrag ins Log
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = timestamp + ' Modul awattargetprices.py: ' + message + '\n'
    with open('/var/www/html/openWB/ramdisk/openWB.log', 'a') as f:
        f.write(line)

def exit_on_invalid_price_data(error):
    # wenn kein aktueller Preis erkannt wurde,
    # schreibt 99.99ct/kWh in Preis-Datei und füllt Chart-Array für die nächsten 12 Stunden damit,
    # schreibt Fehler ins Log
    with open('/var/www/html/openWB/ramdisk/etproviderprice', 'w') as etprovider_pricefile, \
         open('/var/www/html/openWB/ramdisk/etprovidergraphlist', 'w') as etprovider_graphlistfile:
        etprovider_pricefile.write('99.99\n')
        now = datetime.now(timezone.utc)  # timezone-aware datetime-object in UTC
        timestamp = now.replace(minute=0, second=0, microsecond=0)  # volle Stunde
        for i in range(12):
            etprovider_graphlistfile.write('%d, 99.99\n' % timestamp.timestamp())
            timestamp = timestamp + timedelta(hours=1)
    write_log_entry(error + ', setze Preis auf 99.99ct/kWh.')
    #publish MQTT-Daten für Preis und Graph
    os.system('mosquitto_pub -r -t openWB/global/awattar/pricelist -m "$(cat /var/www/html/openWB/ramdisk/etprovidergraphlist)"')
    os.system('mosquitto_pub -r -t openWB/global/awattar/ActualPriceForCharging -m "$(cat /var/www/html/openWB/ramdisk/etproviderprice)"')
    exit()

def try_api_call(max_tries=3, delay=5, backoff=2, exceptions=(Exception,), hook=None):
    #  copied from https://gist.github.com/n1ywb/2570004,
    #  adfjusted to be used with python3
    #
    #  Copyright 2012 by Jeff Laughlin Consulting LLC
    #
    # Permission is hereby granted, free of charge, to any person obtaining a copy
    # of this software and associated documentation files (the "Software"), to deal
    # in the Software without restriction, including without limitation the rights
    # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    # copies of the Software, and to permit persons to whom the Software is
    # furnished to do so, subject to the following conditions:
    #
    # The above copyright notice and this permission notice shall be included in
    # all copies or substantial portions of the Software.
    """Function decorator implementing retrying logic.
    delay: Sleep this many seconds * backoff * try number after failure
    backoff: Multiply delay by this factor after each failure
    exceptions: A tuple of exception classes; default (Exception,)
    hook: A function with the signature myhook(tries_remaining, exception, delay);
          default None
    The decorator will call the function up to max_tries times if it raises
    an exception.
    By default it catches instances of the Exception class and subclasses.
    This will recover after all but the most fatal errors. You may specify a
    custom tuple of exception classes with the 'exceptions' argument; the
    function will only be retried if it raises one of the specified
    exceptions.
    Additionally you may specify a hook function which will be called prior
    to retrying with the number of remaining tries and the exception instance;
    see given example. This is primarily intended to give the opportunity to
    log the failure. Hook is not called after failure if no retries remain.
    """
    def dec(func):
        def f2(*args, **kwargs):
            mydelay = delay
            tries = list(range(max_tries))
            tries.reverse()
            for tries_remaining in tries:
                if debugLevel > 0:
                    write_log_entry("Abfrage aWATTar-API")
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if tries_remaining > 0:
                        write_log_entry("Fehler bei der API-Abfrage, %d Versuche übrig, versuche erneut in %s Sekunden" % (tries_remaining, mydelay))
                        if hook is not None:
                            hook(tries_remaining, e, mydelay)
                        sleep(mydelay)
                        mydelay = mydelay * backoff
                    else:
                        raise
                else:
                    break
        return f2
    return dec

@try_api_call()
def readAPI(url):
    # Timeout für Verbindung = 2 sek und Antwort = 6 sek
    response = requests.get(url, headers={'Content-Type': 'application/json'}, timeout=(2, 6))
    return response

# Hauptprogramm

# übergebene Paremeter auslesen
if len(sys.argv) == 4:
    landeskennung = str(sys.argv[1])
    basispreis = str(sys.argv[2])
    debugLevel = int(sys.argv[3])
    if landeskennung in laenderdaten:
        try:
            basispreis = float(basispreis)
        except ValueError:
            exit_on_invalid_price_data('Basispreis fehlerhaft')
    else:
        exit_on_invalid_price_data('Landeskennung unbekannt')
else:
    exit_on_invalid_price_data('Argumente fehlen')

# Hauptprogramm nur ausführen, wenn Argumente stimmen; erstes Argument ist immer Dateiname
# API abfragen, retry bei Timeout
try:
    response = readAPI(laenderdaten[landeskennung]['url'])
except:
    exit_on_invalid_price_data('Fataler Fehler bei API-Abfrage')

# sind sonstige-Fehler aufgetreten?
try:
    response.raise_for_status()
except Exception as e:
    exit_on_invalid_price_data(str(e))

# Bei Erfolg JSON auswerten
if debugLevel > 0:
    write_log_entry("Keine Fehlermeldung in aWATTar-Antwort, lese JSON")

try:
    marketprices = json.loads(response.text)['data']
except:
    exit_on_invalid_price_data('Korruptes JSON')

if debugLevel > 0:
    write_log_entry("aWATTar-Preisliste extrahiert")

# Liste sortiert nach Zeitstempel
sorted_marketprices = sorted(marketprices, key=lambda k: k['start_timestamp'])

# alle Zeiten in UTC verarbeiten
now = datetime.now(timezone.utc)  # timezone-aware datetime-object in UTC
now_full_hour = now.replace(minute=0, second=0, microsecond=0)  # volle Stunde
for price_data in sorted_marketprices:
    startzeit_utc = datetime.utcfromtimestamp(price_data['start_timestamp']/1000)  # Zeitstempel kommt von API in UTC mit Millisekunden, UNIX ist ohne
    startzeit_utc = startzeit_utc.replace(tzinfo=timezone.utc)  # Objekt von naive nach timezone-aware, hier UTC
    if (startzeit_utc >= now_full_hour):
        if (startzeit_utc == now_full_hour):
            if debugLevel > 0:
                write_log_entry("Aktueller Preis wurde gelesen")
            preise_ok = True
        if (landeskennung == 'de'):
            # Bruttopreis Deutschland [ct/kWh] = ((marketpriceAusAPI/10) * 1.19) + Awattargebühr + Basispreis
            bruttopreis = (price_data['marketprice']/10 * laenderdaten[landeskennung]['umsatzsteuer']) + laenderdaten[landeskennung]['awattargebuehr'] + basispreis
            bruttopreis_str = str('%.2f' % round(bruttopreis, 2))
        else:
            # für Österreich keine Berechnung möglich, daher nur marketpriceAusAPI benutzen
            bruttopreis_str = str('%.2f' % round(price_data['marketprice']/10, 2))
        preisliste.append({str('%d' % startzeit_utc.timestamp()) : bruttopreis_str})

if (preise_ok):
    # Preisliste liegt jetzt vor in UTC und ct/kWh, sortiert nach Zeit
    with open('/var/www/html/openWB/ramdisk/etproviderprice', 'w') as etprovider_pricefile, \
         open('/var/www/html/openWB/ramdisk/etprovidergraphlist', 'w') as etprovider_graphlistfile:
        # Preisliste durchlaufen und in ramdisk
        for index, preise in enumerate(preisliste):
            for startzeit, preis in preise.items():
                etprovider_graphlistfile.write('%s, %s\n' % (startzeit, preis))
                if (index == 0):
                    # erster Eintrag ist aktueller Preis
                    etprovider_pricefile.write('%s\n' % preis)
else:
    exit_on_invalid_price_data('Preisliste unvollständig')

#publish MQTT-Daten für Preis und Graph
os.system('mosquitto_pub -r -t openWB/global/awattar/pricelist -m "$(cat /var/www/html/openWB/ramdisk/etprovidergraphlist)"')
os.system('mosquitto_pub -r -t openWB/global/awattar/ActualPriceForCharging -m "$(cat /var/www/html/openWB/ramdisk/etproviderprice)"')
