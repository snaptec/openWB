#!/usr/bin/python3
# coding: utf8

#########################################################
#
# liest von Tibber die stündlichen Preise für heute und wenn verfügbar morgen,
# erstellt daraus die Datei für den Chart und liefert den aktuell
# gültigen Strompreis
#
# erwartet Stundenpreise, d.h. für jede Stunde eine Preisauskunft
# setzt aktuellen Strompreis im Fehlerfall auf 99.99ct/kWh
#
# benötigt als Parameter den persönlichen Tibber-Token, die home_id
# des Anschlusses und das Debug-Level
#
# Preisliste in UTC und ct/kWh
# Aufbau Datei:
# Zeile 1: Dateiname des Moduls
# Zeile 2 ff: timestamp, price
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

# aus Parameterübergabe
tibber_token = ''
home_id = ''
debug_level = 0  # eingeteilt in 0=aus, 1=wenig, 3=alles
# sonstiges
pricelist_provider = 'Tibber'
read_price_successfull = False
tibber_pricelist = []  # neue Liste
tibber_pricelist_old = []  #  vorhandene Liste
pricelist_provider_old = ''  # für vorhandene Liste veranwtortliches Modul
prices_ok = False
module_starttime = datetime.now()

# Hilfsfunktionen

def publish_price_data():
    with open('/var/www/html/openWB/ramdisk/etproviderprice', 'w') as current_price_file, \
         open('/var/www/html/openWB/ramdisk/etprovidergraphlist', 'w') as pricelist_file:
        pricelist_file.write('%s\n' % pricelist_provider)  # erster Eintrag ist für Preisliste verantwortliches Modul
        # Preisliste durchlaufen und in ramdisk
        for index, price_data in enumerate(tibber_pricelist):
            pricelist_file.write('%s, %s\n' % (price_data[0], price_data[1]))  # Timestamp, Preis
            if (index == 0):
                # erster Eintrag ist aktueller Preis
                current_price_file.write('%s\n' % price_data[1])
    #publish MQTT-Daten für Preis und Graph
    os.system('mosquitto_pub -r -t openWB/global/awattar/pricelist -m "$(cat /var/www/html/openWB/ramdisk/etprovidergraphlist)"')
    os.system('mosquitto_pub -r -t openWB/global/awattar/ActualPriceForCharging -m "$(cat /var/www/html/openWB/ramdisk/etproviderprice)"')
    module_runtime = datetime.now() - module_starttime
    module_runtime = module_runtime.total_seconds()
    write_log_entry('Modullaufzeit ' + str(module_runtime) + ' s', 1)

def write_log_entry(message, min_debug_level):
    # schreibt Eintrag ins Log wenn der mindest debug_level >= der übergebene ist
    if min_debug_level >= 0: #debug_level:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line = timestamp + ' Modul tibbergetprices.py: ' + message + '\n'
        with open('/var/www/html/openWB/ramdisk/openWB.log', 'a') as f:
            f.write(line)

def exit_on_invalid_price_data(error):
    # wenn kein aktueller Preis erkannt wurde,
    # schreibt 99.99ct/kWh in Preis-Datei und füllt Chart-Array für die nächsten 9 Stunden damit,
    # schreibt Fehler ins Log
    with open('/var/www/html/openWB/ramdisk/etproviderprice', 'w') as current_price_file, \
         open('/var/www/html/openWB/ramdisk/etprovidergraphlist', 'w') as pricelist_file:
        current_price_file.write('99.99\n')
        pricelist_file.write('%s\n' % pricelist_provider)  # erster Eintrag ist für Preisliste verantwortliches Modul
        now = datetime.now(timezone.utc)  # timezone-aware datetime-object in UTC
        timestamp = now.replace(minute=0, second=0, microsecond=0)  # volle Stunde
        for i in range(9):
            pricelist_file.write('%d, 99.99\n' % timestamp.timestamp())
            timestamp = timestamp + timedelta(hours=1)
    write_log_entry(error, 0)
    write_log_entry('Setze Preis auf 99.99ct/kWh.', 0)
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
                write_log_entry("Versuch Abfrage Tibber-API", 1)
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if tries_remaining > 0:
                        write_log_entry("Fehler bei der API-Abfrage, %d Versuche übrig, versuche erneut in %s Sekunden" % (tries_remaining, mydelay), 1)
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
def readAPI(token, id):
    headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}
    data = '{ "query": "{viewer {home(id:\\"' + id + '\\") {currentSubscription {priceInfo {today {total startsAt} tomorrow {total startsAt}}}}}}" }'
    # Timeout für Verbindung = 2 sek und Antwort = 6 sek
    response = requests.post('https://api.tibber.com/v1-beta/gql', headers=headers, data=data, timeout=(2, 6))
    return response

