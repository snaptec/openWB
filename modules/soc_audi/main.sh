#!/bin/bash


auditimer=$(</var/www/html/openWB/ramdisk/soctimer)
if (( auditimer < 180 )); then
	auditimer=$((auditimer+1))
	if ((ladeleistung > 800 )); then
		auditimer=$((auditimer+2))
	fi
	echo $auditimer > /var/www/html/openWB/ramdisk/soctimer
else
	answer=$(sudo python3 /var/www/html/openWB/modules/soc_audi/Run.py $soc_audi_username $soc_audi_passwort)
	vin=$(echo $answer  | sed 's/.*: //' | head -c-3 | cut -c 2-)
	acctoken=$(cat token.json | jq -r .access_token)
	battsoc=$(curl -s --header "Accept: application/json" --header "X-App-Name: eRemote" --header "X-App-Version: 1.0.0" --header "User-Agent: okhttp/2.3.0" --header "Authorization: AudiAuth 1 $acctoken" https://msg.audi.de/fs-car/bs/batterycharge/v1/Audi/DE/vehicles/$vin/charger)
	soclevel=$(echo $battsoc | jq .charger.status.batteryStatusData.stateOfCharge.content)

	re='^-?[0-9]+$'
	if  [[ $soclevel =~ $re ]] ; then
		if (( $soclevel != 0 )) ; then
			echo $soclevel > /var/www/html/openWB/ramdisk/soc
		fi
	fi
	echo 1 > /var/www/html/openWB/ramdisk/soctimer
fi
