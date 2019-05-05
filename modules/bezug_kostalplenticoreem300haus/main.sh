#!/bin/bash

# Konfigurationsdatei einbinden
. /var/www/html/openWB/openwb.conf

#########################################################
#
# ermittelt Werte Kostal Plenticore mit EM300
# für alle 3 Phasen Leistung, Strom, Spannung
# dann Netzfrequenz und Bezug/Einspeisung
#
# Werte werden im Wechselrichter-Modul ausgelesen, hier nur
# in die passende ramdisk geschrieben
#
# 2019 Michael Ortenstein
# This file is part of openWB
#
#########################################################

# Unterscheidung EM300 Sensorposition zur Bestimmung Bezug EVU
if [ $kostalplenticorehaus -eq 1 ]; then
  # EM300 Sensorposition 2 (am EVU-Übergabepunkt = grid connection)
  # Bezug EVU wurde bereits im wr_plenticore Modul aus den Modbus-Registern gelesen
  "cp" /var/www/html/openWB/ramdisk/temp_wattbezug /var/www/html/openWB/ramdisk/wattbezug
else
  # EM300 Sensorposition 1 (im Hausverbrauchszweig = home consumption)
  # Werte aus (temporärer) ramdisk lesen
  # Hausverbrauch
  Home_consumption = $(</var/www/html/openWB/ramdisk/temp_wattbezug)
  # PV-Leistung
  PV_power_ac = $(</var/www/html/openWB/ramdisk/pvwatt)
  # Speicherleistung
  Actual_batt_ch_disch_power = $(</var/www/html/openWB/ramdisk/temp_speicherleistung)
  # und Bezug berechnen
  Bezug = $((PV_power_ac + Actual_batt_ch_disch_power - Home_consumption))

  # hier muss noch Bezug nach /var/www/html/openWB/ramdisk/wattbezug geschrieben werden
fi

# Daten aus temporärer ramdisk zur globalen Weiterverarbeitung in die
# entsprechenden ramdisks kopieren. Die temporären Werte stammen aus dem
# wr_plenticore Modul, werden dort zentral aus den Modbus-Registern gelesen

# Bezug Strom Phase 1
"cp" /var/www/html/openWB/ramdisk/temp_bezuga1 /var/www/html/openWB/ramdisk/bezuga1
# Bezug Strom Phase 2
"cp" /var/www/html/openWB/ramdisk/temp_bezuga2 /var/www/html/openWB/ramdisk/bezuga2
# Bezug Strom Phase 3
"cp" /var/www/html/openWB/ramdisk/temp_bezuga3 /var/www/html/openWB/ramdisk/bezuga3
# Netzfrequenz
"cp" /var/www/html/openWB/ramdisk/temp_evuhz /var/www/html/openWB/ramdisk/evuhz
# Bezug Leistung Phase 1
"cp" /var/www/html/openWB/ramdisk/temp_bezugw1 /var/www/html/openWB/ramdisk/bezugw1
# Bezug Leistung Phase 2
"cp" /var/www/html/openWB/ramdisk/temp_bezugw2 /var/www/html/openWB/ramdisk/bezugw2
# Bezug Leistung Phase 3
"cp" /var/www/html/openWB/ramdisk/temp_bezugw3 /var/www/html/openWB/ramdisk/bezugw3
# Spannung Phase 1
"cp" /var/www/html/openWB/ramdisk/temp_evuv1 /var/www/html/openWB/ramdisk/evuv1
# Spannung Phase 2
"cp" /var/www/html/openWB/ramdisk/temp_evuv2 /var/www/html/openWB/ramdisk/evuv2
# Spannung Phase 3
"cp" /var/www/html/openWB/ramdisk/temp_evuv3 /var/www/html/openWB/ramdisk/evuv3

# Rückgabe des Wertes Bezug EVU
bezugwatt=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $bezugwatt
