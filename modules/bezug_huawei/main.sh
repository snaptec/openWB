#!/bin/bash

#datenauslesung erfolgt im PV Modul
echo $watt < /var/www/html/openWB/ramdisk/wattbezug
echo $watt
