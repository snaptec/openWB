#!/bin/bash

CHARGEPOINT=$1

case $CHARGEPOINT in
	2)
		# second charge point
        lstate=$(</var/www/html/openWB/ramdisk/ladestatuss1)
        plugstatus=$(</var/www/html/openWB/ramdisk/plugstats1)
        chagerstatus=$(</var/www/html/openWB/ramdisk/chargestats1)
        soctimerfile="/var/www/html/openWB/ramdisk/soctimer1"
        username=$zoelp2username
        password=$zoelp2passwort
        socfile="/var/www/html/openWB/ramdisk/soc1"
        requestfile="/var/www/html/openWB/ramdisk/zoerequestlp2"
        request1file="/var/www/html/openWB/ramdisk/zoerequest1lp2"
        request2file="/var/www/html/openWB/ramdisk/zoerequest2lp2"
        request3file="/var/www/html/openWB/ramdisk/zoerequest3lp2"
        wakeup="wakeupzoelp2"
        zoestatusfile="/var/www/html/openWB/ramdisk/zoestatuslp2"
        ;;
	*)
        CHARGEPOINT=1
		# defaults to first charge point for backward compatibility
        lstate=$(</var/www/html/openWB/ramdisk/ladestatus)
        plugstatus=$(</var/www/html/openWB/ramdisk/plugstat)
        chagerstatus=$(</var/www/html/openWB/ramdisk/chargestat)
        soctimerfile="/var/www/html/openWB/ramdisk/soctimer"
        username=$zoeusername
        password=$zoepasswort
        socfile="/var/www/html/openWB/ramdisk/soc"
        requestfile="/var/www/html/openWB/ramdisk/zoerequest"
        request1file="/var/www/html/openWB/ramdisk/zoerequest1"
        request2file="/var/www/html/openWB/ramdisk/zoerequest2"
        request3file="/var/www/html/openWB/ramdisk/zoerequest3"
        wakeup="wakeupzoelp1"
        zoestatusfile="/var/www/html/openWB/ramdisk/zoestatus"
        ;;
esac

timer=$(<$soctimerfile)
dtime=$(date +"%T")

if (( timer < 60 )); then
	timer=$((timer+1))
	echo $timer > $soctimerfile
else
	request=$(curl -s -H "Content-Type: application/json" -X POST -d '{"username":"'$username'","password":"'$password'"}' https://www.services.renault-ze.com/api/user/login)
	token=$(echo $request | jq -r .token)
	vin=$(echo $request | jq -r .user.vehicle_details.VIN)
    request1=$(curl -s -H "Authorization: Bearer $token" https://www.services.renault-ze.com/api/vehicle/$vin/battery)
    soc=$(echo $request1 | jq .charge_level)
	request2=$(curl -s -H "Authorization: Bearer $token" https://www.services.renault-ze.com/api/vehicle/$vin/charge/scheduler/onboard)
	scheduler=$(echo $request2 | jq .enabled)
    charging=$(echo $request1 | jq .charging)
#save what we get

	echo $request > $requestfile
	echo $request1 > $request1file
    echo $request2 > $request2file
	echo $soc > $socfile
	echo 0 > $soctimerfile
    if [[ $lstate == "1" ]] && [[ $chagerstatus == "0" ]] && [[ $plugstatus == "1" ]] && [[ $scheduler == "false" ]] && [[ $soc -ne 100 ]] && [[ $charging == "false" ]] && [[ $wakeup == "1" ]] ; then
        echo " $dtime zoe p$CHARGEPOINT ladung remote gestartet"
        echo " $dtime zoe p$CHARGEPOINT lstate(wallbox) $lstate plugged(Wallbox) $plugstatus charging(Wallbox) $chagerstatus charging(Zoe) $charging scheduler(zoe) $scheduler soc $soc "
        request3=$(curl -s -H "Content-Type: application/json" -X POST -H "Authorization: Bearer $token" https://www.services.renault-ze.com/api/vehicle/$vin/charge)
        echo 0 > $zoestatusfile
        echo $request3 > $request3file
#             else
#              echo " $dtime zoe p$CHARGEPOINT laedt nicht, warte... "
#              echo " $dtime zoe p$CHARGEPOINT lstate(wallbox) $lstate plugged(Wallbox) $plugstatus charging(Wallbox) $chagerstatus charging(Zoe) $charging scheduler(zoe) $scheduler soc $soc "                    
#              echo 6 > $zoestatusfile
#            fi
     else
#           echo 0 > $zoestatusfile
            if [[ $debug = "1" ]] ; then
                echo " $dtime zoe p$CHARGEPOINT lstate(wallbox) $lstate plugged(Wallbox) $plugstatus charging(Wallbox) $chagerstatus charging(Zoe) $charging scheduler(zoe) $scheduler soc $soc wakeupzoe $wakeup"
            fi
   fi    
fi