def get_utcfromtimestamp(timestamp):
    # gibt timezone-aware Datetime-Objekt zurück in UTC
    datetime_obj = datetime.utcfromtimestamp(float(timestamp))  # Zeitstempel von String nach Datetime-Objekt
    datetime_obj = datetime_obj.replace(tzinfo=timezone.utc)  # Objekt von naive nach timezone-aware, hier UTC
    return datetime_obj

def cleanup_pricelist(pricelist):
    # bereinigt Preisliste, löscht Einträge die älter als aktuelle Stunde sind
    # und über morgen hinausgehen
    # wenn der erste Preis nicht für die aktuelle Stunde ist, wird leere Liste zurückgegeben
    # prüft auf Abstand der Preise: ist dieser >1h, wird Liste ab diesem Punkt ignoriert
    if len(pricelist) > 0:
        now = datetime.now(timezone.utc)  # timezone-aware datetime-object in UTC
        now_full_hour = now.replace(minute=0, second=0, microsecond=0)  # volle Stunde
        starttime_utc_prev = now  # speichert in Schleife Zeitstempel des vorherigen Listeneintrags
        for index, price in enumerate(pricelist[:]):  # über Kopie der Liste iterieren, um das Original zu manipulieren
            starttime_utc = get_utcfromtimestamp(price[0])  # Start-Zeitstempel aus Preisliste umwandeln
            if starttime_utc < now_full_hour or starttime_utc.date() > now.date() + timedelta(days=1):
                pricelist.remove(price)
            if index > 0:
                # wenn der Abstand zum letzten Preis in Liste > 1 Std, dann Rest der Liste entfernen und Ende
                hourdiff = divmod((starttime_utc - starttime_utc_prev).total_seconds(), 60)
                if hourdiff != (60.0, 0.0):
                    del pricelist[index:]
                    break
            starttime_utc_prev = starttime_utc
        starttime_utc = get_utcfromtimestamp(pricelist[0][0])
        if starttime_utc != now_full_hour:  # erster Preis nicht der aktuelle
            return []
    return pricelist

def get_updated_pricelist():
    # API abfragen, retry bei Timeout
    try:
        response = readAPI(tibber_token, home_id)
    except:
        return False, 'Fataler Fehler bei API-Abfrage'
    write_log_entry('Antwort auf Abfrage erhalten', 2)
    # sind sonstige-Fehler aufgetreten?
    try:
        response.raise_for_status()
    except Exception as e:
        return False, str(e)
    # Bei Erfolg JSON auswerten
    write_log_entry('Ermittle JSON aus Tibber-Antwort', 1)
    try:
        tibber_json = response.json()
    except:
        return False, 'Korruptes JSON'
    if not 'errors' in tibber_json:
        write_log_entry("Keine Fehlermeldung in Tibber-Antwort, werte JSON aus", 1)
        # extrahiere Preise für heute, sortiert nach Zeitstempel
        try:
            today_prices = sorted(tibber_json['data']['viewer']['home']['currentSubscription']['priceInfo']['today'], key=lambda k: (k['startsAt'], k['total']))
        except:
            return False, 'Korrupte Preisdaten'
        # extrahiere Preise für morgen, sortiert nach Zeitstempel
        try:
            tomorrow_prices = sorted(tibber_json['data']['viewer']['home']['currentSubscription']['priceInfo']['tomorrow'], key=lambda k: (k['startsAt'], k['total']))
        except:
            return False, 'Korrupte Preisdaten'
        write_log_entry("Tibber-Preisliste extrahiert", 1)
        # alle Zeiten in UTC verarbeiten
        now = datetime.now(timezone.utc)  # timezone-aware datetime-object in UTC
        now_full_hour = now.replace(minute=0, second=0, microsecond=0)  # volle Stunde
        write_log_entry('Formatiere und analysiere Preisliste von heute', 1)
        for price_data in today_prices:
            # konvertiere Time-String (Format 2021-02-06T00:00:00+01:00) in Datetime-Object
            # entferne ':' in Timezone, da nicht von strptime unterstützt
            time_str = ''.join(price_data['startsAt'].rsplit(':', 1))
            startzeit_localized = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S%z')
            # und konvertiere nach UTC
            starttime_utc = startzeit_localized.astimezone(timezone.utc)
            #Preisliste beginnt immer mit aktueller Stunde
            if (starttime_utc >= now_full_hour):
                if (starttime_utc == now_full_hour):
                    write_log_entry("Aktueller Preis wurde gelesen", 1)
                    prices_ok = True
                bruttopreis = price_data['total'] * 100
                bruttopreis_str = str('%.2f' % round(bruttopreis, 2))
                tibber_pricelist.append([str('%d' % starttime_utc.timestamp()), bruttopreis_str])
        if (not prices_ok):
            return False, 'Aktueller Preis nicht lesbar'
        write_log_entry('Preise von heute gelesen', 2)
        write_log_entry('Formatiere und analysiere Preisliste morgen', 1)
        for price_data in tomorrow_prices:
            # konvertiere Time-String (Format 2021-02-06T00:00:00+01:00) in Datetime-Object
            # entferne ':' in Timezone, da nicht von strptime unterstützt
            time_str = ''.join(price_data['startsAt'].rsplit(':', 1))
            starttime_utc = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S%z')
            bruttopreis = price_data['total'] * 100
            bruttopreis_str = str('%.2f' % round(bruttopreis, 2))
            tibber_pricelist.append([str('%d' % starttime_utc.timestamp()), bruttopreis_str])
        if len(tomorrow_prices) > 0:
            write_log_entry('Preise von morgen gelesen', 2)
        else:
            write_log_entry('Keine Preise von morgen empfangen', 2)
        return True, ''
    else:
        # Fehler in Antwort
        error = tibber_json['errors'][0]['message']
        return False, 'Fehler: ' + error

