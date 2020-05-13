#!/bin/bash
timer=$(</var/www/html/openWB/ramdisk/soctimer)
if (( timer < 60 )); then
	timer=$((timer+1))
	echo $timer > /var/www/html/openWB/ramdisk/soctimer
else
 sudo python /var/www/html/openWB/modules/soc_myrenault/zoensoclp1.py $myrenault_userlp1 $myrenault_passlp1 $myrenault_locationlp1 $myrenault_countrylp1 $soclp1_vin
 echo 0 > /var/www/html/openWB/ramdisk/soctimer
 soc=$(</var/www/html/openWB/ramdisk/soc)
 lstate=$(</var/www/html/openWB/ramdisk/ladestatus)
 dtime=$(date +"%T")
 plugstatus=$(</var/www/html/openWB/ramdisk/plugstat)
 chagerstatus=$(</var/www/html/openWB/ramdisk/chargestat)
 r8=$(</var/www/html/openWB/ramdisk/zoereply8lp1)
 charging=$(echo $r8 | jq -r .data.attributes.chargingStatus)
 if [[ $lstate == "1" ]] && [[ $chagerstatus == "0" ]] && [[ $plugstatus == "1" ]] && [[ $charging == '-1' ]] && [[ $soc -ne 100 ]] && [[ $wakeupmyrenaultlp1 == "1" ]] ; then
        echo " $dtime zoe p1 ladung remote gestartet"
        echo " $dtime zoe p1 lstate(wallbox) $lstate plugged(Wallbox) $plugstatus charging(Wallbox) $chagerstatus charging(Zoe) $charging scheduler(zoe) $scheduler soc $soc "
      sudo python /var/www/html/openWB/modules/soc_myrenault/zoenwakelp1.py $myrenault_userlp1 $myrenault_passlp1  $myrenault_locationlp1  $myrenault_countrylp1 $soclp1_vin
 fi
fi





