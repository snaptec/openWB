#!/bin/bash
. /var/www/html/openWB/openwb.conf
timer=$(</var/www/html/openWB/ramdisk/soctimer)
if (( timer < 60 )); then
	timer=$((timer+1))
	echo $timer > /var/www/html/openWB/ramdisk/soctimer
else
	request=$(curl -s -H "Content-Type: application/json" -X POST -d '{"username":"'$zoeusername'","password":"'$zoepasswort'"}' https://www.services.renault-ze.com/api/user/login)
	token=$(echo $request | jq -r .token)
	vin=$(echo $request | jq -r .user.vehicle_details.VIN)
	soc=$(curl -s -H "Authorization: Bearer $token" https://www.services.renault-ze.com/api/vehicle/$vin/battery |jq .charge_level)
	echo $soc > /var/www/html/openWB/ramdisk/soc
	echo 0 > /var/www/html/openWB/ramdisk/soctimer
fi


