#!/usr/bin/python3
# coding: utf8

#########################################################
#
# liest von aWATTar die stündlichen Preise für heute und morgen,
# erstellt daraus die Preislisten-Datei für den Graphen und
# Datei mit aktuell gültigem Strompreis
#
# erwartet von API Stundenpreise, d.h. für jede Stunde eine Preisauskunft
# setzt aktuellen Strompreis (und für kommende 9 Std) im Fehlerfall auf 99.99ct/kWh
#
# Aufruf als Main
# oder nach Import: update_pricedata(landeskennung, basispreis, debug_level)
#
# param: Landeskennung (at/de)
# param: individueller Basispreis des Anschlusses (kann auch 0 sein)
# param: Debug-Level
#
# Preisliste in UTC und ct/kWh, Aufbau Datei:
# Zeile 1: Name des Moduls + Landeskennung z. B. aWATTar_de
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

MODULE_NAME = 'aWATTar'
LAENDERDATEN = {
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

_openWB_debug_level = 0
_module_starttime = 0

#########################################################
#
# private Hilfsfunktionen
#
#########################################################

def _check_args(arg1, arg2, arg3):
    arg1_str = re.sub('[^A-Za-z]+', '', arg1)  # Landeskennung
    if not arg1_str in LAENDERDATEN:
        raise ValueError('1. Parameter (Landeskennung = "' + arg1_str + '") unbekannt')
    arg2_str = re.sub('[^0-9.,]', '', arg2)  # Basispreis
    try:
        arg2_float = float(arg2_str)
    except:
        raise ValueError('2. Parameter (Basispreis = "' + arg2_str + '") ist keine Zahl') from None
    arg3_str = re.sub('[^0-9]+', '', arg3)  # Debug-Level
    try:
        arg3_int = int(arg3_str)
    except:
        raise ValueError('3. Parameter (Debug-Level = "' + arg3_str + '") ist keine Zahl') from None
    return arg1, arg2_float, arg3_int

def _read_args():
    # gibt Kommandozeilenparameter zurück
    if len(sys.argv) == 4:
        # sys.argv[0] : erstes Argument ist immer Dateiname
        try:
            landeskennung, basispreis, debug_level = _check_args(sys.argv[1], sys.argv[2], sys.argv[3])
        except:
            raise
    else:
        raise ValueError('Parameteranzahl falsch (' + str(len(sys.argv) - 1) + ' uebergeben aber 3 gefordert)')
    return landeskennung, basispreis, debug_level

def _write_log_entry(message, msg_debug_level = 0):
    # schreibt Eintrag ins Log je nach Level
    global _openWB_debug_level
    if msg_debug_level == 0 or _openWB_debug_level is None or msg_debug_level <= _openWB_debug_level:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S:')
        line = timestamp + ' Modul awattargetprices.py: ' + message + '\n'
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
    # schreibt 99.99ct/kWh in Preis-Datei und füllt Chart-Array für die nächsten 9 Stunden damit,
    # schreibt Fehler ins Log
    with open('/var/www/html/openWB/ramdisk/etproviderprice', 'w') as file_current_price, \
         open('/var/www/html/openWB/ramdisk/etprovidergraphlist', 'w') as file_pricelist:
        file_current_price.write('99.99\n')
        file_pricelist.write('%s\n' % current_module_name)  # erster Eintrag ist für Preisliste verantwortliches Modul
        now = datetime.now(timezone.utc)  # timezone-aware datetime-object in UTC
        timestamp = now.replace(minute=0, second=0, microsecond=0)  # volle Stunde
        for i in range(9):
            file_pricelist.write('%d, 99.99\n' % timestamp.timestamp())
            timestamp = timestamp + timedelta(hours=1)
    _write_log_entry(error, 0)
    _write_log_entry('Setze Preis auf 99.99ct/kWh.', 0)
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
                _write_log_entry('Abfrage aWATTar-API', 1)
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
def _readAPI(url):
    # Timeout für Verbindung = 2 sek und Antwort = 6 sek
    response = requests.get(url, headers={'Content-Type': 'application/json'}, timeout=(2, 6))
    return response

def _get_utcfromtimestamp(timestamp):
    # erwartet timestamp Typ float
    # gibt timezone-aware Datetime-Objekt zurück in UTC
    datetime_obj = datetime.utcfromtimestamp(timestamp)  # Zeitstempel von String nach Datetime-Objekt
    datetime_obj = datetime_obj.replace(tzinfo=timezone.utc)  # Objekt von naive nach timezone-aware, hier UTC
    return datetime_obj

def _cleanup_pricelist(pricelist):
    # bereinigt Preisliste, löscht Einträge die älter als aktuelle Stunde sind
    # und über morgen hinausgehen
    # wenn der erste Preis nicht für die aktuelle Stunde ist, wird leere Liste zurückgegeben
    # prüft auf Abstand der Preise: ist dieser >1h, wird Liste ab diesem Punkt abgeschnitten
    if len(pricelist) > 0:
        now = datetime.now(timezone.utc)  # timezone-aware datetime-object in UTC
        now_full_hour = now.replace(minute=0, second=0, microsecond=0)  # volle Stunde
        starttime_utc_prev = now  # speichert in Schleife Zeitstempel des vorherigen Listeneintrags
        for index, price in enumerate(pricelist[:]):  # über Kopie der Liste iterieren, um das Original zu manipulieren
            try:
                starttime_utc = _get_utcfromtimestamp(float(price[0]))  # Start-Zeitstempel aus Preisliste umwandeln
            except:
                raise TypeError('Zeitstempel-Umwandlung fehlgeschlagen') from None
            if starttime_utc < now_full_hour or starttime_utc.date() > now.date() + timedelta(days=1):
                pricelist.remove(price)
            if index > 0:
                # wenn der Abstand zum letzten Preis in Liste > 1 Std, dann Rest der Liste entfernen und Ende
                hourdiff = divmod((starttime_utc - starttime_utc_prev).total_seconds(), 60)
                if hourdiff != (60.0, 0.0):
                    del pricelist[index:]
                    break
            starttime_utc_prev = starttime_utc
        # wenn noch Einträge in Liste verblieben sind auf Aktulität prüfen
        if len(pricelist) > 0:
            starttime_utc = _get_utcfromtimestamp(float(pricelist[0][0]))
            if starttime_utc == now_full_hour:  # erster Preis ist der aktuelle
                return pricelist
    return []

def _get_updated_pricelist():
    # API abfragen, retry bei Timeout
    # Rückgabe ist empfangene bereinigte Preisliste mit aktuellem Preis als ersten Eintrag
    # Bei Fehler oder leerer Liste wird Exception geworfen
    # Da aWATTar pro Abruf nur max. 24h Preise liefert, benötigt man für eine komplette Liste
    # einschl. aller morgiger Preise 2 Abfragen
    #
    # zunächst Abfragen der heutigen Preise in local-time
    date_obj = datetime.now()
    start_obj = date_obj.replace(minute=0, second=0, microsecond=0)  # aktuelle volle Stunde
    start_timestamp = start_obj.timestamp() * 1000
    date_obj = date_obj + timedelta(days=1)
    end_obj = date_obj.replace(hour=0, minute=0, second=0, microsecond=0)  # Mitternacht
    end_timestamp = end_obj.timestamp() * 1000
    api_url = LAENDERDATEN[landeskennung]['url'] + '?start=' + str('%d' % start_timestamp) + '&end=' + str('%d' % end_timestamp)
    # Abfrage der Preise bis Mitternacht
    try:
        response = _readAPI(api_url)
    except:
        raise RuntimeError('Fataler Fehler bei API-Abfrage') from None
    _write_log_entry('Antwort auf Abfrage erhalten', 2)
    # sind sonstige-Fehler aufgetreten?
    try:
        response.raise_for_status()
    except:
        raise
    # Bei Erfolg JSON auswerten
    _write_log_entry('Ermittle JSON fuer heutige Preise aus aWATTar-Antwort', 1)
    try:
        marketprices = json.loads(response.text)['data']
    except:
        raise RuntimeError('Korruptes JSON') from None
    _write_log_entry("aWATTar-Preisliste fuer heute extrahiert", 1)
    # dann Abfragen der morgigen Preise in local-time
    start_timestamp = end_timestamp  # Mitternacht
    end_obj = end_obj + timedelta(days=1) # Mitternacht Übermorgen
    end_timestamp = end_obj.timestamp() * 1000
    api_url = LAENDERDATEN[landeskennung]['url'] + '?start=' + str('%d' % start_timestamp) + '&end=' + str('%d' % end_timestamp)
    # Abfrage der Preise morgen bis Mitternacht
    try:
        response = _readAPI(api_url)
    except:
        raise RuntimeError('Fataler Fehler bei API-Abfrage') from None
    _write_log_entry('Antwort auf Abfrage erhalten', 2)
    # sind sonstige-Fehler aufgetreten?
    try:
        response.raise_for_status()
    except:
        raise
    # Bei Erfolg JSON auswerten
    _write_log_entry('Ermittle JSON fuer morgige Preise aus aWATTar-Antwort', 1)
    try:
        marketprices = marketprices + json.loads(response.text)['data']
    except:
        raise RuntimeError('Korruptes JSON') from None
    _write_log_entry("aWATTar-Preisliste für morgen extrahiert", 1)

    # alle Zeiten in UTC verarbeiten
    now = datetime.now(timezone.utc)  # timezone-aware datetime-object in UTC
    now_full_hour = now.replace(minute=0, second=0, microsecond=0)  # volle Stunde
    _write_log_entry('Formatiere und analysiere Preisliste', 1)
    pricelist = []
    for price_data in marketprices:
        startzeit_utc = _get_utcfromtimestamp(price_data['start_timestamp']/1000)  # Zeitstempel kommt von API in UTC mit Millisekunden, UNIX ist ohne
        if landeskennung == 'de':
            if basispreis == 0:
                # Kein Basispreis, dann nur Anzeige des Börsenpreises [ct/kWh] ohne weitere Bestandteile
                bruttopreis = price_data['marketprice']/10
            else:
                # Bruttopreis Deutschland [ct/kWh] = ((marketpriceAusAPI/10) * 1.19) + Awattargebühr + Basispreis
                bruttopreis = (price_data['marketprice']/10 * LAENDERDATEN[landeskennung]['umsatzsteuer']) + LAENDERDATEN[landeskennung]['awattargebuehr'] + basispreis
            bruttopreis_str = str('%.2f' % round(bruttopreis, 2))
        else:
            # für Österreich keine Berechnung möglich, daher nur marketpriceAusAPI benutzen
            bruttopreis_str = str('%.2f' % round(price_data['marketprice']/10, 2))
        pricelist.append([str('%d' % startzeit_utc.timestamp()), bruttopreis_str])
    try:
        pricelist = _cleanup_pricelist(pricelist)
    except:
        raise
    if len(pricelist) == 0:
        raise RuntimeError('Aktueller Preis konnte nicht ermittelt werden')
    else:
        _write_log_entry('Aktueller Preis ist %s ct/kWh' % pricelist[0][1], 2)
    return pricelist

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

def update_pricedata(landeskennung, basispreis, debug_level):
    global _openWB_debug_level
    global _module_starttime

    _module_starttime = datetime.now()
    # bei exit immer Laufzeit des Moduls bestimmen, Funktion aber nicht doppelt registrieren
    atexit.register(_log_module_runtime)
    if __name__ != '__main__':
        try:
            _check_args(landeskennung, basispreis, debug_level)
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

    current_module_name = MODULE_NAME + '_' + landeskennung
    if len(pricelist_in_file) > 0 and pricelist_in_file[0][1] == '99.99':
        _write_log_entry('Bisherige Preisliste enthaelt nur Fehlerpreise 99.99ct/kWh', 1)
        _write_log_entry('Versuche, neue Preise von aWATTar zu empfangen', 1)
    elif module_name_in_file != None and current_module_name != module_name_in_file:
        if module_name_in_file == '':
            log_text = 'Kein Modul für bisherige Preisliste identifizierbar'
        else:
            log_text = 'Bisherige Preiliste wurde von Modul ' + module_name_in_file + ' erstellt'
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
                    # mit 10 Preisen des Tages übrig: gegen 14 Uhr gibt es neue Preise
                    _write_log_entry('Versuche, weitere Preise von aWATTar zu empfangen', 1)
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
    # bei andauerndem Fehler oder weiterhin leerer Liste Preis auf 99.99ct/kWh setzen
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
        landeskennung, basispreis, debug_level = _read_args()
    except Exception as e:
        _exit_on_invalid_price_data('Modul-Abbruch: ' + str(e), MODULE_NAME)

    update_pricedata(landeskennung, basispreis, debug_level)
