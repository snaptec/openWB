#!/bin/bash

#datenauslesung erfolgt im PV Modul
watt=$(</var/www/html/openWB/ramdisk/huawaibezugwatt)
a1=$(</var/www/html/openWB/ramdisk/huawaievua1)
a2=$(</var/www/html/openWB/ramdisk/huawaievua2)
a3=$(</var/www/html/openWB/ramdisk/huawaievua3)
echo $a1 > /var/www/html/openWB/ramdisk/bezuga1
echo $a2 > /var/www/html/openWB/ramdisk/bezuga2
echo $a3 > /var/www/html/openWB/ramdisk/bezuga3

echo $watt > /var/www/html/openWB/ramdisk/wattbezug
echo $watt
