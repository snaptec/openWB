#!/bin/bash

. /var/www/html/openWB/openwb.conf

soc=$(curl --connect-timeout 10 -s $speichersoc_http)

re='^-?[0-9]+$'

echo $soc > /var/www/html/openWB/ramdisk/speichersoc
leistung=$(curl --connect-timeout 10 -s $speicherleistung_http)

re='^-?[0-9]+$'

echo $leistung > /var/www/html/openWB/ramdisk/speicherleistung