# Hauptprogramm

# übergebene Paremeter auslesen
write_log_entry('Lese Argumente', 1)
if len(sys.argv) == 4:
    tibber_token = str(sys.argv[1])
    home_id = str(sys.argv[2])
    debug_level = int(sys.argv[3])
else:
    exit_on_invalid_price_data('Argumente fehlen oder sind fehlerhaft')
write_log_entry('Argumente OK', 2)

# Hauptprogramm nur ausführen, wenn Argumente stimmen; erstes Argument ist immer Dateiname
# bisherige Preisliste lesen
write_log_entry('Lese bisherige openWB-Strom-Preisliste', 1)
try:
    with open('/var/www/html/openWB/ramdisk/etprovidergraphlist', 'r') as pricelist_file:
        pricelist_provider_old = pricelist_file.readline().rstrip('\n')  # erste Zeile sollte für Preisliste verantwortliches Modul sein
        for prices in pricelist_file:  # dann restliche Zeilen als Preise mit Timestamp lesen
            price_items = prices.split(',')
            price_items = [item.strip() for item in price_items]
            tibber_pricelist_old.append(price_items)
    write_log_entry('Bisherige openWB-Strom-Preisliste gelesen', 2)
    read_price_successfull = True
except:
    write_log_entry("openWB-Strom-Preisliste konnte nicht gelesen werden, versuche Neuerstellung", 1)

if read_price_successfull and pricelist_provider == pricelist_provider_old:
    # Modul der bisherigen Liste ist mit diesem identisch, also Einträge in alter Preisliste benutzen und aufräumen
    write_log_entry('Bereinige bisherige openWB-Strom-Preisliste', 1)
    tibber_pricelist_old = cleanup_pricelist(tibber_pricelist_old)
    write_log_entry('Bisherige openWB-Strom-Preisliste bereinigt', 2)

    if len(tibber_pricelist_old) > 0:
        # mindestens der aktuelle Preis ist in der Liste
        write_log_entry('Bisherige openWB-Strom-Preisliste hat %d Eintraege' % len(tibber_pricelist_old), 2)
        if len(tibber_pricelist_old) < 11:
            # weniger als 11 Stunden in bisheriger Liste: versuche, die Liste neu abzufragen
            # dementsprechend auch bei vorherigem Fehler: 9 Einträge zu 99.99ct/kWh
            write_log_entry('Versuche, weitere Preise abzufragen', 1)
            read_price_successfull, error_msg = get_updated_pricelist()
            if read_price_successfull:
                write_log_entry('Abfrage der Preise erfolgreich', 2)
                write_log_entry('Publiziere Preisliste', 1)
                publish_price_data()
                exit()
            else:
                write_log_entry('Abfrage weiterer Preise nicht erfolgreich', 1)
        else:
            write_log_entry('Ausreichend zukuenftige Preise in bisheriger openWB-Strom-Preisliste', 2)
        # bisherige Liste hat ausreichend Preise für die Zukunft bzw.
        # mindestens den aktuellen Preis und Fehler bei der API-Abfrage
        tibber_pricelist = tibber_pricelist_old  # neue Liste ist bereinigte bisherige
        write_log_entry('Verwende Preise aus bereinigter bisheriger openWB-Strom-Preisliste', 1)
        write_log_entry('Publiziere Preisliste', 1)
        publish_price_data()
        exit()

if pricelist_provider != pricelist_provider_old:
    write_log_entry('Bisherige Preiliste wurde von Modul %s erstellt' % pricelist_provider_old, 1)
    write_log_entry('Wechsel auf Modul %s' % pricelist_provider, 1)

# bisherige Preisliste leer, oder neuer Provider: in jedem Fall neue Abfrage und
# bei andauerndem Fehler Preis auf 99.99ct/kWh setzen
read_price_successfull, error_msg = get_updated_pricelist()
if read_price_successfull:
    write_log_entry('Publiziere Preisliste', 1)
    publish_price_data()
else:
    exit_on_invalid_price_data(error_msg)
