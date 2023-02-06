#!/usr/bin/python3
# coding: utf8

#########################################################
#
# liest von Tibber die stündlichen Preise für heute und morgen,
# erstellt daraus die Preislisten-Datei für den Graphen und
# Datei mit aktuell gültigem Strompreis
#
# erwartet von API Stundenpreise, d.h. für jede Stunde eine Preisauskunft
# setzt aktuellen Strompreis (und für kommende 9 Std) im Fehlerfall auf _failure_price
#
# Aufruf als Main
# oder nach Import: update_pricedata(tibber_token, home_id, debug_level)
#
# param: tibber_token
# param: home_id
# param: Debug-Level
#
# Preisliste in UTC und ct/kWh, Aufbau Datei:
# Zeile 1: Name des Moduls, z. B. Tibber
# Zeile 2 ff: timestamp,price
#
# 2021 Michael Ortenstein
# This file is part of openWB
#
#########################################################

import os
import sys
import re
import json
from time import sleep
from datetime import datetime, date, timezone, timedelta
import requests
import atexit

#########################################################
#
# Setup
#
#########################################################

MODULE_NAME = 'Tibber'

_openWB_debug_level = 0
_module_starttime = 0
_failure_price = 1000.00

#########################################################
#
# private Hilfsfunktionen
#
#########################################################

def _check_args(arg1, arg2, arg3):
    # entferne alles außer Buchstaben, Zahlen, - und _ aus Parametern
    arg1_str = re.sub('[^A-Za-z0-9_-]+', '', arg1)  # tibber_token
    arg2_str = re.sub('[^A-Za-z0-9_-]+', '', arg2)  # home_id
    arg3_str = re.sub('[^0-9]+', '', arg3)  # Debug-Level
    try:
        arg3_int = int(arg3_str)
    except:
        raise ValueError('3. Parameter (Debug-Level = "' + arg3_str + '") ist keine Zahl') from None
    return arg1_str, arg2_str, arg3_int

def _read_args():
    # gibt Kommandozeilenparameter zurück
    if len(sys.argv) == 4:
        # sys.argv[0] : erstes Argument ist immer Dateiname
        try:
            tibber_token, home_id, debug_level = _check_args(sys.argv[1], sys.argv[2], sys.argv[3])
        except:
            raise
    else:
        raise ValueError('Parameteranzahl falsch (' + str(len(sys.argv) - 1) + ' uebergeben aber 3 gefordert)')
    return tibber_token, home_id, debug_level

def _write_log_entry(message, msg_debug_level = 0):
    # schreibt Eintrag ins Log je nach Level
    global _openWB_debug_level
    if msg_debug_level == 0 or _openWB_debug_level is None or msg_debug_level <= _openWB_debug_level:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S:')
        line = timestamp + ' Modul tibbergetprices.py: ' + message + '\n'
        with open('/var/www/html/openWB/ramdisk/openWB.log', 'a') as f:
            f.write(line)

def _publish_price_data(pricelist_to_publish, current_module_name):
    # schreibt Preisliste und aktuellen Preis in Dateien und veröffentlicht die MQTT-Topics
    with open('/var/www/html/openWB/ramdisk/etproviderprice', 'w') as file_current_price, \
         open('/var/www/html/openWB/ramdisk/etprovidergraphlist', 'w') as file_pricelist:
        file_pricelist.write('%s\n' % current_module_name )  # erster Eintrag ist für Preisliste verantwortliches Modul
        # Preisliste durchlaufen und in ramdisk
        for index, price_data in enumerate(pricelist_to_publish):
            file_pricelist.write('%s,%s\n' % (price_data[0], price_data[1]))  # Timestamp, Preis
            if (index == 0):
                # erster Eintrag ist aktueller Preis
                file_current_price.write('%s\n' % price_data[1])
    #publish MQTT-Daten für Preis und Graph
    os.system('mosquitto_pub -r -t openWB/global/awattar/pricelist -m "$(cat /var/www/html/openWB/ramdisk/etprovidergraphlist)"')
    os.system('mosquitto_pub -r -t openWB/global/awattar/ActualPriceForCharging -m "$(cat /var/www/html/openWB/ramdisk/etproviderprice)"')

