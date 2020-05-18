#!/bin/bash
timer=$(</var/www/html/openWB/ramdisk/soctimer)
#new variables
lstate=$(</var/www/html/openWB/ramdisk/ladestatus)
dtime=$(date +"%T")
plugstatus=$(</var/www/html/openWB/ramdisk/plugstat)
chagerstatus=$(</var/www/html/openWB/ramdisk/chargestat)
if (( timer < 60 )); then
	timer=$((timer+1))
	echo $timer > /var/www/html/openWB/ramdisk/soctimer
else
	request=$(curl -s -H "Content-Type: application/json" -X POST -d '{"username":"'$zoeusername'","password":"'$zoepasswort'"}' https://www.services.renault-ze.com/api/user/login)
	token=$(echo $request | jq -r .token)
	vin=$(echo $request | jq -r .user.vehicle_details.VIN)
    request1=$(curl -s -H "Authorization: Bearer $token" https://www.services.renault-ze.com/api/vehicle/$vin/battery)
    soc=$(echo $request1 | jq .charge_level)
	request2=$(curl -s -H "Authorization: Bearer $token" https://www.services.renault-ze.com/api/vehicle/$vin/charge/scheduler/onboard)
	scheduler=$(echo $request2 | jq .enabled)
    charging=$(echo $request1 | jq .charging)
#save what we get
	echo $request > /var/www/html/openWB/ramdisk/zoerequest
	echo $request1 > /var/www/html/openWB/ramdisk/zoerequest1
    echo $request2 > /var/www/html/openWB/ramdisk/zoerequest2
	echo $soc > /var/www/html/openWB/ramdisk/soc
	echo 0 > /var/www/html/openWB/ramdisk/soctimer
    if [[ $lstate == "1" ]] && [[ $chagerstatus == "0" ]] && [[ $plugstatus == "1" ]] && [[ $scheduler == "false" ]] && [[ $soc -ne 100 ]] && [[ $charging == "false" ]] && [[ $wakeupzoelp1 == "1" ]] ; then
              echo " $dtime zoe ladung remote gestartet"
              echo " $dtime zoe lstate(wallbox) $lstate plugged(Wallbox) $plugstatus charging(Wallbox) $chagerstatus charging(Zoe) $charging scheduler(zoe) $scheduler soc $soc "
              request3=$(curl -s -H "Content-Type: application/json" -X POST -H "Authorization: Bearer $token" https://www.services.renault-ze.com/api/vehicle/$vin/charge)
              echo 0 > /var/www/html/openWB/ramdisk/zoestatus
              echo $request3 > /var/www/html/openWB/ramdisk/zoerequest3
#             else
#              echo " $dtime zoe laedt nicht, warte... "
#              echo " $dtime zoe lstate(wallbox) $lstate plugged(Wallbox) $plugstatus charging(Wallbox) $chagerstatus charging(Zoe) $charging scheduler(zoe) $scheduler soc $soc "                    
#              echo 6 > /var/www/html/openWB/ramdisk/zoestatus
#            fi
     else
#           echo 0 > /var/www/html/openWB/ramdisk/zoestatus
            if [[ $debug = "1" ]] ; then
                echo " $dtime zoe lstate(wallbox) $lstate plugged(Wallbox) $plugstatus charging(Wallbox) $chagerstatus charging(Zoe) $charging scheduler(zoe) $scheduler soc $soc wakeupzoe $wakeupzoelp1"
            fi
   fi    
fi


