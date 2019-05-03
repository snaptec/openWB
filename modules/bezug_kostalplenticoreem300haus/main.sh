#!/bin/bash

#hier gibt es fast nichts zu tun, da alle Werte aus den Registern des WR im WR-Modul
#gelesen und berechnet werden

#. /var/www/html/openWB/openwb.conf
#sudo python /var/www/html/openWB/modules/bezug_kostalplenticoreem300haus/read_kostalplenticoreem300haus.py $kostalplenticoreip $kostalplenticorehaus

bezugwatt=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $bezugwatt
