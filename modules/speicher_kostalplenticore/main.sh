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

# Speicherleistung
"cp" /var/www/html/openWB/ramdisk/temp_speicherleistung /var/www/html/openWB/ramdisk/speicherleistung
# Speicher Ladestand
"cp" /var/www/html/openWB/ramdisk/temp_speichersoc /var/www/html/openWB/ramdisk/speichersoc
