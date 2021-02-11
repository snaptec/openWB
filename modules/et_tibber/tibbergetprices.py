#!/usr/bin/python3
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

# Hilfsfunktionen
def write_log_entry(message):
    # schreibt Eintrag ins Log
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = timestamp + ' Modul tibbergetprices.py: ' + message + '\n'
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
                        exit_on_invalid_price_data('Kein aktueller Preis erkannt')
                else:
                    break
        return f2
    return dec

@try_api_call()
def readAPI(token, id):
    headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}
    data = '{ "query": "{viewer {home(id:\\"' + id + '\\") {currentSubscription {priceInfo {today {total startsAt} tomorrow {total startsAt}}}}}}" }'
    # Timeout für Verbindung = 2 sek und Antwort = 6 sek
    response = requests.post('https://api.tibber.com/v1-beta/gql', headers=headers, data=data, timeout=(2, 6))
    return response

# Hauptprogramm

# übergebene Paremeter auslesen
argumentsOK = False
if len(sys.argv) == 3:
    tibberToken = str(sys.argv[1])
    homeID = str(sys.argv[2])
else:
    # Hauptprogramm nur ausführen, wenn Argumente stimmen; erstes Argument ist immer Dateiname
    exit_on_invalid_price_data('Argumente fehlen oder sind fehlerhaft')

readPriceSuccessfull = False
# API abfragen
try:
    response = readAPI(tibberToken, homeID)
    response.raise_for_status()
except requests.exceptions.HTTPError as errh:
    exit_on_invalid_price_data('Http Error: ' + str(errh))
except requests.exceptions.ConnectionError as errc:
    exit_on_invalid_price_data('Error Connecting:' + str(errc))
except requests.exceptions.RequestException as err:
    exit_on_invalid_price_data('OOps: sonstiger Fehler:' + str(err))

# Bei Erfolg JSON auswerten
try:
    tibber_json = response.json()
except:
    exit_on_invalid_price_data('Korruptes JSON')

if not 'errors' in tibber_json:
    # extrahiere Preise für heute, sortiert nach Zeitstempel
    try:
        today_prices = sorted(tibber_json['data']['viewer']['home']['currentSubscription']['priceInfo']['today'], key=lambda k: (k['startsAt'], k['total']))
    except:
        exit_on_invalid_price_data('Korrupte Preisdaten')
    # extrahiere Preise für morgen, sortiert nach Zeitstempel
    try:
        tomorrow_prices = sorted(tibber_json['data']['viewer']['home']['currentSubscription']['priceInfo']['tomorrow'], key=lambda k: (k['startsAt'], k['total']))
    except:
        exit_on_invalid_price_data('Korrupte Preisdaten')

    # alle Zeiten in UTC verarbeiten
    now = datetime.now(timezone.utc)  # timezone-aware datetime-object in UTC
    now_full_hour = now.replace(minute=0, second=0, microsecond=0)  # volle Stunde
    preisliste = []
    preise_ok = False
    for price_data in today_prices:
        # konvertiere Time-String (Format 2021-02-06T00:00:00+01:00) in Datetime-Object
        # entferne ':' in Timezone, da nicht von strptime unterstützt
        time_str = ''.join(price_data['startsAt'].rsplit(':', 1))
        startzeit_localized = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S%z')
        # und konvertiere nach UTC
        startzeit_utc = startzeit_localized.astimezone(timezone.utc)
        #Preisliste beginnt immer mit aktueller Stunde
        if (startzeit_utc >= now_full_hour):
            if (startzeit_utc == now_full_hour):
                preise_ok = True
            bruttopreis = price_data['total'] * 100
            bruttopreis_str = str('%.2f' % round(bruttopreis, 2))
            preisliste.append({str('%d' % startzeit_utc.timestamp()) : bruttopreis_str})
    if (not preise_ok):
        exit_on_invalid_price_data('Aktueller Preis nicht gefunden')
    for price_data in tomorrow_prices:
        # konvertiere Time-String (Format 2021-02-06T00:00:00+01:00) in Datetime-Object
        # entferne ':' in Timezone, da nicht von strptime unterstützt
        time_str = ''.join(price_data['startsAt'].rsplit(':', 1))
        startzeit_utc = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S%z')
        bruttopreis = price_data['total'] * 100
        bruttopreis_str = str('%.2f' % round(bruttopreis, 2))
        preisliste.append({str('%d' % startzeit_utc.timestamp()) : bruttopreis_str})

    with open('/var/www/html/openWB/ramdisk/etproviderprice', 'w') as etprovider_pricefile, \
         open('/var/www/html/openWB/ramdisk/etprovidergraphlist', 'w') as etprovider_graphlistfile:
        # Preisliste durchlaufen und in ramdisk
        for index, preise in enumerate(preisliste):
            for startzeit, preis in preise.items():
                etprovider_graphlistfile.write('%s, %s\n' % (startzeit, preis))
                if (index == 0):
                    # erster Eintrag ist aktueller Preis
                    etprovider_pricefile.write('%s\n' % preis)

    #publish MQTT-Daten für Preis und Graph
    os.system('mosquitto_pub -r -t openWB/global/awattar/pricelist -m "$(cat /var/www/html/openWB/ramdisk/etprovidergraphlist)"')
    os.system('mosquitto_pub -r -t openWB/global/awattar/ActualPriceForCharging -m "$(cat /var/www/html/openWB/ramdisk/etproviderprice)"')

else:
    # Fehler in Antwort
    error = tibber_json['errors'][0]['message']
    exit_on_invalid_price_data('Fehler in Tibber-Antwort: ' + error)
