#!/bin/bash
. /var/www/html/openWB/openwb.conf

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

sudo python /var/www/html/openWB/modules/wr_plenticore/read_kostalplenticore.py $kostalplenticoreip

# Rückgabe des Wertes PV-Leistung
pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $pvwatt
