#!/usr/bin/env python3

# Konfigurationsdatei einbinden

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

import shutil
import sys

kostalplenticorehaus = str(sys.argv[1])

# Unterscheidung EM300 Sensorposition zur Bestimmung Bezug EVU
if kostalplenticorehaus == 1:
	# EM300 Sensorposition 2 (am EVU-Übergabepunkt = grid connection)
	# Bezug EVU wurde bereits im wr_plenticore Modul aus den Modbus-Registern gelesen
	shutil.copy("/var/www/html/openWB/ramdisk/temp_wattbezug", "/var/www/html/openWB/ramdisk/wattbezug")
else:
	# EM300 Sensorposition 1 (im Hausverbrauchszweig = home consumption)
	# Werte aus (temporärer) ramdisk lesen
	# aktueller Hausverbrauch
	with open("/var/www/html/openWB/ramdisk/temp_wattbezug", "r") as f:
		home_consumption=f.read()
	# aktuelle PV-Leistung
	with open("/var/www/html/openWB/ramdisk/pvwatt", "r") as f:
		pv_power_ac=f.read()
	# aktuelle Speicherleistung
	with open("/var/www/html/openWB/ramdisk/temp_speicherleistung", "r") as f:
		actual_batt_ch_disch_power=f.read()
	# Bezug berechnen
	bezug=pv_power_ac + actual_batt_ch_disch_power + home_consumption
	# und in die ramdisk
	with open("/var/www/html/openWB/ramdisk/wattbezug", "w") as f:
		f.write(bezug)


# Daten aus temporärer ramdisk zur globalen Weiterverarbeitung in die
# entsprechenden ramdisks kopieren. Die temporären Werte stammen aus dem
# wr_plenticore Modul, werden dort zentral aus den Modbus-Registern gelesen

# Bezug Strom Phase 1
shutil.copy("/var/www/html/openWB/ramdisk/temp_bezuga1", "/var/www/html/openWB/ramdisk/bezuga1")
# Bezug Strom Phase 2
shutil.copy("/var/www/html/openWB/ramdisk/temp_bezuga2", "/var/www/html/openWB/ramdisk/bezuga2")
# Bezug Strom Phase 3
shutil.copy("/var/www/html/openWB/ramdisk/temp_bezuga3", "/var/www/html/openWB/ramdisk/bezuga3")
# Netzfrequenz
shutil.copy("/var/www/html/openWB/ramdisk/temp_evuhz", "/var/www/html/openWB/ramdisk/evuhz")
# Bezug Leistung Phase 1
shutil.copy("/var/www/html/openWB/ramdisk/temp_bezugw1", "/var/www/html/openWB/ramdisk/bezugw1")
# Bezug Leistung Phase 2
shutil.copy("/var/www/html/openWB/ramdisk/temp_bezugw2", "/var/www/html/openWB/ramdisk/bezugw2")
# Bezug Leistung Phase 3
shutil.copy("/var/www/html/openWB/ramdisk/temp_bezugw3", "/var/www/html/openWB/ramdisk/bezugw3")
# Spannung Phase 1
shutil.copy("/var/www/html/openWB/ramdisk/temp_evuv1", "/var/www/html/openWB/ramdisk/evuv1")
# Spannung Phase 2
shutil.copy("/var/www/html/openWB/ramdisk/temp_evuv2", "/var/www/html/openWB/ramdisk/evuv2")
# Spannung Phase 3
shutil.copy("/var/www/html/openWB/ramdisk/temp_evuv3", "/var/www/html/openWB/ramdisk/evuv3")
# Power Faktor Phase 1
shutil.copy("/var/www/html/openWB/ramdisk/temp_evupf1", "/var/www/html/openWB/ramdisk/evupf1")
# Power Faktor Phase 2
shutil.copy("/var/www/html/openWB/ramdisk/temp_evupf2", "/var/www/html/openWB/ramdisk/evupf2")
# Power Faktor Phase 3
shutil.copy("/var/www/html/openWB/ramdisk/temp_evupf3", "/var/www/html/openWB/ramdisk/evupf3")