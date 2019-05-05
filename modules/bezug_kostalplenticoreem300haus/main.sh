#!/bin/bash

#########################################################
#
# liest aus Wechselrichter Kostal Plenticore mit EM300
# den Strom auf allen 3 Phasen sowie Bezug/Einspeisung
# bei Verwendung EM300 am Hausanschlusspunkt
#
# 2019 Michael Ortenstein
# This file is part of openWB
#
#########################################################

# Daten aus temporärer ramdisk zur globalen Weiterverarbeitung in die
# entsprechenden ramdisks kopieren. Die temporären Werte stammen aus dem
# wr_plenticore Modul, werden dort zentral aus den Modbus-Registern gelesen

# Bezug EVU
"cp" /var/www/html/openWB/ramdisk/temp_wattbezug /var/www/html/openWB/ramdisk/wattbezug
# Bezug Phase 1
"cp" /var/www/html/openWB/ramdisk/temp_bezuga1 /var/www/html/openWB/ramdisk/bezuga1
# Bezug Phase 2
"cp" /var/www/html/openWB/ramdisk/temp_bezuga2 /var/www/html/openWB/ramdisk/bezuga2
# Bezug Phase 3
"cp" /var/www/html/openWB/ramdisk/temp_bezuga3 /var/www/html/openWB/ramdisk/bezuga3

# Rückgabe des Wertes Bezug EVU
bezugwatt=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $bezugwatt
