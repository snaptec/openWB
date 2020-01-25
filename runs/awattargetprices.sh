#!/bin/bash

awadata=$(curl -s https://api.awattar.de/v1/marketdata)
rm /var/www/html/openWB/ramdisk/awattarstarthours
start=$(echo $awadata | jq '.data[].start_timestamp')
while IFS= read -r line; do
	date +"%H" -d @$((line/1000)) >> /var/www/html/openWB/ramdisk/awattarstarthours
done <<< "$start"
rm /var/www/html/openWB/ramdisk/awattarendhours
end=$(echo $awadata | jq '.data[].end_timestamp')
while IFS= read -r line; do
	date +"%H" -d @$((line/1000)) >> /var/www/html/openWB/ramdisk/awattarendhours
done <<< "$end"
rm /var/www/html/openWB/ramdisk/awattarpricelist
actual=0
price=$(echo $awadata | jq '.data[].marketprice')
while IFS= read -r line; do
	if ((actual == 0 )); then
		echo "scale=2;$line * 100 / 1000" | bc -l > /var/www/html/openWB/ramdisk/awattarprice
		actual=1
		actualprice=$(</var/www/html/openWB/ramdisk/awattarprice)
	fi
	echo "scale=2;$line * 100 / 1000" | bc -l >> /var/www/html/openWB/ramdisk/awattarpricelist
done <<< "$price"

paste -d "," /var/www/html/openWB/ramdisk/awattarstarthours /var/www/html/openWB/ramdisk/awattarpricelist > /var/www/html/openWB/ramdisk/awattargraphlist
mosquitto_pub -r -t openWB/global/awattar/pricelist -m "$(cat /var/www/html/openWB/ramdisk/awattargraphlist)"