def _exit_on_invalid_price_data(error, current_module_name):
    # schreibt _failure_price in Preis-Datei und füllt Chart-Array für die nächsten 9 Stunden damit,
    # schreibt Fehler ins Log
    with open('/var/www/html/openWB/ramdisk/etproviderprice', 'w') as file_current_price, \
         open('/var/www/html/openWB/ramdisk/etprovidergraphlist', 'w') as file_pricelist:
        file_current_price.write(str(_failure_price) + '\n')
        file_pricelist.write('%s\n' % current_module_name)  # erster Eintrag ist für Preisliste verantwortliches Modul
        now = datetime.now(timezone.utc)  # timezone-aware datetime-object in UTC
        timestamp = now.replace(minute=0, second=0, microsecond=0)  # volle Stunde
        for i in range(9):
            file_pricelist.write('%d, %f\n' % (timestamp.timestamp(), _failure_price))
            timestamp = timestamp + timedelta(hours=1)
    _write_log_entry(error, 0)
    _write_log_entry('Setze Preis auf ' + str(_failure_price) + 'ct/kWh.', 0)
    #publish MQTT-Daten für Preis und Graph
    os.system('mosquitto_pub -r -t openWB/global/awattar/pricelist -m "$(cat /var/www/html/openWB/ramdisk/etprovidergraphlist)"')
    os.system('mosquitto_pub -r -t openWB/global/awattar/ActualPriceForCharging -m "$(cat /var/www/html/openWB/ramdisk/etproviderprice)"')
    exit()

def _try_api_call(max_tries=3, delay=5, backoff=2, exceptions=(Exception,), hook=None):
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
                _write_log_entry('Abfrage Tibber-API', 1)
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if tries_remaining > 0:
                        _write_log_entry("Fehler bei der API-Abfrage, %d Versuche übrig, versuche erneut in %s Sekunden" % (tries_remaining, mydelay), 0)
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

@_try_api_call()
def _readAPI(token, id):
    headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}
    data = '{ "query": "{viewer {home(id:\\"' + id + '\\") {currentSubscription {priceInfo {today {total startsAt} tomorrow {total startsAt}}}}}}" }'
    # Timeout für Verbindung = 2 sek und Antwort = 6 sek
    response = requests.post('https://api.tibber.com/v1-beta/gql', headers=headers, data=data, timeout=(2, 6))
    return response

def _get_utcfromtimestamp(timestamp):
    # erwartet timestamp Typ float
    # gibt timezone-aware Datetime-Objekt zurück in UTC
    datetime_obj = datetime.utcfromtimestamp(timestamp)  # Zeitstempel von String nach Datetime-Objekt
    datetime_obj = datetime_obj.replace(tzinfo=timezone.utc)  # Objekt von naive nach timezone-aware, hier UTC
    return datetime_obj

def _cleanup_pricelist(pricelist):
    # bereinigt sortierte Preisliste, löscht Einträge die älter als aktuelle Stunde sind
    # und über morgen hinausgehen
    # wenn der erste Preis nicht für die aktuelle Stunde ist, wird leere Liste zurückgegeben
    # prüft auf Abstand der Preise: ist dieser >1h, wird Liste ab diesem Punkt abgeschnitten
    if len(pricelist) > 0:
        now = datetime.now(timezone.utc)  # timezone-aware datetime-object in UTC
        now_full_hour = now.replace(minute=0, second=0, microsecond=0)  # volle Stunde
        now_full_hour_timestamp = datetime.timestamp(now_full_hour)
        # zuerst filtern auf "ab diese Stunde" bis "längstens morgen"
        for index, price in enumerate(pricelist[:]):  # über Kopie der Liste iterieren, um das Original zu manipulieren
            try:
                starttime_utc = _get_utcfromtimestamp(float(price[0]))  # Start-Zeitstempel aus Preisliste umwandeln
            except:
                raise TypeError('Zeitstempel-Umwandlung fehlgeschlagen') from None
            # ältere als aktuelle Stunde und weiter als morgen löschen
            if (float(price[0]) < now_full_hour_timestamp) or (starttime_utc.date() > now.date() + timedelta(days=1)):
                pricelist.remove(price)
        # jetzt prüfen auf Start mit aktueller Stunde und Stundenabstände
        if len(pricelist) > 0:
            timestamp_prev = float(pricelist[0][0])  # erster Listeneintrag
            starttime_utc = _get_utcfromtimestamp(float(pricelist[0][0]))
            if _get_utcfromtimestamp(timestamp_prev) == now_full_hour:  # erster Preis ist der von aktueller Stunde
                for index, price in enumerate(pricelist[:]):  # über Kopie der Liste iterieren, um das Original zu manipulieren
                    if index > 0:
                        timestamp = float(price[0])
                        secondsdiff = timestamp - timestamp_prev
                        timestamp_prev = float(price[0])
                        if secondsdiff != 3600.0:  # ist Abstand <> 1h dann ab hier Liste löschen
                            del pricelist[index:]
                            break
            else:
                return []
            return pricelist
    return []

