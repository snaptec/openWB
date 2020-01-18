#!/bin/bash
. /var/www/html/openWB/openwb.conf
timer=$(</var/www/html/openWB/ramdisk/soctimer1)
#new variables
if (( timer < 60 )); then
	timer=$((timer+1))
	echo $timer > /var/www/html/openWB/ramdisk/soctimer1
else
#	echo $soc > /var/www/html/openWB/ramdisk/soc1
sudo python /var/www/html/openWB/modules/soc_myrenaultlp2/zoensoclp2.py $myrenault_userlp2 $myrenault_passlp2 $myrenault_locationlp2  $myrenault_countrylp2 
	echo 0 > /var/www/html/openWB/ramdisk/soctimer1
fi
