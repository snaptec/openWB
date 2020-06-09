#!/bin/bash

soctimer=$(</var/www/html/openWB/ramdisk/soctimer)
if (( soctimer < 4 )); then
	soctimer=$((soctimer+1))
	echo $soctimer > /var/www/html/openWB/ramdisk/soctimer
else
	answer=$(curl -s -X GET 'https://app.evnotify.de/soc?akey='$evnotifyakey'&token='$evnotifytoken)
	# extract the soc value
	soc=$(echo $answer | jq .soc_display)
	# parse to int to be able to check in condition - to determine if valid or not
	isvalid=$(echo $soc | cut -d "." -f 1 | cut -d "," -f 1)
	if (( isvalid >= 0 && isvalid != null)); then
		echo $isvalid > /var/www/html/openWB/ramdisk/soc
		echo 0 > /var/www/html/openWB/ramdisk/soctimer
	fi
fi






