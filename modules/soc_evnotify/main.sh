#!/bin/bash
. /var/www/html/openWB/openwb.conf


soctimer=$(</var/www/html/openWB/ramdisk/soctimer)
if (( soctimer < 4 )); then
	soctimer=$((soctimer+1))
	echo $soctimer > /var/www/html/openWB/ramdisk/soctimer
else
	token=$(</var/www/html/openWB/modules/soc_evnotify/token)
	if [[ -z "$token" ]]; then
	curl -s -H "Content-Type: application/json" --request POST -d '{"akey":"'$evnotifyakey'","password":"'$evnotifypasswort'"}' https://evnotify.de:8743/login | jq -r .token > /var/www/html/openWB/modules/soc_evnotify/token
	token=$(</var/www/html/openWB/modules/soc_evnotify/token)
	fi

	answer=$(curl -s -H "Content-Type: application/json" --request POST -d '{"akey":"'$evnotifyakey'","token":"'$token'","type":"PULL"}' https://evnotify.de:8743/sync) 
	errorhand=$(echo $answer | jq -r .message)
	if [ "$errorhand" == "Sync not enabled" ]; then
	curl -s -H "Content-Type: application/json" --request POST -d '{"akey":"'$evnotifyakey'","password":"'$evnotifypasswort'"}' https://evnotify.de:8743/login | jq -r .token > /var/www/html/openWB/modules/soc_evnotify/token
	fi
	echo $answer | jq .syncRes.curSoC > /var/www/html/openWB/ramdisk/soc
	echo 0 > /var/www/html/openWB/ramdisk/soctimer
fi






