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
#########################################################

# Aufruf der Leseroutine mit den IP WR 1 und ggf. WR 2
if [[ $speichermodul == "speicher_kostalplenticore" ]]; then
	sudo python /var/www/html/openWB/modules/wr_plenticore/read_kostalplenticore.py $kostalplenticoreip $kostalplenticoreip2 1 $kostalplenticoreip3
else
	sudo python /var/www/html/openWB/modules/wr_plenticore/read_kostalplenticore.py $kostalplenticoreip $kostalplenticoreip2 0 $kostalplenticoreip3
fi

# Rückgabe des Wertes Gesamt-PV-Leistung
pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $pvwatt