def _get_updated_pricelist():
    # API abfragen, retry bei Timeout
    # Rückgabe ist empfangene bereinigte Preisliste mit aktuellem Preis als ersten Eintrag
    # Bei Fehler oder leerer Liste wird Exception geworfen
    try:
        response = _readAPI(tibber_token, home_id)
    except:
        raise RuntimeError('Fataler Fehler bei API-Abfrage') from None
    _write_log_entry('Antwort auf Abfrage erhalten', 2)
    # sind sonstige-Fehler aufgetreten?
    try:
        response.raise_for_status()
    except:
        raise
    # Bei Erfolg JSON auswerten
    _write_log_entry('Ermittle JSON aus Tibber-Antwort', 1)
    try:
        tibber_json = response.json()
    except:
        raise RuntimeError('Korruptes JSON') from None
    if not 'errors' in tibber_json:
        _write_log_entry("Keine Fehlermeldung in Tibber-Antwort, werte JSON aus", 1)
        # extrahiere Preise für heute, sortiert nach Zeitstempel
        try:
            today_prices = sorted(tibber_json['data']['viewer']['home']['currentSubscription']['priceInfo']['today'], key=lambda k: (k['startsAt'], k['total']))
        except:
            raise RuntimeError('Korruptes JSON') from None
        # extrahiere Preise für morgen, sortiert nach Zeitstempel
        try:
            tomorrow_prices = sorted(tibber_json['data']['viewer']['home']['currentSubscription']['priceInfo']['tomorrow'], key=lambda k: (k['startsAt'], k['total']))
        except:
            raise RuntimeError('Korruptes JSON') from None
        sorted_marketprices = today_prices + tomorrow_prices
        _write_log_entry("Tibber-Preisliste extrahiert", 1)
        # alle Zeiten in UTC verarbeiten
        now = datetime.now(timezone.utc)  # timezone-aware datetime-object in UTC
        now_full_hour = now.replace(minute=0, second=0, microsecond=0)  # volle Stunde
        _write_log_entry('Formatiere und analysiere Preisliste', 1)
        pricelist = []
        for price_data in sorted_marketprices:
            # konvertiere Time-String (Format 2021-02-06T00:00:00+01:00) in Datetime-Object
            # entferne ':' in Timezone, da nicht von strptime unterstützt
            time_str = ''.join(price_data['startsAt'].rsplit(':', 1))
            startzeit_localized = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S.%f%z')
            # und konvertiere nach UTC
            starttime_utc = startzeit_localized.astimezone(timezone.utc)
            #Preisliste beginnt immer mit aktueller Stunde
            bruttopreis = price_data['total'] * 100
            bruttopreis_str = str('%.2f' % round(bruttopreis, 2))
            pricelist.append([str('%d' % starttime_utc.timestamp()), bruttopreis_str])
        try:
            pricelist = _cleanup_pricelist(pricelist)
        except:
            raise
        if len(pricelist) == 0:
            raise RuntimeError('Aktueller Preis konnte nicht ermittelt werden')
        else:
            _write_log_entry('Aktueller Preis ist %s ct/kWh' % pricelist[0][1], 2)
        return pricelist
    else:
        # Fehler in Antwort
        error = tibber_json['errors'][0]['message']
        raise RuntimeError(error) from None

def _get_existing_pricelist():
    # liest vorhanden Preisliste aus Datei
    # return: Preisliste, Name des Moduls verantwortlich für Preisliste
    existing_pricelist = []  # vorhandene Liste
    try:
        with open('/var/www/html/openWB/ramdisk/etprovidergraphlist', 'r') as file_pricelist:
            module_name_in_file = file_pricelist.readline().rstrip('\n')  # erste Zeile sollte für Preisliste verantwortliches Modul sein
            module_name_in_file = re.sub('[^A-Za-z0-9_-]', '', module_name_in_file)  # ggf. unerwünschte Zeichen entfernen
            for prices in file_pricelist:  # dann restliche Zeilen als Preise mit Timestamp lesen
                price_items = prices.split(',')
                price_items = [item.strip() for item in price_items]
                existing_pricelist.append(price_items)
    except:
        raise
    return existing_pricelist, module_name_in_file

