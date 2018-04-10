#!/bin/bash

. /var/www/html/openWB/openwb.conf

wattbezug=$(curl --connect-timeout 10 -s $bezug_http_w_url)

re='^-?[0-9]+$'

if ! [[ $wattbezug =~ $re ]] ; then
	   wattbezug="0"
fi
echo $wattbezug
echo $wattbezug > /var/www/html/openWB/ramdisk/wattbezug

if [[ $bezug_http_ikwh_url != "none" ]]; then
	ikwh=$(curl --connect-timeout 5 -s $bezug_http_ikwh_url)
	echo $ikwh > /var/www/html/openWB/ramdisk/bezugkwh
fi
if [[ $bezug_http_ekwh_url != "none" ]]; then
	ekwh=$(curl --connect-timeout 5 -s $bezug_http_ekwh_url)
	echo $ekwh > /var/www/html/openWB/ramdisk/einspeisungkwh
fi



