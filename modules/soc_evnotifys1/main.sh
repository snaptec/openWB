#!/bin/bash

soctimer=$(</var/www/html/openWB/ramdisk/soctimer1)
if (( soctimer < 4 )); then
	soctimer=$((soctimer+1))
	echo $soctimer > /var/www/html/openWB/ramdisk/soctimer1
else
	answer=$(curl -s -X GET 'https://app.evnotify.de/soc?akey='$evnotifyakeylp2'&token='$evnotifytokenlp2)
	# extract the soc value
	soc=$(echo $answer | jq .soc_display)
	# parse to int to be able to check in condition - to determine if valid or not
	isvalid=$(echo $soc | cut -d "." -f 1 | cut -d "," -f 1)
	if (( isvalid >= 0 && isvalid != null)); then
		echo $isvalid > /var/www/html/openWB/ramdisk/soc1
		echo 0 > /var/www/html/openWB/ramdisk/soctimer1
	fi
fi






