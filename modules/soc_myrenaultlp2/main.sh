#!/bin/bash
timer=$(</var/www/html/openWB/ramdisk/soctimer1)
if (( timer < 60 )); then
	timer=$((timer+1))
	echo $timer > /var/www/html/openWB/ramdisk/soctimer1
else
sudo python /var/www/html/openWB/modules/soc_myrenaultlp2/zoensoclp2.py $myrenault_userlp2 $myrenault_passlp2 $myrenault_locationlp2  $myrenault_countrylp2 
	echo 0 > /var/www/html/openWB/ramdisk/soctimer1
	soc=$(</var/www/html/openWB/ramdisk/soc1)
	lstate=$(</var/www/html/openWB/ramdisk/ladestatuss1)
 dtime=$(date +"%T")
 plugstatus=$(</var/www/html/openWB/ramdisk/plugstats1)
 chagerstatus=$(</var/www/html/openWB/ramdisk/chargestats1)
 r8=$(</var/www/html/openWB/ramdisk/zoereply8lp2)
 charging=$(echo $r8 | jq -r .data.attributes.chargingStatus)
 if [[ $lstate == "1" ]] && [[ $chagerstatus == "0" ]] && [[ $plugstatus == "1" ]] && [[ $charging == "-1" ]] && [[ $soc -ne 100 ]] && [[ $wakeupmyrenaultlp2 == "1" ]] ; then
        echo " $dtime zoe p2 ladung remote gestartet"
        echo " $dtime zoe p2 lstate(wallbox) $lstate plugged(Wallbox) $plugstatus charging(Wallbox) $chagerstatus charging(Zoe) $charging soc $soc "
        sudo python /var/www/html/openWB/modules/soc_myrenaultlp2/zoenwakelp2.py $myrenault_userlp2 $myrenault_passlp2  $myrenault_locationlp2  $myrenault_countrylp2
 fi
fi
