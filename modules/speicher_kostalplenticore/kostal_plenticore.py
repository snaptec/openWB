#!/usr/bin/env python3

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

import shutil

# Speicherleistung WR 1
shutil.copy("/var/www/html/openWB/ramdisk/temp_speicherleistung", "/var/www/html/openWB/ramdisk/speicherleistung")
# Speicher Ladestand von Speicher am WR 1
shutil.copy("/var/www/html/openWB/ramdisk/temp_speichersoc", "/var/www/html/openWB/ramdisk/speichersoc")

exit(0)