#!/bin/bash
timer=$(</var/www/html/openWB/ramdisk/soctimer1)
if (( timer < 60 )); then
	timer=$((timer+1))
	echo $timer > /var/www/html/openWB/ramdisk/soctimer1
else
 sudo python /var/www/html/openWB/modules/soc_myopellp2/opelsoc.py $soc_2_username $soc_2_password $soc_2_clientid $soc_2_clientsecret
 echo 0 > /var/www/html/openWB/ramdisk/soctimer1
