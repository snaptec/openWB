#!/bin/bash

. /var/www/html/openWB/openwb.conf
data=$(curl -s https://api.corrently.io/core/gsi?plz=$plz)
rm /var/www/html/openWB/ramdisk/gsiforecast.csv

echo $data |jq -r '.forecast[] | "\(.epochtime) \(.gsi)"' | while read line
do
	time=$(echo $line | awk '{print $1;}')
	ftime=$(date -d@"$time" +%d"Day"-%H"H")
	gsi=$(echo $line | awk '{print $2;}')

	echo "$ftime,$gsi" >> /var/www/html/openWB/ramdisk/gsiforecast.csv
done

