#!/bin/bash

soc=$(curl --connect-timeout 10 -s $speichersoc_http |sed 's/\..*$//')

re='^-?[0-9]+$'

echo $soc > /var/www/html/openWB/ramdisk/speichersoc
leistung=$(curl --connect-timeout 10 -s $speicherleistung_http )

echo $leistung > /var/www/html/openWB/ramdisk/speicherleistung

if [[ speicherikwh != "none" ]]; then
ikwh=$(curl --connect-timeout 10 -s $speicherikwh_http)
echo $ikwh > /var/www/html/openWB/ramdisk/speicherikwh
fi
if [[ speicherekwh != "none" ]]; then

ekwh=$(curl --connect-timeout 10 -s $speicherekwh_http)
echo $ekwh > /var/www/html/openWB/ramdisk/speicherekwh
fi
