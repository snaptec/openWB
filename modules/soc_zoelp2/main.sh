#!/bin/bash
timer=$(</var/www/html/openWB/ramdisk/soctimer1)
#new variables
lstate=$(</var/www/html/openWB/ramdisk/ladestatuss1)
dtime=$(date +"%T")
plugstatus=$(</var/www/html/openWB/ramdisk/plugstats1)
chagerstatus=$(</var/www/html/openWB/ramdisk/chargestats1)
if (( timer < 60 )); then
	timer=$((timer+1))
	echo $timer > /var/www/html/openWB/ramdisk/soctimer1
else
	request=$(curl -s -H "Content-Type: application/json" -X POST -d '{"username":"'$zoelp2username'","password":"'$zoelp2passwort'"}' https://www.services.renault-ze.com/api/user/login)
	token=$(echo $request | jq -r .token)
	vin=$(echo $request | jq -r .user.vehicle_details.VIN)
    request1=$(curl -s -H "Authorization: Bearer $token" https://www.services.renault-ze.com/api/vehicle/$vin/battery)
    soc=$(echo $request1 | jq .charge_level)
	request2=$(curl -s -H "Authorization: Bearer $token" https://www.services.renault-ze.com/api/vehicle/$vin/charge/scheduler/onboard)
	scheduler=$(echo $request2 | jq .enabled)
    charging=$(echo $request1 | jq .charging)
#save what we get
	echo $request > /var/www/html/openWB/ramdisk/zoerequestlp2
	echo $request1 > /var/www/html/openWB/ramdisk/zoerequest1lp2
    echo $request2 > /var/www/html/openWB/ramdisk/zoerequest2lp2
	echo $soc > /var/www/html/openWB/ramdisk/soc1
	echo 0 > /var/www/html/openWB/ramdisk/soctimer1
    if [[ $lstate == "1" ]] && [[ $chagerstatus == "0" ]] && [[ $plugstatus == "1" ]] && [[ $scheduler == "false" ]] && [[ $soc -ne 100 ]] && [[ $charging == "false" ]] && [[ $wakeupzoelp2 == "1" ]] ; then
              echo " $dtime zoe p2 ladung remote gestartet"
              echo " $dtime zoe p2 lstate(wallbox) $lstate plugged(Wallbox) $plugstatus charging(Wallbox) $chagerstatus charging(Zoe) $charging scheduler(zoe) $scheduler soc $soc "
              request3=$(curl -s -H "Content-Type: application/json" -X POST -H "Authorization: Bearer $token" https://www.services.renault-ze.com/api/vehicle/$vin/charge)
              echo 0 > /var/www/html/openWB/ramdisk/zoestatuslp2
              echo $request3 > /var/www/html/openWB/ramdisk/zoerequest3lp2
#             else
#              echo " $dtime zoe p2 laedt nicht, warte... "
#              echo " $dtime zoe p2 lstate(wallbox) $lstate plugged(Wallbox) $plugstatus charging(Wallbox) $chagerstatus charging(Zoe) $charging scheduler(zoe) $scheduler soc $soc "                    
#              echo 6 > /var/www/html/openWB/ramdisk/zoestatuslp2
#             fi
    else
#           echo 0 > /var/www/html/openWB/ramdisk/zoestatuslp2
            if [[ $debug = "1" ]] ; then
               echo " $dtime zoe p2 lstate(wallbox) $lstate plugged(Wallbox) $plugstatus charging(Wallbox) $chagerstatus charging(Zoe) $charging scheduler(zoe) $scheduler soc $soc wakeupzoe $wakeupzoelp2 "
            fi
   fi
fi
