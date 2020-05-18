#!/bin/bash
timer=$(</var/www/html/openWB/ramdisk/soctimer)
#new variables
if (( timer < 60 )); then
	timer=$((timer+1))
	echo $timer > /var/www/html/openWB/ramdisk/soctimer
else
#	echo $soc > /var/www/html/openWB/ramdisk/soc
sudo python /var/www/html/openWB/modules/soc_myrenaultlp1/zoensoclp1.py $myrenault_userlp1 $myrenault_passlp1 $myrenault_locationlp1  $myrenault_countrylp1 
	echo 0 > /var/www/html/openWB/ramdisk/soctimer
fi
