#!/bin/bash

#########################################################
#
# liest aus Wechselrichter Kostal Plenticore Register
# zu PV-Statistik und berechnet PV-Leistung, Speicherleistung
# unter Beachtung angeschlossener Batterie falls vorhanden
#
# 2019 Michael Ortenstein
# This file is part of openWB
# 
# 01.09.2021	skl	Python3 , Anpassung auf neue .py
#########################################################

# Aufruf der Leseroutine mit den IP WR 1 und ggf. WR 2 und WR3
# WR3 kann auch eine Liste an einanderfolgenden IP haben 
if [[ $speichermodul == "speicher_kostalplenticore" ]]; then
	sudo python3 /var/www/html/openWB/modules/wr_plenticore/read_kostalplenticore.py $kostalplenticoreip $kostalplenticoreip2 1 $kostalplenticoreip3
else
	sudo python3 /var/www/html/openWB/modules/wr_plenticore/read_kostalplenticore.py $kostalplenticoreip $kostalplenticoreip2 0 $kostalplenticoreip3
fi

# Rückgabe des Wertes Gesamt-PV-Leistung
pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $pvwatt
