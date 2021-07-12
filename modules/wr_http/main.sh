#!/bin/bash
wattwr=$(curl --connect-timeout 10 -s $wr_http_w_url)

re='^-?[0-9]+$'

if ! [[ $wattwr =~ $re ]] ; then
	wattwr="0"
fi
if (( wattwr > 3 )); then
	wattwr=$(( wattwr * -1 ))
fi
echo $wattwr
echo $wattwr > /var/www/html/openWB/ramdisk/pvwatt

if [[ $wr_http_kwh_url != "none" ]]; then
	ekwh=$(curl --connect-timeout 5 -s $wr_http_kwh_url)
	echo $ekwh > /var/www/html/openWB/ramdisk/pvkwh
	pvkwhk=$(echo "scale=3;$ekwh / 1000" |bc)
	echo $pvkwhk > /var/www/html/openWB/ramdisk/pvkwhk
fi
