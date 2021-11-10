#!/bin/bash

#datenauslesung erfolgt im PV Modul
speichersoc=$(</var/www/html/openWB/ramdisk/huaweispeichersoc)
speicherl=$(</var/www/html/openWB/ramdisk/huaweispeicherleistung)
echo $speichersoc > /var/www/html/openWB/ramdisk/speichersoc
echo $speicherl > /var/www/html/openWB/ramdisk/speicherleistung

