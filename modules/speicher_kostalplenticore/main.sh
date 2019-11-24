#!/bin/bash

#########################################################
#
# liest aus Wechselrichter Kostal Plenticore
# mit angeschlossener Batterie die Lade-/Entladeleistung
# und den Batterie-SOC
#
# 2019 Michael Ortenstein
# This file is part of openWB
#
#########################################################

# Daten aus temporärer ramdisk zur globalen Weiterverarbeitung in die
# entsprechenden ramdisks kopieren. Die temporären Werte stammen aus dem
# wr_plenticore Modul, werden dort zentral aus den Modbus-Registern gelesen

# Gesamt-Speicherleistung WR 1 + 2
"cp" /var/www/html/openWB/ramdisk/temp_speicherleistung /var/www/html/openWB/ramdisk/speicherleistung
# Speicherleistung WR 1
"cp" /var/www/html/openWB/ramdisk/temp_speicherleistung1 /var/www/html/openWB/ramdisk/speicherleistung1
# Speicherleistung WR 2
"cp" /var/www/html/openWB/ramdisk/temp_speicherleistung2 /var/www/html/openWB/ramdisk/speicherleistung2
# Speicher Ladestand von Speicher am WR 1
"cp" /var/www/html/openWB/ramdisk/temp_speichersoc /var/www/html/openWB/ramdisk/speichersoc
# Speicher Ladestand von Speicher am WR 2
"cp" /var/www/html/openWB/ramdisk/temp_speichersoc2 /var/www/html/openWB/ramdisk/speichersoc2
