#!/bin/bash
timer=$(</var/www/html/openWB/ramdisk/soctimer)
if (( timer < 60 )); then
	timer=$((timer+1))
	echo $timer > /var/www/html/openWB/ramdisk/soctimer
else
 sudo python /var/www/html/openWB/modules/soc_myopel/opelsoc.py $soc_1_username $soc_1_password $soc_1_clientid $soc_1_clientsecret
 echo 0 > /var/www/html/openWB/ramdisk/soctimer
