#!/bin/bash

re='^[-+]?[0-9]+\.?[0-9]*$'
r2e='^-?[0-9]+$'
wattll=$(curl --connect-timeout 3 -s $httpll_w_url)
if ! [[ $wattll =~ $re ]] ; then
	wattll="0"
fi
echo $wattll > /var/www/html/openWB/ramdisk/llaktuell
kwhll=$(curl --connect-timeout 3 -s $httpll_kwh_url)
if ! [[ $kwhll =~ $re ]] ; then
	kwhll="0"
fi
echo $kwhll > /var/www/html/openWB/ramdisk/llkwh

a1ll=$(curl --connect-timeout 3 -s $httpll_a1_url)
if ! [[ $a1ll =~ $re ]] ; then
	a1ll="0"
fi
echo $a1ll > /var/www/html/openWB/ramdisk/lla1
a2ll=$(curl --connect-timeout 3 -s $httpll_a2_url)
if ! [[ $a2ll =~ $re ]] ; then
	a1ll="0"
fi
echo $a2ll > /var/www/html/openWB/ramdisk/lla2
a3ll=$(curl --connect-timeout 3 -s $httpll_a3_url)
if ! [[ $a3ll =~ $re ]] ; then
	a3ll="0"
fi
echo $a3ll > /var/www/html/openWB/ramdisk/lla3

plugstat=$(curl --connect-timeout 2 -s $httpll_ip/plugstat)
chargestat=$(curl --connect-timeout 2 -s $httpll_ip/chargestat)
if ! [[ $plugstat =~ $r2e ]] ; then
	plugstat="0"
fi
if ! [[ $chargestat =~ $r2e ]] ; then
	chargestat="0"
fi
echo $plugstat > /var/www/html/openWB/ramdisk/plugstat
echo $chargestat > /var/www/html/openWB/ramdisk/chargestat
