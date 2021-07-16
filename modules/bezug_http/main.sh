#!/bin/bash

re='^-?[0-9]+$'

wattbezug=$(curl --connect-timeout 10 -s $bezug_http_w_url)
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
if [[ $bezug_http_l1_url != "none" ]]; then
	l1a=$(curl --connect-timeout 5 -s $bezug_http_l1_url)
	echo $l1a > /var/www/html/openWB/ramdisk/bezuga1
fi
if [[ $bezug_http_l2_url != "none" ]]; then
	l2a=$(curl --connect-timeout 5 -s $bezug_http_l2_url)
	echo $l2a > /var/www/html/openWB/ramdisk/bezuga2
fi
if [[ $bezug_http_l3_url != "none" ]]; then
	l3a=$(curl --connect-timeout 5 -s $bezug_http_l3_url)
	echo $l3a > /var/www/html/openWB/ramdisk/bezuga3
fi