def _convert_timestamp_to_str(timestamp):
    # konvertiert timestamp in UTC zu String (in Lokalzeit) Format: 11.01., 23:00 Uhr
    # ist das Datum heute, dann Format heute, 23:00 Uhr
    # ist das Datum morgen, dann Format morgen, 23:00 Uhr
    today = date.today()
    tomorrow = today + timedelta(days=1)
    datetime_obj = _get_utcfromtimestamp(timestamp)
    datetime_obj = datetime_obj.astimezone(tz=None)  # und nach lokal
    if today == datetime_obj.date():
        the_date = 'heute, '
    elif tomorrow == datetime_obj.date():
        the_date = 'morgen, '
    else:
        the_date = datetime_obj.strftime('%d.%m., ')
    the_time = datetime_obj.strftime('%H:%M Uhr')
    return (the_date + the_time)

def _log_module_runtime():
    # schreibt Modullaufzeit ins Logfile
    runtime = datetime.now() - _module_starttime
    runtime = runtime.total_seconds()
    _write_log_entry('Modullaufzeit ' + str(runtime) + ' s', 1)

#########################################################
#
# öffentliche Funktion
#
#########################################################

def update_pricedata(tibber_token, home_id, debug_level):
    global _openWB_debug_level
    global _module_starttime

    _module_starttime = datetime.now()
    # bei exit immer Laufzeit des Moduls bestimmen, Funktion aber nicht doppelt registrieren
    atexit.register(_log_module_runtime)
    if __name__ != '__main__':
        try:
            _check_args(tibber_token, home_id, debug_level)
        except Exception as e:
            _exit_on_invalid_price_data('Modul-Abbruch: ' + str(e), MODULE_NAME)

    _openWB_debug_level = debug_level  # zwecks Nutzung in Hilfsfunktionen
    _write_log_entry('Lese bisherige Preisliste', 1)
    pricelist_in_file = []
    module_name_in_file = None
    try:
        pricelist_in_file, module_name_in_file = _get_existing_pricelist()
    except Exception as e:
        _write_log_entry('Fehler: ' + str(e), 0)
        _write_log_entry("Vorhandene Preisliste konnte nicht gelesen werden, versuche Neuerstellung", 1)
    current_module_name = MODULE_NAME  # analog zu aWATTar, vielleicht gibt es irgendwann Ländervarianten
    if len(pricelist_in_file) > 0 and pricelist_in_file[0][1] == str(_failure_price):
        _write_log_entry('Bisherige Preisliste enthaelt nur Fehlerpreise ' + str(_failure_price) + 'ct/kWh', 1)
        _write_log_entry('Versuche, neue Preise von Tibber zu empfangen', 1)
    elif module_name_in_file != None and current_module_name != module_name_in_file:
        if module_name_in_file == '':
            log_text = 'Kein Modul für bisherige Preisliste identifizierbar'
        else:
            log_text = 'Bisherige Preisliste wurde von Modul ' + module_name_in_file + ' erstellt'
        _write_log_entry(log_text, 1)
        _write_log_entry('Wechsel auf Modul %s' % current_module_name, 1)
    elif len(pricelist_in_file) > 0:
        _write_log_entry('Bisherige Preisliste gelesen', 2)
        # Modul der bisherigen Liste ist mit diesem identisch, also Einträge in alter Preisliste benutzen und aufräumen
        prices_count_before_cleanup = len(pricelist_in_file)
        _write_log_entry('Bereinige bisherige Preisliste', 1)
        try:
            pricelist_in_file = _cleanup_pricelist(pricelist_in_file)
        except Exception as e:
            _write_log_entry('Fehler: ' + str(e), 0)
            _write_log_entry("Vorhandene Preisliste nicht nutzbar", 1)
            pricelist_in_file = []

        if len(pricelist_in_file) > 0:
            prices_count_after_cleanup = len(pricelist_in_file)
            _write_log_entry('Bisherige Preisliste bereinigt', 2)
            prices_count_diff = prices_count_before_cleanup - prices_count_after_cleanup
            if prices_count_diff == 0:
                _write_log_entry('Es wurde kein Preis geloescht', 2)
            elif prices_count_diff == 1:
                _write_log_entry('Es wurde 1 Preis geloescht', 2)
            elif prices_count_diff > 1:
                _write_log_entry('Es wurden %d Preise geloescht' % prices_count_diff, 2)
            if prices_count_after_cleanup > 0:
                # mindestens der aktuelle Preis ist in der Liste
                _write_log_entry('Bisherige Preisliste hat noch %d Eintraege' % prices_count_after_cleanup, 2)
                pricelist_valid_until_str = _convert_timestamp_to_str(float(pricelist_in_file[-1][0]))  # timestamp von letztem Element in Liste
                _write_log_entry('Letzter Preis in bisherige Preisliste gueltig ab ' + pricelist_valid_until_str, 2)
                if prices_count_after_cleanup < 11:
                    # weniger als 11 Stunden in bisheriger Liste: versuche, die Liste neu abzufragen
                    # dementsprechend auch bei vorherigem Fehler: 9 Einträge zu _failure_price
                    _write_log_entry('Versuche, weitere Preise von Tibber zu empfangen', 1)
                    pricelist_received = []
                    try:
                        pricelist_received = _get_updated_pricelist()
                    except Exception as e:
                        _write_log_entry(str(e), 0)
                    if len(pricelist_received) > 0:
                        _write_log_entry('Abfrage der Preise erfolgreich', 2)
                        _write_log_entry('Abgefragte Preisliste hat %d Eintraege' % len(pricelist_received), 2)
                        pricelist_valid_until_str = _convert_timestamp_to_str(float(pricelist_received[-1][0]))  # timestamp von letztem Element in Liste
                        _write_log_entry('Letzter Preis in abgefragter Preisliste gueltig ab ' + pricelist_valid_until_str, 2)
                        prices_count_diff = len(pricelist_received) - prices_count_after_cleanup
                        if prices_count_diff == 0:
                            _write_log_entry('Keine neuen Preise empfangen', 2)
                            _write_log_entry('Bereinigte bisherige Preisliste wird weiter verwendet', 2)
                        elif prices_count_diff < 0:
                            _write_log_entry('Empfangene Preisliste kuerzer als bereits vorhandene', 2)
                            _write_log_entry('Bereinigte bisherige Preisliste wird weiter verwendet', 2)
                        else:
                            _write_log_entry('%d zusaetzliche Preise empfangen' % prices_count_diff, 2)
                            _write_log_entry('Publiziere Preisliste', 1)
                            _publish_price_data(pricelist_received, current_module_name)
                            exit()
                    else:
                        _write_log_entry('Abfrage weiterer Preise nicht erfolgreich', 1)
                else:
                    _write_log_entry('Ausreichend zukuenftige Preise in bisheriger Preisliste', 1)
                # bisherige Liste hat ausreichend Preise für die Zukunft bzw.
                # mindestens den aktuellen Preis und Fehler bei der API-Abfrage
                if prices_count_before_cleanup - prices_count_after_cleanup > 0:
                    # es wurden Preise aus der bisherigen Liste bereinigt, also veröffentlichen
                    _write_log_entry('Verwende Preise aus bereinigter bisheriger Preisliste', 1)
                    _write_log_entry('Publiziere Preisliste', 1)
                    _publish_price_data(pricelist_in_file, current_module_name)
                exit()

    # bisherige Preisliste leer, fehlerhaft oder neuer Provider: in jedem Fall neue Abfrage und
    # bei andauerndem Fehler oder weiterhin leerer Liste Preis auf _failure_price setzen
    try:
        pricelist_received = _get_updated_pricelist()
    except Exception as e:
        _exit_on_invalid_price_data(str(e), current_module_name)
    # Preisliste enthält mindestens den aktuellen Preis
    pricelist_valid_until_str = _convert_timestamp_to_str(float(pricelist_received[-1][0]))  # timestamp von letztem Element in Liste
    _write_log_entry('Letzter Preis in abgefragter Preisliste gueltig ab ' + pricelist_valid_until_str, 2)
    msg = 'Publiziere Preisliste mit ' + str(len(pricelist_received))
    if len(pricelist_received) == 1:
        msg += ' Preis'
    else:
        msg += ' Preisen'
    _write_log_entry(msg, 1)
    _publish_price_data(pricelist_received, current_module_name)

#########################################################
#
# Main:
#
#########################################################

if __name__ == '__main__':
    try:
        tibber_token, home_id, debug_level = _read_args()
    except Exception as e:
        _exit_on_invalid_price_data('Modul-Abbruch: ' + str(e), MODULE_NAME)

    update_pricedata(tibber_token, home_id, debug_level)
