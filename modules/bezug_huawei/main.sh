#!/bin/bash

#datenauslesung erfolgt im PV Modul
watt=$(</var/www/html/openWB/ramdisk/huawaibezugwatt)
echo $watt > /var/www/html/openWB/ramdisk/wattbezug
echo $watt
